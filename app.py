"""Cổng thông tin Khu dân cư Lăng Tô - giao diện ưu tiên điện thoại (Streamlit)."""
from __future__ import annotations

import datetime as dt
import hmac
import os
import time
from dataclasses import dataclass
from urllib.parse import quote

import pandas as pd
import streamlit as st

import storage as db
from helpers import (
    NO_DATE,
    clean_phone,
    esc,
    esc_br,
    fmt_compact,
    fmt_vnd,
    fold,
    format_phone,
    initials,
    is_yes,
    parse_date,
    parse_money,
    show_date,
    squash,
    status_class,
    valid_phone,
    year_of,
)
from styles import APP_CSS

st.set_page_config(
    page_title="Khu dân cư Lăng Tô",
    page_icon="🏘️",
    layout="centered",
    initial_sidebar_state="collapsed",
)
st.markdown("""
    <style>
    /* Ẩn dòng chữ mờ "Press Enter to submit form" bên trong ô nhập liệu */
    .stTextInput div[data-baseweb="input"]::after,
    .stTextArea textarea ~ div {
        display: none !important;
    }
    
    /* Ẩn chữ gợi ý nhỏ phía dưới input nếu có */
    div[data-testid="InputInstructions"] {
        display: none !important;
    }
    </style>
""", unsafe_allow_html=True)

# =====================================================================
# Cấu hình các trang
# =====================================================================
@dataclass(frozen=True)
class Page:
    slug: str
    icon: str
    short: str
    title: str
    subtitle: str
    bg: str  # màu nền ô biểu tượng
    fg: str


PAGES: dict[str, Page] = {
    p.slug: p
    for p in [
        Page("bang-tin", "📢", "Bảng tin", "Bảng tin & thông báo", "Tin mới nhất từ cán bộ thôn", "#e6efff", "#2559d8"),
        Page("danh-ba", "📋", "Danh bạ", "Danh bạ", "Gọi nhanh cán bộ và bà con", "#e0f5e9", "#2b8552"),
        Page("su-kien", "🎉", "Sự kiện", "Sự kiện cộng đồng", "Lịch sinh hoạt của khu dân cư", "#fff0dc", "#c26a0a"),
        Page("thu-chi", "💰", "Thu chi", "Công khai thu chi", "Minh bạch các khoản thu, chi", "#dcf4f2", "#0f8a85"),
        Page("dang-ky", "📝", "Đăng ký", "Đăng ký sự kiện", "Đăng ký tham gia trong một phút", "#eee8ff", "#6d4ad8"),
        Page("phan-anh", "⚠️", "Phản ánh", "Gửi phản ánh, kiến nghị", "Cán bộ thôn sẽ tiếp nhận và xử lý", "#ffe7e4", "#d64545"),
        Page("vinh-danh", "🏆", "Vinh danh", "Vinh danh, khen thưởng", "Những tấm gương của khu dân cư", "#fff3c9", "#a86f00"),
        Page("cho-que", "🛒", "Chợ quê", "Chợ quê nông sản", "Mua bán trực tiếp giữa bà con", "#ebf5d6", "#578512"),
        Page("dat-lich", "📅", "Đặt lịch", "Đặt lịch nhà văn hóa", "Mượn hội trường, bàn ghế, loa đài", "#e0f0fb", "#1a78b5"),
        Page("quan-tri", "🔐", "Quản trị", "Khu vực cán bộ", "Chỉ dành cho cán bộ được phân công", "#edf0f5", "#5f6f89"),
    ]
}
TILE_SLUGS = [s for s in PAGES if s != "quan-tri"]
NAV_SLUGS = ["bang-tin", "su-kien", "danh-ba", "phan-anh"]  # 4 mục + Trang chủ trên thanh dưới


# =====================================================================
# Truy cập dữ liệu
# =====================================================================
@st.cache_resource
def _bootstrap() -> bool:
    db.ensure_file()
    return True


try:
    _bootstrap()
except Exception as _exc:  # ví dụ: hệ thống tệp chỉ đọc
    st.error(f"Không tạo được file dữ liệu: {_exc}")
    st.stop()


@st.cache_data(show_spinner=False, max_entries=64)
def _cached(sheet: str, stamp: tuple[int, int]) -> pd.DataFrame:
    return db.read_sheet(sheet)


def load(sheet: str) -> pd.DataFrame:
    """Đọc một sheet; tự làm mới khi file Excel thay đổi."""
    return _cached(sheet, db.file_stamp())


def events_with_counts() -> pd.DataFrame:
    """Bảng sự kiện, cột 'Tổng Số Hộ Tham Gia' được tính lại từ các đăng ký."""
    events = load("SuKien")
    regs = load("DangKySuKien")
    if events.empty or regs.empty:
        return events
    regs = regs.copy()
    regs["_n"] = pd.to_numeric(regs["Số Lượng"], errors="coerce").fillna(1)
    totals = regs.groupby(regs["Tên Sự Kiện"].str.strip())["_n"].sum()
    events = events.copy()
    for i, name in events["Tên Sự Kiện"].items():
        key = name.strip()
        if key in totals.index:
            events.at[i, "Tổng Số Hộ Tham Gia"] = str(int(totals[key]))
    return events


# =====================================================================
# Tiện ích giao diện
# =====================================================================
def html_block(markup: str) -> None:
    st.markdown(squash(markup), unsafe_allow_html=True)


def link(slug: str, **params: str) -> str:
    """Địa chỉ nội bộ (?page=...), đã escape để đặt trong thuộc tính href."""
    query = "&".join([f"page={slug}"] + [f"{k}={quote(str(v))}" for k, v in params.items()])
    return esc("?" + query)


def empty(title: str, hint: str = "", icon: str = "📭") -> None:
    hint_html = f"<span>{esc(hint)}</span>" if hint else ""
    html_block(f'<div class="empty"><div class="e-ico">{icon}</div><b>{esc(title)}</b>{hint_html}</div>')


def flash(kind: str, message: str) -> None:
    """Lưu thông báo để hiện ở lần chạy kế tiếp (sau st.rerun)."""
    st.session_state["_flash"] = (kind, message)


def show_flash() -> None:
    item = st.session_state.pop("_flash", None)
    if not item:
        return
    kind, message = item
    getattr(st, kind if kind in ("success", "warning", "error", "info") else "info")(message)


def page_header(page: Page) -> None:
    html_block(
        f"""
        <div class="page-head">
          <a class="back" href="{link('home')}" target="_self" aria-label="Về trang chủ">‹</a>
          <div>
            <div class="ph-title">{page.icon} {esc(page.title)}</div>
            <div class="ph-sub">{esc(page.subtitle)}</div>
          </div>
        </div>
        """
    )


def bottom_nav(active: str) -> None:
    return
    items = [("home", "🏠", "Trang chủ")] + [(s, PAGES[s].icon, PAGES[s].short) for s in NAV_SLUGS]
    parts = []
    for slug, icon, label in items:
        cls = "on" if slug == active else ""
        parts.append(
            f'<a class="{cls}" href="{link(slug)}" target="_self">'
            f'<span class="i">{icon}</span><span>{esc(label)}</span></a>'
        )
    html_block(f'<div class="bottom-nav">{"".join(parts)}</div>')


def cal_chip(value: str) -> str:
    d = parse_date(value)
    if not d:
        return '<div class="cal alt">📅</div>'
    return f'<div class="cal"><b>{d.day:02d}</b><span>Th{d.month}</span></div>'


# =====================================================================
# Bảng tin
# =====================================================================
def sorted_news(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["_pin"] = df["Ghim Nổi Bật"].map(is_yes)
    df["_key"] = df["Ngày Đăng"].map(lambda v: parse_date(v) or NO_DATE)
    return df.sort_values(["_pin", "_key"], ascending=[False, False], kind="stable")


def news_card(r) -> str:
    pinned = bool(r["_pin"])
    cat = r["Phân Loại"].strip() or "Chung"
    meta = []
    if r["Ngày Đăng"].strip():
        meta.append(f"🗓 {esc(show_date(r['Ngày Đăng']))}")
    if r["Người Đăng"].strip():
        meta.append(f"👤 {esc(r['Người Đăng'])}")
    pin_badge = '<span class="badge warn">📌 Ghim</span>' if pinned else ""
    return f"""
    <div class="card {'pinned' if pinned else ''}">
      <div class="card-top">{pin_badge}<span class="badge">{esc(cat)}</span></div>
      <div class="card-title">{esc(r['Tiêu Đề'] or 'Thông báo')}</div>
      <div class="card-body">{esc_br(r['Nội Dung'])}</div>
      <div class="card-meta">{''.join(f'<span>{m}</span>' for m in meta)}</div>
    </div>
    """


def page_news() -> None:
    df = load("ThongBao")
    if df.empty:
        empty("Chưa có thông báo nào", "Khi cán bộ đăng tin mới, bà con sẽ thấy ở đây.")
        return
    df = sorted_news(df)
    cats = sorted({c.strip() for c in df["Phân Loại"] if c.strip()})
    if len(cats) > 1:
        pick = st.selectbox("Lọc theo loại", ["Tất cả"] + cats, label_visibility="collapsed")
        if pick != "Tất cả":
            df = df[df["Phân Loại"].str.strip() == pick]
    html_block("".join(news_card(r) for _, r in df.iterrows()))


# =====================================================================
# Danh bạ
# =====================================================================
def person_card(r) -> str:
    phone = clean_phone(r["Số Điện Thoại"])
    call = f'<a class="callbtn" href="tel:{phone}" target="_self">📞 Gọi</a>' if phone else ""
    officer = '<span class="badge">Cán bộ</span>' if is_yes(r["Cán Bộ"]) else ""
    phone_line = f'<div class="phone">{esc(format_phone(phone))}</div>' if phone else ""
    return f"""
    <div class="card person">
      <div class="avatar">{esc(initials(r['Họ Tên']))}</div>
      <div class="info">
        <div class="name">{esc(r['Họ Tên'])} {officer}</div>
        <div class="role">{esc(r['Chức Vụ'])}</div>
        {phone_line}
      </div>
      {call}
    </div>
    """


def page_contacts() -> None:
    df = load("DanhBaThon")
    if df.empty:
        empty("Danh bạ đang trống", "Cán bộ thôn sẽ cập nhật số điện thoại tại đây.")
        return
    query = st.text_input("Tìm kiếm", placeholder="🔍 Tìm theo tên, chức vụ hoặc số điện thoại", label_visibility="collapsed")
    only_officers = st.toggle("Chỉ hiện cán bộ thôn", value=False)
    df = df.copy()
    df["_off"] = df["Cán Bộ"].map(is_yes)
    if only_officers:
        df = df[df["_off"]]
    if query.strip() and not df.empty:
        needle = fold(query)
        df = df[df.apply(lambda row: needle in fold(" ".join(str(v) for v in row.values)), axis=1)]
    df = df.sort_values("_off", ascending=False, kind="stable")
    if df.empty:
        empty("Không tìm thấy kết quả", "Thử gõ tên ngắn hơn hoặc bỏ bộ lọc.", "🔍")
        return
    html_block("".join(person_card(r) for _, r in df.iterrows()))


# =====================================================================
# Sự kiện
# =====================================================================
def page_events() -> None:
    df = events_with_counts()
    if df.empty:
        empty("Chưa có sự kiện nào", "Sự kiện mới sẽ hiện ở đây ngay khi được đăng.", "🎉")
        return
    today = dt.date.today()

    def order(value: str) -> tuple[int, int]:
        d = parse_date(value)
        if d is None:
            return (1, 0)
        return (0, d.toordinal()) if d >= today else (2, -d.toordinal())

    keys = [order(v) for v in df["Thời Gian Bắt Đầu"]]
    df = df.iloc[sorted(range(len(df)), key=keys.__getitem__)]

    cards = []
    for _, r in df.iterrows():
        d = parse_date(r["Thời Gian Bắt Đầu"])
        past = d is not None and d < today
        badges = []
        if d is not None:
            if d == today:
                badges.append('<span class="badge warn">Hôm nay</span>')
            elif past:
                badges.append('<span class="badge gray">Đã diễn ra</span>')
            else:
                badges.append('<span class="badge ok">Sắp diễn ra</span>')
        joined = r["Tổng Số Hộ Tham Gia"].strip()
        if joined and joined != "0":
            badges.append(f'<span class="badge">👥 {esc(joined)} đăng ký</span>')
        meta = []
        if r["Thời Gian Bắt Đầu"].strip():
            meta.append(f"🕒 {esc(show_date(r['Thời Gian Bắt Đầu']))}")
        if r["Địa Điểm"].strip():
            meta.append(f"📍 {esc(r['Địa Điểm'])}")
        button = ""
        if not past:
            button = f'<a class="btn-link" href="{link("dang-ky", sk=r["Tên Sự Kiện"].strip())}" target="_self">Đăng ký tham gia</a>'
        cards.append(
            f"""
            <div class="card">
              <div class="row-card" style="align-items:flex-start">
                {cal_chip(r['Thời Gian Bắt Đầu'])}
                <div class="rc-main">
                  <div class="card-top">{''.join(badges)}</div>
                  <div class="card-title">{esc(r['Tên Sự Kiện'])}</div>
                </div>
              </div>
              <div class="card-body" style="margin-top:8px">{esc_br(r['Mô Tả'])}</div>
              <div class="card-meta">{''.join(f'<span>{m}</span>' for m in meta)}</div>
              {button}
            </div>
            """
        )
    html_block("".join(cards))


# =====================================================================
# Đăng ký sự kiện
# =====================================================================
def page_register() -> None:
    events = events_with_counts()
    names = [n.strip() for n in events["Tên Sự Kiện"] if n.strip()] if not events.empty else []
    if not names:
        empty("Hiện chưa có sự kiện để đăng ký", "Bà con quay lại sau khi cán bộ đăng sự kiện mới nhé.", "📝")
        return

    preset = st.query_params.get("sk", "")
    with st.form("form_dang_ky", clear_on_submit=True):
        ho_ten = st.text_input("Họ và tên hộ gia đình / cá nhân *", placeholder="Ví dụ: Nguyễn Văn A", max_chars=80)
        su_kien = st.selectbox("Sự kiện *", names, index=names.index(preset) if preset in names else 0)
        so_luong = st.number_input("Số người tham gia", min_value=1, max_value=50, value=1, step=1)
        ghi_chu = st.text_input("Ghi chú (không bắt buộc)", max_chars=200)
        submitted = st.form_submit_button("Xác nhận đăng ký")

    if submitted:
        if not ho_ten.strip():
            st.warning("Vui lòng nhập họ và tên để cán bộ ghi nhận.")
        else:
            try:
                db.append_row(
                    "DangKySuKien",
                    {
                        "Họ Tên": ho_ten.strip(),
                        "Tên Sự Kiện": su_kien,
                        "Số Lượng": str(int(so_luong)),
                        "Ghi Chú": ghi_chu.strip(),
                        "Ngày Đăng Ký": str(dt.date.today()),
                    },
                )
                db.write_sheet("SuKien", events_with_counts())
            except Exception as exc:
                st.error(f"Chưa lưu được đăng ký, vui lòng thử lại. ({exc})")
            else:
                flash("success", f"Đã ghi nhận đăng ký của '{ho_ten.strip()}' cho sự kiện '{su_kien}'.")
                st.rerun()

    html_block('<div class="sec"><b>Số đăng ký hiện tại</b></div>')
    rows = []
    for _, r in events.iterrows():
        n = r["Tổng Số Hộ Tham Gia"].strip() or "0"
        rows.append(
            f'<div class="lrow"><div class="lr-main"><div class="lr-title">{esc(r["Tên Sự Kiện"])}</div>'
            f'<div class="lr-sub">{esc(show_date(r["Thời Gian Bắt Đầu"]))}</div></div>'
            f'<div class="lr-amt">{esc(n)} 👥</div></div>'
        )
    html_block(f'<div class="card ledger">{"".join(rows)}</div>')


# =====================================================================
# Công khai thu chi
# =====================================================================
def page_finance() -> None:
    df = load("CongKhaiThuChi")
    if df.empty:
        empty("Chưa có khoản thu, chi nào được công khai", "Cán bộ sẽ cập nhật tại đây để bà con cùng theo dõi.", "💰")
        return
    df = df.copy()
    df["_d"] = df["Ngày"].map(lambda v: parse_date(v) or NO_DATE)
    df["_thu"] = df["Thu (VNĐ)"].map(parse_money)
    df["_chi"] = df["Chi (VNĐ)"].map(parse_money)

    all_label = "Tất cả các tháng"
    months = sorted({(d.year, d.month) for d in df["_d"] if d != NO_DATE}, reverse=True)
    balance_label = "Còn lại"
    if months:
        labels = {f"Tháng {m:02d}/{y}": (y, m) for y, m in months}
        pick = st.selectbox("Xem theo tháng", [all_label] + list(labels), label_visibility="collapsed")
        if pick != all_label:
            y, m = labels[pick]
            df = df[df["_d"].map(lambda d: (d.year, d.month) == (y, m))]
            balance_label = f"Chênh lệch {pick.lower()}"
    df = df.sort_values("_d", ascending=False, kind="stable")

    thu, chi = int(df["_thu"].sum()), int(df["_chi"].sum())
    con_lai = thu - chi
    html_block(
        f"""
        <div class="stat-main {'neg' if con_lai < 0 else ''}">
          <div class="l">{esc(balance_label)}</div>
          <div class="v">{esc(fmt_vnd(con_lai))}</div>
        </div>
        <div class="stat-row">
          <div class="stat"><div class="l">Tổng thu</div><div class="v in">{esc(fmt_compact(thu))}</div></div>
          <div class="stat"><div class="l">Tổng chi</div><div class="v out">{esc(fmt_compact(chi))}</div></div>
        </div>
        """
    )
    if df.empty:
        empty("Tháng này chưa có khoản nào")
        return
    rows = []
    for _, r in df.iterrows():
        amounts = []
        if r["_thu"]:
            amounts.append(f'<div class="lr-amt in">+{esc(fmt_vnd(r["_thu"]))}</div>')
        if r["_chi"]:
            amounts.append(f'<div class="lr-amt out">−{esc(fmt_vnd(r["_chi"]))}</div>')
        sub = " · ".join(x for x in [show_date(r["Ngày"]), r["Ghi Chú"].strip()] if x)
        rows.append(
            f'<div class="lrow"><div class="lr-main"><div class="lr-title">{esc(r["Nội Dung"])}</div>'
            f'<div class="lr-sub">{esc(sub)}</div></div><div>{"".join(amounts)}</div></div>'
        )
    html_block(f'<div class="card ledger">{"".join(rows)}</div>')


# =====================================================================
# Phản ánh, kiến nghị
# =====================================================================
def page_feedback() -> None:
    html_block(
        '<div class="card-body" style="margin:0 2px 12px">'
        "🔒 Phản ánh chỉ hiển thị với cán bộ thôn, không đăng công khai."
        "</div>"
    )
    with st.form("form_phan_anh", clear_on_submit=True):
        nguoi_gui = st.text_input("Họ và tên của bạn *", max_chars=80)
        linh_vuc = st.selectbox("Lĩnh vực", ["Môi trường", "An ninh trật tự", "Hạ tầng / Đường xá", "Tranh chấp", "Khác"])
        noi_dung = st.text_area("Nội dung phản ánh *", placeholder="Mô tả rõ sự việc để cán bộ xử lý nhanh hơn", max_chars=2000, height=140)
        dia_diem = st.text_input("Địa điểm xảy ra", placeholder="Ví dụ: đầu ngõ 12, gần nhà văn hóa", max_chars=200)
        submitted = st.form_submit_button("Gửi phản ánh")
    if not submitted:
        return
    if not nguoi_gui.strip() or not noi_dung.strip():
        st.warning("Vui lòng điền họ tên và nội dung phản ánh.")
        return
    try:
        db.append_row(
            "PhanAnh",
            {
                "Người Gửi": nguoi_gui.strip(),
                "Lĩnh Vực": linh_vuc,
                "Nội Dung": noi_dung.strip(),
                "Địa Điểm": dia_diem.strip(),
                "Ngày Gửi": str(dt.date.today()),
                "Trạng Thái": "Chờ xử lý",
            },
        )
    except Exception as exc:
        st.error(f"Chưa gửi được phản ánh, vui lòng thử lại. ({exc})")
    else:
        st.success("Đã gửi phản ánh đến cán bộ thôn. Cảm ơn bà con!")


# =====================================================================
# Vinh danh
# =====================================================================
def page_honors() -> None:
    df = load("VinhDanh")
    if df.empty:
        empty("Chưa có danh sách vinh danh", "Những gương sáng của khu dân cư sẽ được ghi nhận tại đây.", "🏆")
        return
    df = df.copy()
    df["_y"] = df["Năm"].map(year_of)
    years = sorted({y for y in df["_y"] if y}, reverse=True)
    if len(years) > 1:
        pick = st.selectbox("Lọc theo năm", ["Tất cả các năm"] + [str(y) for y in years], label_visibility="collapsed")
        if pick != "Tất cả các năm":
            df = df[df["_y"] == int(pick)]
    df = df.sort_values("_y", ascending=False, kind="stable")
    cards = []
    for _, r in df.iterrows():
        year = f'<span class="badge gray">{esc(r["Năm"])}</span>' if r["Năm"].strip() else ""
        reason = f'<div class="h-reason">{esc_br(r["Lý Do Khen Thưởng"])}</div>' if r["Lý Do Khen Thưởng"].strip() else ""
        cards.append(
            f"""
            <div class="card honor">
              <div class="trophy">🏆</div>
              <div class="h-info">
                <div class="h-name">{esc(r['Họ Tên'])}</div>
                <div class="h-title">{esc(r['Danh Hiệu'])}</div>
                {reason}
              </div>
              {year}
            </div>
            """
        )
    html_block("".join(cards))


# =====================================================================
# Chợ quê nông sản
# =====================================================================
def product_card(r) -> str:
    price = parse_money(r["Giá Bán"])
    unit = r["Đơn Vị"].strip()
    if price > 0:
        per = f" / {esc(unit)}" if unit else ""
        price_html = f'<div class="price">{esc(fmt_vnd(price))}<small>{per}</small></div>'
    else:
        price_html = '<div class="price"><small>Liên hệ để hỏi giá</small></div>'
    phone = clean_phone(r["Số Điện Thoại"])
    call = f'<a class="btn-link" href="tel:{phone}" target="_self">📞 Gọi {esc(format_phone(phone))}</a>' if phone else ""
    posted = f'<div class="card-meta"><span>🗓 Đăng ngày {esc(show_date(r["Ngày Đăng"]))}</span></div>' if r["Ngày Đăng"].strip() else ""
    cat = f'<span class="badge ok">{esc(r["Phân Loại"])}</span>' if r["Phân Loại"].strip() else ""
    return f"""
    <div class="card">
      <div class="prod-top">
        <div>
          <div class="card-top">{cat}</div>
          <div class="card-title">{esc(r['Tên Sản Phẩm'])}</div>
        </div>
        {price_html}
      </div>
      {posted}
      {call}
    </div>
    """


def page_market() -> None:
    tab_view, tab_post = st.tabs(["🛍️ Xem nông sản", "➕ Đăng bán"])
    with tab_view:
        df = load("ChoQue")
        if df.empty:
            empty("Chợ quê chưa có sản phẩm", "Bà con bấm 'Đăng bán' để giới thiệu sản phẩm của nhà mình.", "🛒")
        else:
            query = st.text_input("Tìm sản phẩm", placeholder="🔍 Tìm sản phẩm", label_visibility="collapsed", key="cq_q")
            cats = sorted({c.strip() for c in df["Phân Loại"] if c.strip()})
            if len(cats) > 1:
                pick = st.selectbox("Loại", ["Tất cả loại"] + cats, label_visibility="collapsed", key="cq_cat")
                if pick != "Tất cả loại":
                    df = df[df["Phân Loại"].str.strip() == pick]
            if query.strip():
                needle = fold(query)
                df = df[df["Tên Sản Phẩm"].map(lambda v: needle in fold(v))]
            df = df.iloc[::-1]  # mới đăng lên trước
            if df.empty:
                empty("Không tìm thấy sản phẩm", "Thử từ khóa khác.", "🔍")
            else:
                html_block("".join(product_card(r) for _, r in df.iterrows()))
    with tab_post:
        with st.form("form_cho_que", clear_on_submit=True):
            ten = st.text_input("Tên sản phẩm *", max_chars=100)
            loai = st.selectbox("Phân loại", ["Nông sản", "Thực phẩm", "Thủ công mỹ nghệ", "Đồ dùng gia đình"])
            gia = st.number_input("Giá bán (VNĐ)", min_value=0, step=1000, value=0, help="Để 0 nếu muốn người mua liên hệ để hỏi giá.")
            don_vi = st.text_input("Đơn vị tính", placeholder="kg, bó, lít, chục...", max_chars=20)
            sdt = st.text_input("Số điện thoại liên hệ *", placeholder="09xx xxx xxx", max_chars=20)
            submitted = st.form_submit_button("Đăng bán sản phẩm")
        if submitted:
            if not ten.strip():
                st.warning("Vui lòng nhập tên sản phẩm.")
            elif not valid_phone(sdt):
                st.warning("Số điện thoại chưa đúng, vui lòng nhập lại (9-11 chữ số).")
            else:
                try:
                    db.append_row(
                        "ChoQue",
                        {
                            "Tên Sản Phẩm": ten.strip(),
                            "Phân Loại": loai,
                            "Giá Bán": str(int(gia)),
                            "Đơn Vị": don_vi.strip(),
                            "Số Điện Thoại": clean_phone(sdt),
                            "Ngày Đăng": str(dt.date.today()),
                        },
                    )
                except Exception as exc:
                    st.error(f"Chưa đăng được sản phẩm, vui lòng thử lại. ({exc})")
                else:
                    flash("success", "Đã đăng bán sản phẩm. Bà con có thể xem ở tab 'Xem nông sản'.")
                    st.rerun()


# =====================================================================
# Đặt lịch nhà văn hóa
# =====================================================================
def booking_card(r) -> str:
    status = r["Trạng Thái"].strip() or "Chờ duyệt"
    purpose = f'<div class="card-meta"><span>{esc(r["Mục Đích"])}</span></div>' if r["Mục Đích"].strip() else ""
    return f"""
    <div class="card row-card">
      {cal_chip(r['Ngày Sử Dụng'])}
      <div class="rc-main">
        <div class="card-title tight">{esc(r['Dịch Vụ'])}</div>
        <div class="card-meta"><span>👤 {esc(r['Họ Tên'])}</span><span>🗓 {esc(show_date(r['Ngày Sử Dụng']))}</span></div>
        {purpose}
      </div>
      <span class="badge {status_class(status)}">{esc(status)}</span>
    </div>
    """


def page_booking() -> None:
    df = load("DatLichNhaVanHoa")
    today = dt.date.today()

    with st.form("form_dat_lich", clear_on_submit=True):
        ho_ten = st.text_input("Họ và tên người đăng ký *", max_chars=80)
        dich_vu = st.selectbox("Loại dịch vụ", ["Mượn Nhà văn hóa", "Mượn bàn ghế / loa đài", "Đăng ký họp thôn"])
        ngay = st.date_input("Ngày sử dụng", min_value=today, value=today, format="DD/MM/YYYY")
        muc_dich = st.text_area("Mục đích sử dụng", placeholder="Ví dụ: tổ chức đám cưới, họp tổ dân phố...", max_chars=500, height=100)
        submitted = st.form_submit_button("Gửi yêu cầu đặt lịch")

    if submitted:
        if not ho_ten.strip():
            st.warning("Vui lòng nhập họ và tên người đăng ký.")
        else:
            busy = (
                not df.empty
                and (
                    (df["Dịch Vụ"].str.strip() == dich_vu)
                    & (df["Ngày Sử Dụng"].map(lambda v: parse_date(v) == ngay))
                    & ~df["Trạng Thái"].map(lambda s: status_class(s) == "bad")
                ).any()
            )
            try:
                db.append_row(
                    "DatLichNhaVanHoa",
                    {
                        "Họ Tên": ho_ten.strip(),
                        "Dịch Vụ": dich_vu,
                        "Ngày Sử Dụng": str(ngay),
                        "Mục Đích": muc_dich.strip(),
                        "Trạng Thái": "Chờ duyệt",
                    },
                )
            except Exception as exc:
                st.error(f"Chưa gửi được yêu cầu, vui lòng thử lại. ({exc})")
            else:
                if busy:
                    flash("warning", "Đã gửi yêu cầu. Lưu ý: ngày này đã có người đăng ký cùng dịch vụ, cán bộ sẽ liên hệ để sắp xếp.")
                else:
                    flash("success", "Đã gửi yêu cầu đặt lịch. Vui lòng chờ cán bộ duyệt.")
                st.rerun()

    html_block('<div class="sec"><b>Lịch sắp tới</b></div>')
    if df.empty:
        empty("Chưa có lịch đặt nào", "", "📅")
        return
    df = df.copy()
    df["_d"] = df["Ngày Sử Dụng"].map(lambda v: parse_date(v) or NO_DATE)
    upcoming = df[df["_d"] >= today].sort_values("_d", kind="stable")
    if upcoming.empty:
        empty("Chưa có lịch sắp tới", "", "📅")
    else:
        html_block("".join(booking_card(r) for _, r in upcoming.iterrows()))
    past = df[df["_d"] < today].sort_values("_d", ascending=False, kind="stable")
    if not past.empty:
        with st.expander(f"Lịch đã qua ({len(past)})"):
            html_block("".join(booking_card(r) for _, r in past.head(30).iterrows()))


# =====================================================================
# Khu vực cán bộ
# =====================================================================
DEFAULT_PASSWORD = "admin123"
BACKUP_LABEL = "🗄️ Sao lưu & khôi phục"


def admin_password() -> str:
    try:
        secret = st.secrets.get("ADMIN_PASSWORD")
    except Exception:
        secret = None
    return str(secret or os.environ.get("ADMIN_PASSWORD") or DEFAULT_PASSWORD)


ADMIN_SECTIONS: dict[str, str] = {
    "📢 Thông báo": "ThongBao",
    "📋 Danh bạ": "DanhBaThon",
    "🎉 Sự kiện": "SuKien",
    "📝 Đăng ký sự kiện": "DangKySuKien",
    "💰 Thu chi": "CongKhaiThuChi",
    "⚠️ Phản ánh": "PhanAnh",
    "🏆 Vinh danh": "VinhDanh",
    "🛒 Chợ quê": "ChoQue",
    "📅 Đặt lịch": "DatLichNhaVanHoa",
}
# Cột chọn từ danh sách: giá trị đầu tiên là mặc định khi ô để trống
ADMIN_SELECTS: dict[str, dict[str, list[str]]] = {
    "ThongBao": {"Ghim Nổi Bật": ["Không", "Có"]},
    "DanhBaThon": {"Cán Bộ": ["Không", "Có"]},
    "PhanAnh": {"Trạng Thái": ["Chờ xử lý", "Đang xử lý", "Đã xử lý", "Từ chối"]},
    "DatLichNhaVanHoa": {"Trạng Thái": ["Chờ duyệt", "Đã duyệt", "Từ chối"]},
}
ADMIN_WIDE = {"ThongBao": ["Nội Dung"], "SuKien": ["Mô Tả"], "PhanAnh": ["Nội Dung"]}


def admin_editor_data(sheet: str) -> tuple[pd.DataFrame, dict]:
    """Dữ liệu + cấu hình cột cho bảng chỉnh sửa (ô chọn từ danh sách, cột rộng)."""
    cc = st.column_config
    df = load(sheet).copy()
    config: dict = {col: cc.TextColumn(width="large") for col in ADMIN_WIDE.get(sheet, [])}
    for col, options in ADMIN_SELECTS.get(sheet, {}).items():
        df[col] = df[col].map(lambda v, first=options[0]: v.strip() or first)
        extra = [v for v in df[col].unique() if v not in options]  # giữ nguyên giá trị cũ ngoài danh sách
        config[col] = cc.SelectboxColumn(options=options + extra)
    return df, config


def admin_backup() -> None:
    st.caption(
        "Nên tải file sao lưu định kỳ. Trên một số máy chủ miễn phí, dữ liệu có thể bị xóa khi ứng dụng khởi động lại."
    )
    st.download_button(
        "⬇️ Tải file Excel sao lưu",
        data=db.export_bytes(),
        file_name=f"dulieu_langto_{dt.date.today():%Y%m%d}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    st.markdown("**Khôi phục từ file sao lưu**")
    upload = st.file_uploader("Chọn file .xlsx", type=["xlsx"], label_visibility="collapsed")
    if upload is not None:
        agree = st.checkbox("Tôi hiểu: toàn bộ dữ liệu hiện tại sẽ được thay bằng file này.")
        if st.button("Khôi phục dữ liệu", disabled=not agree):
            try:
                db.restore_from_bytes(upload.getvalue())
            except Exception as exc:
                st.error(str(exc))
            else:
                flash("success", "Đã khôi phục dữ liệu từ file Excel.")
                st.rerun()


def page_admin() -> None:
    if not st.session_state.get("is_admin"):
        with st.form("login", clear_on_submit=True):
            password = st.text_input("Mật khẩu cán bộ", type="password")
            go = st.form_submit_button("Đăng nhập")
        if go:
            if hmac.compare_digest(password.encode(), admin_password().encode()):
                st.session_state["is_admin"] = True
                st.rerun()
            else:
                time.sleep(1)
                st.error("Mật khẩu chưa đúng. Vui lòng thử lại.")
        return

    if admin_password() == DEFAULT_PASSWORD:
        st.warning("Đang dùng mật khẩu mặc định. Hãy cấu hình lại bảo mật nếu cần.")
    if st.button("Đăng xuất"):
        st.session_state["is_admin"] = False
        st.rerun()

    choice = st.selectbox("Chọn mục cần quản lý", list(ADMIN_SECTIONS) + [BACKUP_LABEL])
    if choice == BACKUP_LABEL:
        admin_backup()
        return

    sheet = ADMIN_SECTIONS[choice]
    data, config = admin_editor_data(sheet)
    
    # Thêm cột checkbox chọn xóa vào bảng dữ liệu quản trị
    if not data.empty:
        if "_xoa" not in data.columns:
            data.insert(0, "_xoa", False)
        config["_xoa"] = st.column_config.CheckboxColumn("🗑️ Xóa?", default=False)

    edited = st.data_editor(data, num_rows="dynamic", hide_index=True, column_config=config, key=f"ed_{sheet}")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("💾 Lưu thay đổi", type="primary", use_container_width=True):
            try:
                # Lọc bỏ các dòng có tích chọn xóa trước khi ghi dữ liệu xuống database
                if "_xoa" in edited.columns:
                    final_data = edited[edited["_xoa"] == False].drop(columns=["_xoa"])
                else:
                    final_data = edited
                db.write_sheet(sheet, final_data)
            except Exception as exc:
                st.error(f"Lỗi khi lưu dữ liệu: {exc}")
            else:
                flash("success", "Đã lưu thay đổi và xóa các dòng đã chọn thành công!")
                st.rerun()
    with col2:
        if st.button("🔄 Làm mới bảng", use_container_width=True):
            st.rerun()


# =====================================================================
# Trang chủ
# =====================================================================
def page_home() -> None:
    news = sorted_news(load("ThongBao"))
    n_news = len(news)
    n_events = len(load("SuKien"))
    n_contacts = len(load("DanhBaThon"))

    html_block(
        f"""
        <div class="hero">
          <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 6px;">
            <div class="hero-mark" style="margin-bottom: 0;">🏡</div>
            <div class="hero-title" style="margin-bottom: 0;font-size: 18px;">Khu dân cư Lăng Tô</div>
          </div>
          <div class="hero-sub">Trang thông tin và điều hành.</div>
          <div class="chips">
            <a class="chip" href="{link('bang-tin')}" target="_self">📢 {n_news} thông báo</a>
            <a class="chip" href="{link('su-kien')}" target="_self">🎉 {n_events} sự kiện</a>
            <a class="chip" href="{link('danh-ba')}" target="_self">📋 {n_contacts} liên hệ</a>
          </div>
        </div>
        """
    )

    tiles = "".join(
        f'<a class="tile" href="{link(p.slug)}" target="_self">'
        f'<span class="ico" style="background:{p.bg};color:{p.fg}">{p.icon}</span>'
        f'<span class="lbl">{esc(p.short)}</span></a>'
        for p in (PAGES[s] for s in TILE_SLUGS)
    )
    html_block(f'<div class="grid3">{tiles}</div>')

    if not news.empty:
        html_block(f'<div class="sec"><b>Tin mới nhất</b><a href="{link("bang-tin")}" target="_self">Xem tất cả</a></div>')
        html_block(news_card(news.iloc[0]))

    html_block(
        f'<div class="admin-link"><a href="{link("quan-tri")}" target="_self">🔐 Khu vực cán bộ</a></div>'
        '<div class="tip">Mẹo: mở menu trình duyệt và chọn “Thêm vào màn hình chính” để dùng như một ứng dụng.</div>'
    )


# =====================================================================
# Điều hướng
# =====================================================================
ROUTES = {
    "bang-tin": page_news,
    "danh-ba": page_contacts,
    "su-kien": page_events,
    "thu-chi": page_finance,
    "dang-ky": page_register,
    "phan-anh": page_feedback,
    "vinh-danh": page_honors,
    "cho-que": page_market,
    "dat-lich": page_booking,
    "quan-tri": page_admin,
}


def current_slug() -> str:
    slug = st.query_params.get("page", "home")
    return slug if slug in ROUTES else "home"


def main() -> None:
    st.markdown("<style>" + APP_CSS + "</style>", unsafe_allow_html=True)
    slug = current_slug()
    if slug == "home":
        show_flash()
        page_home()
    else:
        page_header(PAGES[slug])
        show_flash()
        ROUTES[slug]()
    bottom_nav(slug)


main()
