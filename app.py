import streamlit as st
import pandas as pd
import datetime
import os
import openpyxl

# --- CẤU HÌNH TRANG WEB ---
st.set_page_config(
    page_title="Quản Lý Khu Dân Cư Lăng Tô", 
    page_icon="🏘️", 
    layout="centered"
)

# --- TÊN FILE EXCEL ---
EXCEL_FILE = "dulieu_langto.xlsx"

# --- KHỞI TẠO CẤU TRÚC CỘT CHUẨN CHO 10 TAB CHỨC NĂNG ---
DEFAULT_COLUMNS = {
    "ThongBao": ["Tiêu Đề", "Nội Dung", "Phân Loại", "Ngày Đăng", "Người Đăng", "Ghim Nổi Bật"],
    "DanhBaThon": ["Họ Tên", "Chức Vụ", "Số Điện Thoại", "Cán Bộ"],
    "SuKien": ["Tên Sự Kiện", "Mô Tả", "Thời Gian Bắt Đầu", "Địa Điểm", "Tổng Số Hộ Tham Gia"],
    "DangKySuKien": ["Họ Tên", "Tên Sự Kiện", "Số Lượng", "Ghi Chú", "Ngày Đăng Ký"],
    "CongKhaiThuChi": ["Ngày", "Nội Dung", "Thu (VNĐ)", "Chi (VNĐ)", "Ghi Chú"],
    "PhanAnh": ["Người Gửi", "Lĩnh Vực", "Nội Dung", "Địa Điểm", "Ngày Gửi", "Trạng Thái"],
    "VinhDanh": ["Họ Tên", "Danh Hiệu", "Lý Do Khen Thưởng", "Năm"],
    "ChoQue": ["Tên Sản Phẩm", "Phân Loại", "Giá Bán", "Đơn Vị", "Số Điện Thoại", "Ngày Đăng"],
    "DatLichNhaVanHoa": ["Họ Tên", "Dịch Vụ", "Ngày Sử Dụng", "Mục Đích", "Trạng Thái"]
}

def init_excel_file():
    if not os.path.exists(EXCEL_FILE):
        with pd.ExcelWriter(EXCEL_FILE, engine='openpyxl') as writer:
            for sheet, cols in DEFAULT_COLUMNS.items():
                pd.DataFrame(columns=cols).to_excel(writer, sheet_name=sheet, index=False)
    else:
        try:
            xls = pd.ExcelFile(EXCEL_FILE)
            existing_sheets = [s.lower() for s in xls.sheet_names]
            with pd.ExcelWriter(EXCEL_FILE, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
                for sheet, cols in DEFAULT_COLUMNS.items():
                    if sheet.lower() not in existing_sheets:
                        pd.DataFrame(columns=cols).to_excel(writer, sheet_name=sheet, index=False)
        except Exception:
            pass

init_excel_file()

# --- CSS TỐI ƯU GIAO DIỆN DI ĐỘNG: 3 NÚT 1 HÀNG KHÍT MÀN HÌNH ---
st.markdown("""
<style>
    /* Ép toàn bộ container vừa vặn màn hình điện thoại, chống tràn */
    .block-container {
        padding-left: 0.3rem !important;
        padding-right: 0.3rem !important;
        padding-top: 0.3rem !important;
        max-width: 100% !important;
    }

    .stApp {
        background-color: #f8fafc;
    }
    
    /* Banner xanh dương chuyên nghiệp, bo tròn các góc */
    .app-banner {
        background: linear-gradient(135deg, #1e3a8a, #3b82f6);
        color: white;
        padding: 10px 12px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(30, 58, 138, 0.2);
        margin-bottom: 8px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .banner-icon {
        font-size: 24px;
        background: rgba(255, 255, 255, 0.2);
        padding: 4px 8px;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .banner-text h3 {
        margin: 0;
        font-size: 14px;
        font-weight: 700;
        letter-spacing: 0.3px;
    }
    .banner-text p {
        margin: 2px 0 0 0;
        font-size: 10px;
        opacity: 0.9;
    }

    /* ÉP CỨNG CHUẨN 3 CỘT / HÀNG NGANG TRÊN MỌI THIẾT BỊ DI ĐỘNG */
    div[data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        gap: 2px !important;
        width: 100% !important;
    }

    div[data-testid="column"] {
        width: 33.333% !important;
        flex: 1 1 33.333% !important;
        min-width: 33.333% !important;
        max-width: 33.333% !important;
        padding: 0 1px !important;
    }
    
    /* Thiết kế nút bấm dịch vụ: thu gọn padding để vừa khít 3 nút trên màn hình dọc */
    .stButton button {
        width: 100% !important;
        background-color: #ffffff;
        color: #1e293b;
        border: 1px solid #cbd5e1;
        border-radius: 8px;
        padding: 5px 1px !important;
        font-size: 9.5px !important;
        font-weight: 600;
        box-shadow: 0 1px 2px rgba(0,0,0,0.02);
        transition: all 0.2s ease;
        text-align: center;
        margin-bottom: 2px;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    
    .stButton button:hover {
        border-color: #3b82f6;
        color: #3b82f6;
    }

    /* KHU VỰC ĐIỀU HƯỚNG: NÚT QUAY LẠI VÀ TIÊU ĐỀ NẰM SÁT GỌN GÀNG CÙNG 1 HÀNG */
    .nav-back-container button {
        background-color: #f1f5f9 !important;
        color: #334155 !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 6px !important;
        font-size: 9.5px !important;
        padding: 2px 6px !important;
        font-weight: 600 !important;
        width: auto !important;
        margin: 0 !important;
    }

    .nav-title-text {
        font-size: 11.5px !important;
        font-weight: 700 !important;
        color: #1e293b !important;
        margin: 0 !important;
        text-align: right;
    }

    /* NỘI DUNG VÀ BẢNG DỮ LIỆU: TIÊU ĐỀ 12px, NỘI DUNG 11px */
    h1 {
        font-size: 12px !important;
    }
    
    [data-testid="stDataFrame"] div, [data-testid="stDataEditor"] div, p, span, label, .streamlit-expanderHeader {
        font-size: 11px !important;
    }
    
    table {
        width: 100% !important;
    }
    
    input, select, textarea {
        font-size: 11px !important;
    }
</style>
""", unsafe_allow_html=True)

# --- CÁC HÀM XỬ LÝ DỮ LIỆU EXCEL ---
def clean_dataframe(df, sheet_name):
    if df is None:
        df = pd.DataFrame()
    df = df.loc[:, ~df.columns.astype(str).str.contains('Unnamed|none|nan', case=False, na=False)]
    df = df.dropna(how="all")
    if sheet_name in DEFAULT_COLUMNS:
        expected_cols = DEFAULT_COLUMNS[sheet_name]
        for col in expected_cols:
            if col not in df.columns:
                df[col] = ""
        df = df[expected_cols]
    for col in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            df[col] = df[col].dt.strftime('%Y-%m-%d')
        else:
            df[col] = df[col].astype(str).replace('nan', '').replace('None', '')
    return df

@st.cache_data(ttl=1)
def load_excel_data(sheet_name):
    try:
        if not os.path.exists(EXCEL_FILE):
            init_excel_file()
        xls = pd.ExcelFile(EXCEL_FILE)
        sheet_map = {s.lower(): s for s in xls.sheet_names}
        target_lower = sheet_name.lower()
        if target_lower in sheet_map:
            df = pd.read_excel(EXCEL_FILE, sheet_name=sheet_map[target_lower], dtype=str)
            return clean_dataframe(df, sheet_name)
        else:
            return pd.DataFrame(columns=DEFAULT_COLUMNS.get(sheet_name, []))
    except Exception:
        return pd.DataFrame(columns=DEFAULT_COLUMNS.get(sheet_name, []))

def save_entire_sheet(sheet_name, df_modified):
    try:
        df_modified = clean_dataframe(df_modified, sheet_name)
        init_excel_file()
        xls = pd.ExcelFile(EXCEL_FILE)
        sheet_map = {s.lower(): s for s in xls.sheet_names}
        actual_sheet_name = sheet_map.get(sheet_name.lower(), sheet_name)
        all_dfs = {}
        for s in xls.sheet_names:
            if s.lower() == sheet_name.lower():
                all_dfs[actual_sheet_name] = df_modified
            else:
                df_s = pd.read_excel(EXCEL_FILE, sheet_name=s, dtype=str)
                found_key = s
                for k in DEFAULT_COLUMNS:
                    if k.lower() == s.lower():
                        found_key = k
                        break
                all_dfs[s] = clean_dataframe(df_s, found_key)
        if actual_sheet_name not in all_dfs:
            all_dfs[actual_sheet_name] = df_modified
        with pd.ExcelWriter(EXCEL_FILE, engine='openpyxl', mode='w') as writer:
            for s, df in all_dfs.items():
                df.to_excel(writer, sheet_name=s, index=False)
        st.cache_data.clear()
        return True
    except Exception as e:
        st.error(f"Lỗi khi lưu file: {e}")
        return False

def save_row_to_excel(sheet_name, new_data_dict):
    try:
        df_current = load_excel_data(sheet_name)
        df_new = pd.DataFrame([new_data_dict])
        df_combined = pd.concat([df_current, df_new], ignore_index=True)
        if save_entire_sheet(sheet_name, df_combined):
            st.cache_data.clear()
            return True
        return False
    except Exception as e:
        st.error(f"Lỗi khi thêm dữ liệu: {e}")
        return False

def display_df_with_1_index(df):
    df_clean = clean_dataframe(df, "")
    if not df_clean.empty:
        df_reset = df_clean.reset_index(drop=True)
        df_reset.insert(0, "STT", range(1, len(df_reset) + 1))
        st.dataframe(df_reset, use_container_width=True, hide_index=True)
    else:
        st.info("💡 Hiện chưa có dữ liệu.")

def get_updated_events_df():
    df_sk = load_excel_data("SuKien")
    df_dk = load_excel_data("DangKySuKien")
    if df_sk.empty:
        return df_sk
    df_sk_calc = df_sk.copy()
    if not df_dk.empty and 'Tên Sự Kiện' in df_dk.columns:
        df_dk['Số Lượng_num'] = pd.to_numeric(df_dk['Số Lượng'], errors='coerce').fillna(1) if 'Số Lượng' in df_dk.columns else 1
        sum_dk = df_dk.groupby('Tên Sự Kiện')['Số Lượng_num'].sum().reset_index()
        for idx, row in df_sk_calc.iterrows():
            ten_sk = row.get('Tên Sự Kiện', '')
            matched = sum_dk[sum_dk['Tên Sự Kiện'].str.strip() == ten_sk.strip()]
            if not matched.empty:
                df_sk_calc.loc[idx, 'Tổng Số Hộ Tham Gia'] = str(int(matched['Số Lượng_num'].values[0]))
    return df_sk_calc

# --- QUẢN LÝ TRANG (STATE) ---
if "current_page" not in st.session_state:
    st.session_state.current_page = "Trang Chủ"

def navigate_to(page_name):
    st.session_state.current_page = page_name
    st.rerun()

# --- ĐIỀU HƯỚNG GIAO DIỆN CHÍNH (NÚT QUAY LẠI SÁT TIÊU ĐỀ NỘI DUNG) ---
if st.session_state.current_page != "Trang Chủ":
    page_titles = {
        "Bảng Tin": "📢 Bảng Tin & Thông Báo",
        "Danh Bạ Thôn": "📋 Danh Bạ Cư Dân",
        "Sự Kiện": "🎉 Sự Kiện Cộng Đồng",
        "Công Khai Thu Chi": "💰 Công Khai Tài Chính",
        "Đăng Ký Sự Kiện": "📝 Đăng Ký Sự Kiện",
        "Phản Ánh Kiến Nghị": "⚠️ Gửi Phản Ánh",
        "Vinh Danh Khen Thưởng": "🏆 Vinh Danh Khen Thưởng",
        "Chợ Quê Nông Sản": "🛒 Chợ Quê Nông Sản",
        "Đặt Lịch Nhà Văn Hóa": "📅 Đặt Lịch Văn Hóa",
        "Khu Vực Quản Trị Cán Bộ": "🔐 Quản Trị Cán Bộ"
    }
    current_title = page_titles.get(st.session_state.current_page, st.session_state.current_page)
    
    col_nav_btn, col_nav_title = st.columns([1.2, 3.8])
    with col_nav_btn:
        st.markdown('<div class="nav-back-container">', unsafe_allow_html=True)
        if st.button("⬅️ Trang chủ", key="btn_back_home"):
            navigate_to("Trang Chủ")
        st.markdown('</div>', unsafe_allow_html=True)
    with col_nav_title:
        st.markdown(f'<p class="nav-title-text">{current_title}</p>', unsafe_allow_html=True)
    st.markdown("<hr style='margin: 4px 0 8px 0; border: none; border-top: 1px solid #e2e8f0;'>", unsafe_allow_html=True)

# ================= TRANG CHỦ =================
if st.session_state.current_page == "Trang Chủ":
    
    # Banner hiện đại bo tròn
    st.markdown("""
        <div class="app-banner">
            <div class="banner-icon">🏡</div>
            <div class="banner-text">
                <h3>KHU DÂN CƯ LĂNG TÔ</h3>
                <p>Cổng Thông Tin Quản Lý Cộng Đồng</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # --- HÀNG 1 (3 NÚT) ---
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📢 Bảng Tin", use_container_width=True): navigate_to("Bảng Tin")
    with col2:
        if st.button("📋 Danh Bạ", use_container_width=True): navigate_to("Danh Bạ Thôn")
    with col3:
        if st.button("🎉 Sự Kiện", use_container_width=True): navigate_to("Sự Kiện")

    # --- HÀNG 2 (3 NÚT) ---
    col4, col5, col6 = st.columns(3)
    with col4:
        if st.button("💰 Thu Chi", use_container_width=True): navigate_to("Công Khai Thu Chi")
    with col5:
        if st.button("📝 Đăng Ký", use_container_width=True): navigate_to("Đăng Ký Sự Kiện")
    with col6:
        if st.button("⚠️ Phản Ánh", use_container_width=True): navigate_to("Phản Ánh Kiến Nghị")

    # --- HÀNG 3 (3 NÚT) ---
    col7, col8, col9 = st.columns(3)
    with col7:
        if st.button("🏆 Vinh Danh", use_container_width=True): navigate_to("Vinh Danh Khen Thưởng")
    with col8:
        if st.button("🛒 Chợ Quê", use_container_width=True): navigate_to("Chợ Quê Nông Sản")
    with col9:
        if st.button("📅 Đặt Lịch", use_container_width=True): navigate_to("Đặt Lịch Nhà Văn Hóa")

    # --- HÀNG 4: NÚT QUẢN TRỊ ĐẶC BIỆT ---
    col10, col11, col12 = st.columns(3)
    with col11:
        if st.button("🔐 Quản Trị", use_container_width=True): navigate_to("Khu Vực Quản Trị Cán Bộ")


# ================= CHI TIẾT 10 TAB CHỨC NĂNG =================

elif st.session_state.current_page == "Bảng Tin":
    df_tb = load_excel_data("ThongBao")
    if not df_tb.empty:
        for idx, row in df_tb.iterrows():
            ghim = "📌 [Ghim]" if str(row.get('Ghim Nổi Bật', '')) == "Có" else ""
            with st.expander(f"{ghim} {row.get('Tiêu Đề', 'Thông báo')} (Loại: {row.get('Phân Loại', 'Chung')})"):
                st.write(f"**Nội dung:** {row.get('Nội Dung', '')}")
                st.write(f"📅 Ngày: {row.get('Ngày Đăng', '')} | 👤 Đăng bởi: {row.get('Người Đăng', '')}")
    else:
        st.info("Chưa có thông báo nào.")

elif st.session_state.current_page == "Danh Bạ Thôn":
    df_db = load_excel_data("DanhBaThon")
    display_df_with_1_index(df_db)

elif st.session_state.current_page == "Sự Kiện":
    df_sk_hien_thi = get_updated_events_df()
    display_df_with_1_index(df_sk_hien_thi)

elif st.session_state.current_page == "Công Khai Thu Chi":
    df_tc = load_excel_data("CongKhaiThuChi")
    display_df_with_1_index(df_tc)

elif st.session_state.current_page == "Đăng Ký Sự Kiện":
    df_sk = load_excel_data("SuKien")
    df_sk_hien_thi = get_updated_events_df()
    
    st.subheader("📅 Danh sách sự kiện")
    display_df_with_1_index(df_sk_hien_thi)
    
    with st.form("form_dang_ky", clear_on_submit=True):
        st.subheader("Biểu mẫu đăng ký tham gia")
        ho_ten_ho = st.text_input("Họ và tên hộ gia đình / cá nhân")
        list_sk = df_sk['Tên Sự Kiện'].tolist() if not df_sk.empty and 'Tên Sự Kiện' in df_sk.columns else []
        chon_sk = st.selectbox("Chọn sự kiện", list_sk if list_sk else ["Không có sự kiện"])
        so_luong_them = st.number_input("Số lượng tham gia", min_value=1, value=1, step=1)
        ghi_chu_dk = st.text_input("Ghi chú")
        submitted_dk = st.form_submit_button("Xác nhận đăng ký")
        
        if submitted_dk:
            if not ho_ten_ho.strip() or not list_sk:
                st.warning("Vui lòng nhập đầy đủ thông tin!")
            else:
                data_dang_ky = {
                    "Họ Tên": ho_ten_ho,
                    "Tên Sự Kiện": chon_sk,
                    "Số Lượng": str(so_luong_them),
                    "Ghi Chú": ghi_chu_dk,
                    "Ngày Đăng Ký": str(datetime.date.today())
                }
                if save_row_to_excel("DangKySuKien", data_dang_ky):
                    updated_sk = get_updated_events_df()
                    save_entire_sheet("SuKien", updated_sk)
                    st.success(f"Đã ghi nhận đăng ký thành công cho '{ho_ten_ho}'!")
                    st.rerun()

elif st.session_state.current_page == "Phản Ánh Kiến Nghị":
    with st.form("form_phan_anh", clear_on_submit=True):
        nguoi_gui = st.text_input("Họ và tên của bạn")
        linh_vuc_pa = st.selectbox("Lĩnh vực", ["Môi trường", "An ninh trật tự", "Hạ tầng / Đường xá", "Tranh chấp", "Khác"])
        noi_dung_pa = st.text_area("Nội dung chi tiết phản ánh")
        vi_tri_pa = st.text_input("Địa điểm xảy ra vấn đề")
        submitted_pa = st.form_submit_button("Gửi phản ánh")
        if submitted_pa:
            if not nguoi_gui.strip() or not noi_dung_pa.strip():
                st.warning("Vui lòng điền họ tên và nội dung!")
            else:
                data_pa = {
                    "Người Gửi": nguoi_gui,
                    "Lĩnh Vực": linh_vuc_pa,
                    "Nội Dung": noi_dung_pa,
                    "Địa Điểm": vi_tri_pa,
                    "Ngày Gửi": str(datetime.date.today()),
                    "Trạng Thái": "Chờ xử lý"
                }
                if save_row_to_excel("PhanAnh", data_pa):
                    st.success("Phản ánh của bạn đã được gửi thành công đến cán bộ thôn!")

elif st.session_state.current_page == "Vinh Danh Khen Thưởng":
    df_vd = load_excel_data("VinhDanh")
    display_df_with_1_index(df_vd)

elif st.session_state.current_page == "Chợ Quê Nông Sản":
    tab_xem, tab_dang = st.tabs(["🛍️ Xem nông sản", "➕ Đăng bán sản phẩm"])
    with tab_xem:
        df_cq = load_excel_data("ChoQue")
        display_df_with_1_index(df_cq)
    with tab_dang:
        with st.form("form_cho_que", clear_on_submit=True):
            ten_sp = st.text_input("Tên sản phẩm")
            phan_loai_sp = st.selectbox("Phân loại", ["Nông sản", "Thực phẩm", "Thủ công mỹ nghệ", "Đồ dùng gia đình"])
            gia_sp = st.number_input("Giá bán (VNĐ)", min_value=0, step=1000)
            don_vi_sp = st.text_input("Đơn vị tính (kg, bó, lít...)")
            sdt_lh = st.text_input("Số điện thoại liên hệ")
            submitted_cq = st.form_submit_button("Đăng bán sản phẩm")
            if submitted_cq:
                if not ten_sp.strip() or not sdt_lh.strip():
                    st.warning("Vui lòng nhập tên sản phẩm và số điện thoại!")
                else:
                    data_cq = {
                        "Tên Sản Phẩm": ten_sp,
                        "Phân Loại": phan_loai_sp,
                        "Giá Bán": str(gia_sp),
                        "Đơn Vị": don_vi_sp,
                        "Số Điện Thoại": sdt_lh,
                        "Ngày Đăng": str(datetime.date.today())
                    }
                    if save_row_to_excel("ChoQue", data_cq):
                        st.success("Đăng bán sản phẩm thành công!")
                        st.rerun()

elif st.session_state.current_page == "Đặt Lịch Nhà Văn Hóa":
    df_dl = load_excel_data("DatLichNhaVanHoa")
    display_df_with_1_index(df_dl)
    with st.form("form_dat_lich", clear_on_submit=True):
        ho_ten_dl = st.text_input("Họ và tên người đăng ký")
        dich_vu = st.selectbox("Loại dịch vụ", ["Mượn Nhà văn hóa", "Mượn bàn ghế / loa đài", "Đăng ký họp thôn"])
        ngay_dat = st.date_input("Ngày sử dụng")
        muc_dich = st.text_area("Mục đích sử dụng chi tiết")
        submitted_dl = st.form_submit_button("Gửi yêu cầu đặt lịch")
        if submitted_dl:
            if not ho_ten_dl.strip():
                st.warning("Vui lòng nhập họ và tên!")
            else:
                data_dl = {
                    "Họ Tên": ho_ten_dl,
                    "Dịch Vụ": dich_vu,
                    "Ngày Sử Dụng": str(ngay_dat),
                    "Mục Đích": muc_dich,
                    "Trạng Thái": "Chờ duyệt"
                }
                if save_row_to_excel("DatLichNhaVanHoa", data_dl):
                    st.success("Yêu cầu đặt lịch đã được gửi thành công.")

elif st.session_state.current_page == "Khu Vực Quản Trị Cán Bộ":
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        with st.form("login_form"):
            password = st.text_input("Nhập mật khẩu quản trị", type="password")
            submit_login = st.form_submit_button("Đăng nhập")
            if submit_login:
                if password == "admin123":
                    st.session_state.authenticated = True
                    st.success("Đăng nhập thành công!")
                    st.rerun()
                else:
                    st.error("Mật khẩu không chính xác!")
    else:
        st.success("✅ Cán bộ đã đăng nhập thành công. Bạn có thể tự do chỉnh sửa trực tiếp dữ liệu trên các bảng dưới đây.")
        if st.button("Đăng xuất"):
            st.session_state.authenticated = False
            st.rerun()

        st.markdown("---")
        df_sk = load_excel_data("SuKien")
        df_tb = load_excel_data("ThongBao")
        df_db = load_excel_data("DanhBaThon")
        df_tc = load_excel_data("CongKhaiThuChi")
        df_pa = load_excel_data("PhanAnh")
        df_vd = load_excel_data("VinhDanh")
        df_dl = load_excel_data("DatLichNhaVanHoa")
        df_cq = load_excel_data("ChoQue")

        tab_tb, tab_db, tab_sk, tab_tc, tab_pa, tab_vd, tab_cq, tab_dl = st.tabs([
            "📢 Thông Báo", "📋 Danh Bạ", "🎉 Sự Kiện", "💰 Thu Chi", 
            "⚠️ Phản Ánh", "🏆 Vinh Danh", "🛒 Chợ Quê", "📅 Đặt Lịch"
        ])
        
        with tab_tb:
            st.subheader("Quản lý Thông Báo")
            edited_tb = st.data_editor(df_tb, num_rows="dynamic", key="editor_tb_free", use_container_width=True)
            if st.button("💾 Lưu thay đổi Thông Báo", key="btn_save_tb"):
                if save_entire_sheet("ThongBao", edited_tb): st.success("Lưu thành công!").rerun()

        with tab_db:
            st.subheader("Quản lý Danh Bạ")
            edited_db = st.data_editor(df_db, num_rows="dynamic", key="editor_db_free", use_container_width=True)
            if st.button("💾 Lưu thay đổi Danh Bạ", key="btn_save_db"):
                if save_entire_sheet("DanhBaThon", edited_db): st.success("Lưu thành công!").rerun()

        with tab_sk:
            st.subheader("Quản lý Sự Kiện")
            edited_sk = st.data_editor(df_sk, num_rows="dynamic", key="editor_sk_free", use_container_width=True)
            if st.button("💾 Lưu thay đổi Sự Kiện", key="btn_save_sk"):
                if save_entire_sheet("SuKien", edited_sk): st.success("Lưu thành công!").rerun()

        with tab_tc:
            st.subheader("Quản lý Thu Chi")
            edited_tc = st.data_editor(df_tc, num_rows="dynamic", key="editor_tc_free", use_container_width=True)
            if st.button("💾 Lưu thay đổi Thu Chi", key="btn_save_tc"):
                if save_entire_sheet("CongKhaiThuChi", edited_tc): st.success("Lưu thành công!").rerun()

        with tab_pa:
            st.subheader("Xử lý Phản Ánh")
            edited_pa = st.data_editor(df_pa, num_rows="dynamic", key="editor_pa_free", use_container_width=True)
            if st.button("💾 Lưu thay đổi Phản Ánh", key="btn_save_pa"):
                if save_entire_sheet("PhanAnh", edited_pa): st.success("Lưu thành công!").rerun()

        with tab_vd:
            st.subheader("Quản lý Vinh Danh")
            edited_vd = st.data_editor(df_vd, num_rows="dynamic", key="editor_vd_free", use_container_width=True)
            if st.button("💾 Lưu thay đổi Vinh Danh", key="btn_save_vd"):
                if save_entire_sheet("VinhDanh", edited_vd): st.success("Lưu thành công!").rerun()

        with tab_cq:
            st.subheader("Quản lý Chợ Quê")
            edited_cq = st.data_editor(df_cq, num_rows="dynamic", key="editor_cq_free", use_container_width=True)
            if st.button("💾 Lưu thay đổi Chợ Quê", key="btn_save_cq"):
                if save_entire_sheet("ChoQue", edited_cq): st.success("Lưu thành công!").rerun()

        with tab_dl:
            st.subheader("Quản lý Đặt Lịch")
            edited_dl = st.data_editor(df_dl, num_rows="dynamic", key="editor_dl_free", use_container_width=True)
            if st.button("💾 Lưu thay đổi Đặt Lịch", key="btn_save_dl"):
                if save_entire_sheet("DatLichNhaVanHoa", edited_dl): st.success("Lưu thành công!").rerun()
