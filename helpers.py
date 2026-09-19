"""Hàm tiện ích thuần Python (không phụ thuộc Streamlit): định dạng, làm sạch, escape HTML."""
from __future__ import annotations

import datetime as dt
import html
import re
import unicodedata
import warnings

import pandas as pd

warnings.filterwarnings("ignore", message=".*dayfirst.*")
warnings.filterwarnings("ignore", message=".*Could not infer format.*")

NO_DATE = dt.date.min  # dùng khi ô ngày để trống / không đọc được, để sắp xếp không lỗi

_YES = {"có", "co", "x", "yes", "y", "true", "1", "ghim", "cán bộ", "can bo", "cb", "✓", "✔"}


# ---------------------------------------------------------------- văn bản / HTML
def is_yes(value) -> bool:
    """Ô 'Có/Không' trong Excel -> bool (chịu được nhiều cách gõ)."""
    return str("" if value is None else value).strip().lower() in _YES


def esc(value) -> str:
    """Escape mọi dữ liệu người dùng trước khi đưa vào HTML (chống chèn mã)."""
    return html.escape("" if value is None else str(value).strip(), quote=True)


def esc_br(value) -> str:
    """Như esc() nhưng giữ xuống dòng."""
    text = esc(value).replace("\r\n", "\n").replace("\r", "\n")
    return text.replace("\n", "<br>")


def squash(markup: str) -> str:
    """Gộp HTML nhiều dòng thành một dòng - tránh Markdown hiểu nhầm thụt lề là khối code."""
    return " ".join(line.strip() for line in markup.strip().splitlines() if line.strip())


def fold(text) -> str:
    """Bỏ dấu tiếng Việt + chữ thường, để tìm kiếm 'nguyen' vẫn ra 'Nguyễn'."""
    t = unicodedata.normalize("NFD", str("" if text is None else text).lower().replace("đ", "d"))
    return "".join(ch for ch in t if unicodedata.category(ch) != "Mn")


def initials(name) -> str:
    parts = str("" if name is None else name).split()
    if not parts:
        return "?"
    if len(parts) == 1:
        return parts[0][0].upper()
    return (parts[0][0] + parts[-1][0]).upper()


# ---------------------------------------------------------------- ngày
_ISO = re.compile(r"^(\d{4})-(\d{2})-(\d{2})(?:[ T](\d{2}):(\d{2})(?::\d{2}(?:\.\d+)?)?)?$")


def parse_date(value) -> dt.date | None:
    s = str("" if value is None else value).strip()
    if not s:
        return None
    ts = pd.to_datetime(s, errors="coerce", dayfirst=not _ISO.match(s))  # ISO: năm-tháng-ngày; còn lại: ngày/tháng/năm
    return None if pd.isna(ts) else ts.date()


def show_date(value) -> str:
    """2025-06-20 19:00 -> '19:00, 20/06/2025'; chuỗi khác giữ nguyên."""
    s = str("" if value is None else value).strip()
    m = _ISO.match(s)
    if not m:
        return s
    y, mo, d, hh, mm = m.groups()
    out = f"{d}/{mo}/{y}"
    if hh is not None and (hh, mm) != ("00", "00"):
        out = f"{hh}:{mm}, {out}"
    return out


def year_of(value) -> int:
    m = re.search(r"\d{4}", str("" if value is None else value))
    return int(m.group()) if m else 0


# ---------------------------------------------------------------- tiền
_GROUPED = re.compile(r"^-?\d{1,3}([.,]\d{3})+$")


def parse_money(value) -> int:
    """'1.500.000' / '1,500,000' / '1500000.0' / '1500000 đ' -> 1500000."""
    s = re.sub(r"[^\d.,\-]", "", str("" if value is None else value))
    if not s or s in {"-", ".", ","}:
        return 0
    if _GROUPED.match(s):
        s = re.sub(r"[.,]", "", s)
    else:
        s = s.replace(",", ".")
    try:
        return int(round(float(s)))
    except ValueError:
        return 0


def fmt_vnd(amount: int) -> str:
    return f"{int(amount):,}".replace(",", ".") + " đ"


def fmt_compact(amount: int) -> str:
    a = abs(amount)
    if a >= 1_000_000_000:
        return f"{amount / 1e9:.1f}".replace(".", ",").replace(",0", "") + " tỷ"
    if a >= 1_000_000:
        return f"{amount / 1e6:.1f}".replace(".", ",").replace(",0", "") + " triệu"
    return fmt_vnd(amount)


# ---------------------------------------------------------------- điện thoại
def clean_phone(value) -> str:
    """Chuẩn hoá SĐT Việt Nam: bỏ ký tự lạ, +84 -> 0, bù số 0 bị Excel làm mất."""
    digits = re.sub(r"\D", "", str("" if value is None else value))
    if not digits:
        return ""
    if digits.startswith("84") and 11 <= len(digits) <= 12:
        digits = "0" + digits[2:]
    if len(digits) == 9 and digits[0] in "35789":
        digits = "0" + digits
    return digits


def format_phone(digits: str) -> str:
    if len(digits) == 10:
        return f"{digits[:4]} {digits[4:7]} {digits[7:]}"
    if len(digits) == 11:
        return f"{digits[:4]} {digits[4:8]} {digits[8:]}"
    return digits


def valid_phone(value) -> bool:
    return 9 <= len(clean_phone(value)) <= 11


# ---------------------------------------------------------------- trạng thái
def status_class(status) -> str:
    """Tên trạng thái -> màu huy hiệu (ok / warn / bad / gray)."""
    t = str("" if status is None else status).strip().lower()
    if not t:
        return "gray"
    if any(k in t for k in ("từ chối", "hủy", "huỷ", "không duyệt")):
        return "bad"
    if any(k in t for k in ("chờ", "chưa", "đang", "mới", "tiếp nhận")):
        return "warn"
    if any(k in t for k in ("đã", "duyệt", "xong", "hoàn")):
        return "ok"
    return "gray"
