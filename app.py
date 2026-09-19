import streamlit as st
import pandas as pd
import datetime
import os
import openpyxl

# --- CẤU HÌNH TRANG WEB (TỐI ƯU GIAO DIỆN MOBILE APP) ---
st.set_page_config(
    page_title="Quản Lý Khu Dân Cư Lăng Tô", 
    page_icon="🏘️", 
    layout="centered"
)

# --- TÊN FILE EXCEL TRÊN GITHUB ---
EXCEL_FILE = "dulieu_langto.xlsx"

# --- KHỞI TẠO CẤU TRÚC CỘT CHUẨN CHO TỪNG SHEET ---
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

# --- CSS TÙY CHỈNH MOBILE APP & HIỆU ỨNG CHUYỂN TRANG MƯỢT MÀ ---
st.markdown("""
<style>
    /* Ẩn sidebar mặc định của Streamlit */
    [data-testid="stSidebar"] {
        display: none;
    }
    
    /* Thiết lập font chữ và nền tổng thể gọn gàng */
    html, body, [class*="css"] {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        background-color: #f8fafc;
    }

    /* Hiệu ứng chuyển trang / xuất hiện mượt mà (Fade In) */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(6px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .fade-in-container {
        animation: fadeIn 0.3s ease-in-out;
    }

    /* Header kiểu App Di Động thu gọn, tinh tế */
    .app-header {
        background: linear-gradient(135deg, #0284c7, #0369a1);
        padding: 16px 20px;
        border-radius: 0 0 16px 16px;
        text-align: center;
        color: white;
        margin: -1rem -1rem 1.2rem -1rem;
        box-shadow: 0 3px 10px rgba(2, 132, 199, 0.25);
    }
    .app-header h1 {
        margin: 0;
        font-size: 18px;
        font-weight: 700;
        letter-spacing: -0.3px;
    }
    .app-header p {
        margin: 3px 0 0 0;
        font-size: 11px;
        opacity: 0.9;
    }

    /* Nút bấm menu chính dạng thẻ thu gọn, thanh lịch */
    .stButton>button {
        width: 100% !important;
        border-radius: 10px !important;
        padding: 10px 12px !important;
        font-weight: 600 !important;
        font-size: 13px !important;
        background-color: #ffffff !important;
        color: #1e293b !important;
        border: 1px solid #e2e8f0 !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        text-align: left !important;
    }
    .stButton>button:hover {
        background-color: #f1f5f9 !important;
        border-color: #cbd5e1 !important;
        color: #0284c7 !important;
    }
    .stButton>button:active {
        transform: scale(0.97);
    }

    /* Tùy chỉnh riêng cho nút Quay lại hoặc xác nhận (Màu nổi bật) */
    div.row-widget.stButton:nth-of-type(1) button {
        background-color: #0284c7 !important;
        color: white !important;
        text-align: center !important;
    }

    /* Expander thu gọn, giao diện thẻ card sạch sẽ */
    .streamlit-expanderHeader {
        background-color: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-size: 13px !important;
        color: #1e293b !important;
        padding: 8px 12px !important;
        margin-bottom: 6px !important;
    }
    .streamlit-expanderHeader:hover {
        background-color: #f8fafc !important;
        border-color: #94a3b8 !important;
    }

    /* Chân trang */
    .app-footer {
        font-size: 10px;
        color: #64748b;
        text-align: center;
        padding: 20px 10px;
        line-height: 1.4;
        border-top: 1px dashed #cbd5e1;
        margin-top: 30px;
    }
</style>
""", unsafe_allow_html=True)

# --- HÀM LÀM SẠCH & CHUẨN HÓA CỘT EXCEL ---
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
            cols = DEFAULT_COLUMNS.get(sheet_name, [])
            return pd.DataFrame(columns=cols)
    except Exception:
        cols = DEFAULT_COLUMNS.get(sheet_name, [])
        return pd.DataFrame(columns=cols)

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
        st.error(f"Lỗi khi lưu file Excel: {e}")
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

# Hàm hiển thị dữ liệu dạng Thẻ (Cards) thu gọn
def display_mobile_cards(df, title_col, details_cols):
    df_clean = clean_dataframe(df, "")
    if df_clean.empty:
        st.info("💡 Hiện chưa có dữ liệu nào trong mục này.")
        return

    for idx, row in df_clean.iterrows():
        title_val = row.get(title_col, 'Chi tiết')
        with st.expander(f"📌 {title_val}"):
            for col in details_cols:
                val = row.get(col, '')
                if val and val != 'nan':
                    st.markdown(f"**{col}:** {val}")

# --- HÀM TÍNH TOÁN CỘNG DỒN TỰ ĐỘNG SỐ LƯỢNG ĐĂNG KÝ ---
def get_updated_events_df():
    df_sk = load_excel_data("SuKien")
    df_dk = load_excel_data("DangKySuKien")
    if df_sk.empty:
        return df_sk
    df_sk_calc = df_sk.copy()
    if not df_dk.empty and 'Tên Sự Kiện' in df_dk.columns:
        if 'Số Lượng' in df_dk.columns:
            df_dk['Số Lượng_num'] = pd.to_numeric(df_dk['Số Lượng'], errors='coerce').fillna(1)
        else:
            df_dk['Số Lượng_num'] = 1
        sum_dk = df_dk.groupby('Tên Sự Kiện')['Số Lượng_num'].sum().reset_index()
        for idx, row in df_sk_calc.iterrows():
            ten_sk = row.get('Tên Sự Kiện', '')
            matched = sum_dk[sum_dk['Tên Sự Kiện'].str.strip() == ten_sk.strip()]
            if not matched.empty:
                df_sk_calc.loc[idx, 'Tổng Số Hộ Tham Gia'] = str(int(matched['Số Lượng_num'].values[0]))
            else:
                current_val = str(row.get('Tổng Số Hộ Tham Gia', ''))
                if current_val in ['', 'nan', 'None']:
                    df_sk_calc.loc[idx, 'Tổng Số Hộ Tham Gia'] = '0'
    else:
        for idx, row in df_sk_calc.iterrows():
            current_val = str(row.get('Tổng Số Hộ Tham Gia', ''))
            if current_val in ['', 'nan', 'None']:
                df_sk_calc.loc[idx, 'Tổng Số Hộ Tham Gia'] = '0'
    return df_sk_calc

# --- GIAO DIỆN APP HEADER ---
st.markdown("""
    <div class="app-header">
        <h1>🏘️ Quản Lý Khu Dân Cư Lăng Tô</h1>
        <p>Ứng dụng số hóa cộng đồng thông minh</p>
    </div>
""", unsafe_allow_html=True)

# --- QUẢN LÝ TRẠNG THÁI CHUYỂN TAB TRÊN MOBILE ---
if "active_tab" not in st.session_state:
    st.session_state.active_tab = "Trang chủ"

# Nút quay lại trang chủ nếu đang ở màn hình khác kèm hiệu ứng chuyển trang
if st.session_state.active_tab != "Trang chủ":
    if st.button("⬅️ Quay lại Menu chính"):
        st.session_state.active_tab = "Trang chủ"
        st.rerun()

# Bọc toàn bộ nội dung chuyển trang trong khung container có hiệu ứng Fade-in mượt mà
with st.container():
    st.markdown('<div class="fade-in-container">', unsafe_allow_html=True)
    
    # --- MÀN HÌNH CHÍNH (MENU LƯỚI 2 CỘT THU GỌN) ---
    if st.session_state.active_tab == "Trang chủ":
        st.markdown("##### 📱 Chọn chức năng sử dụng:")
        
        col1, col2 = st.columns(2)
        
        menu_items = [
            ("📢 Bảng Tin", "1. 📢 Bảng Tin & Thông Báo"),
            ("📋 Danh Bạ", "2. 📋 Danh Bạ Thôn"),
            ("🎉 Sự Kiện", "3. 🎉 Sự Kiện Cộng Đồng"),
            ("📝 Đăng Ký", "4. 📝 Đăng Ký & Điểm Danh"),
            ("💰 Thu Chi", "5. 💰 Công Khai Thu Chi"),
            ("⚠️ Phản Ánh", "6. ⚠️ Phản Ánh & Kiến Nghị"),
            ("🏆 Vinh Danh", "7. 🏆 Vinh Danh & Khen Thưởng"),
            ("🛒 Chợ Quê", "8. 🛒 Chợ Quê Nông Sản"),
            ("📅 Đặt Lịch", "9. 📅 Đặt Lịch Nhà Văn Hóa"),
            ("🔐 Quản Trị", "10. 🛠️ Khu Vực Quản Trị Cán Bộ")
        ]
        
        for i, (title, key) in enumerate(menu_items):
            with (col1 if i % 2 == 0 else col2):
                if st.button(title, key=f"btn_menu_{i}"):
                    st.session_state.active_tab = key
                    st.rerun()

    # --- XỬ LÝ NỘI DUNG CÁC MỤC ---
    elif st.session_state.active_tab == "1. 📢 Bảng Tin & Thông Báo":
        st.markdown("### 📢 Bảng Tin & Thông Báo")
        df_tb = load_excel_data("ThongBao")
        if not df_tb.empty:
            for idx, row in df_tb.iterrows():
                ghim = "🔥 [Nổi bật]" if str(row.get('Ghim Nổi Bật', '')) == "Có" else ""
                with st.expander(f"{ghim} {row.get('Tiêu Đề', 'Thông báo')} ({row.get('Phân Loại', 'Chung')})"):
                    st.write("**Nội dung:**")
                    st.info(row.get('Nội Dung', ''))
                    st.caption(f"📅 Ngày đăng: {row.get('Ngày Đăng', '')} | 👤 Người đăng: {row.get('Người Đăng', '')}")
        else:
            st.info("Chưa có thông báo nào trong hệ thống.")

    elif st.session_state.active_tab == "2. 📋 Danh Bạ Thôn":
        st.markdown("### 📋 Danh Bạ Cán Bộ & Cư Dân")
        df_db = load_excel_data("DanhBaThon")
        display_mobile_cards(df_db, "Họ Tên", ["Chức Vụ", "Số Điện Thoại", "Cán Bộ"])

    elif st.session_state.active_tab == "3. 🎉 Sự Kiện Cộng Đồng":
        st.markdown("### 🎉 Sự Kiện Cộng Đồng")
        df_sk_hien_thi = get_updated_events_df()
        display_mobile_cards(df_sk_hien_thi, "Tên Sự Kiện", ["Mô Tả", "Thời Gian Bắt Đầu", "Địa Điểm", "Tổng Số Hộ Tham Gia"])

    elif st.session_state.active_tab == "4. 📝 Đăng Ký & Điểm Danh":
        st.markdown("### 📝 Đăng Ký Hoạt Động & Điểm Danh")
        df_sk = load_excel_data("SuKien")
        df_sk_hien_thi = get_updated_events_df()

        st.markdown("**Danh sách sự kiện hiện tại:**")
        display_mobile_cards(df_sk_hien_thi, "Tên Sự Kiện", ["Thời Gian Bắt Đầu", "Địa Điểm", "Tổng Số Hộ Tham Gia"])
        
        st.markdown("---")
        with st.form("form_dang_ky", clear_on_submit=True):
            st.markdown("**Biểu mẫu đăng ký tham gia sự kiện**")
            ho_ten_ho = st.text_input("Họ và tên hộ gia đình / cá nhân đăng ký")
            list_sk = df_sk['Tên Sự Kiện'].tolist() if not df_sk.empty and 'Tên Sự Kiện' in df_sk.columns else []
            chon_sk = st.selectbox("Chọn sự kiện cần đăng ký", list_sk if list_sk else ["Không có sự kiện"])
            so_luong_them = st.number_input("Số lượng tham gia", min_value=1, value=1, step=1)
            ghi_chu_dk = st.text_input("Ghi chú thêm")
            submitted_dk = st.form_submit_button("Xác nhận đăng ký")
            
            if submitted_dk:
                if not ho_ten_ho.strip() or not list_sk:
                    st.warning("Vui lòng nhập họ tên và chọn sự kiện hợp lệ!")
                else:
                    data_dang_ky = {
                        "Họ Tên": ho_ten_ho,
                        "Tên Sự Kiện": chon_sk,
                        "Số Lượng": str(so_luong_them),
                        "Ghi Chú": ghi_chu_dk,
                        "Ngày Đăng Ký": str(datetime.date.today())
                    }
                    if save_row_to_excel("DangKySuKien", data_dang_ky):
                        updated_sk_for_save = get_updated_events_df()
                        save_entire_sheet("SuKien", updated_sk_for_save)
                        st.success(f"Cảm ơn '{ho_ten_ho}' đã đăng ký thành công!")
                        st.rerun()

    elif st.session_state.active_tab == "5. 💰 Công Khai Thu Chi":
        st.markdown("### 💰 Công Khai Tài Chính Quỹ Thôn")
        df_tc = load_excel_data("CongKhaiThuChi")
        display_mobile_cards(df_tc, "Nội Dung", ["Ngày", "Thu (VNĐ)", "Chi (VNĐ)", "Ghi Chú"])

    elif st.session_state.active_tab == "6. ⚠️ Phản Ánh & Kiến Nghị":
        st.markdown("### ⚠️ Gửi Phản Ánh & Kiến Nghị")
        with st.form("form_phan_anh", clear_on_submit=True):
            nguoi_gui = st.text_input("Họ và tên của bạn")
            linh_vuc_pa = st.selectbox("Lĩnh vực phản ánh", ["Môi trường", "An ninh trật tự", "Hạ tầng / Đường xá", "Tranh chấp", "Khác"])
            noi_dung_pa = st.text_area("Nội dung chi tiết phản ánh / kiến nghị")
            vi_tri_pa = st.text_input("Khu vực / Địa điểm xảy ra vấn đề")
            submitted_pa = st.form_submit_button("Gửi phản ánh")
            if submitted_pa:
                if not nguoi_gui.strip() or not noi_dung_pa.strip():
                    st.warning("Vui lòng điền đầy đủ họ tên và nội dung!")
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
                        st.success("Phản ánh của bạn đã được gửi thành công đến Ban quản lý thôn!")

    elif st.session_state.active_tab == "7. 🏆 Vinh Danh & Khen Thưởng":
        st.markdown("### 🏆 Vinh Danh & Khen Thưởng")
        df_vd = load_excel_data("VinhDanh")
        display_mobile_cards(df_vd, "Họ Tên", ["Danh Hiệu", "Lý Do Khen Thưởng", "Năm"])

    elif st.session_state.active_tab == "8. 🛒 Chợ Quê Nông Sản":
        st.markdown("### 🛒 Chợ Quê Nông Sản")
        tab_xem, tab_dang = st.tabs(["🛍️ Xem sản phẩm", "➕ Đăng bán"])
        
        with tab_xem:
            df_cq = load_excel_data("ChoQue")
            display_mobile_cards(df_cq, "Tên Sản Phẩm", ["Phân Loại", "Giá Bán", "Đơn Vị", "Số Điện Thoại", "Ngày Đăng"])
            
        with tab_dang:
            with st.form("form_cho_que", clear_on_submit=True):
                ten_sp = st.text_input("Tên sản phẩm (Rau, củ, quả, gạo...)")
                phan_loai_sp = st.selectbox("Phân loại", ["Nông sản", "Thực phẩm", "Thủ công mỹ nghệ", "Đồ dùng gia đình"])
                gia_sp = st.number_input("Giá bán (VNĐ)", min_value=0, step=1000)
                don_vi_sp = st.text_input("Đơn vị tính (kg, bó, lít, con...)")
                sdt_lh = st.text_input("Số điện thoại liên hệ")
                submitted_cq = st.form_submit_button("Đăng bán ngay")
                
                if submitted_cq:
                    if not ten_sp.strip() or not sdt_lh.strip():
                        st.warning("Vui lòng điền tên sản phẩm và số điện thoại liên hệ!")
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
                            st.success("Sản phẩm đã được đăng lên chợ quê thành công!")
                            st.rerun()

    elif st.session_state.active_tab == "9. 📅 Đặt Lịch Nhà Văn Hóa":
        st.markdown("### 📅 Đặt Lịch Nhà Văn Hóa")
        df_dl = load_excel_data("DatLichNhaVanHoa")
        display_mobile_cards(df_dl, "Họ Tên", ["Dịch Vụ", "Ngày Sử Dụng", "Mục Đích", "Trạng Thái"])
        
        with st.form("form_dat_lich", clear_on_submit=True):
            ho_ten_dl = st.text_input("Họ và tên người đăng ký")
            dich_vu = st.selectbox("Loại dịch vụ", ["Mượn Nhà văn hóa", "Mượn bàn ghế / loa đài", "Đăng ký họp thôn"])
            ngay_dat = st.date_input("Ngày sử dụng")
            muc_dich = st.text_area("Mục đích sử dụng chi tiết")
            submitted_dl = st.form_submit_button("Gửi yêu cầu đặt lịch")
            if submitted_dl:
                if not ho_ten_dl.strip():
                    st.warning("Vui lòng nhập họ và tên người đăng ký!")
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

    elif st.session_state.active_tab == "10. 🛠️ Khu Vực Quản Trị Cán Bộ":
        st.markdown("### 🔐 Quản Trị Cán Bộ Thôn")
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
            st.success("✅ Đã đăng nhập quyền cán bộ.")
            if st.button("Đăng xuất quản trị"):
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
                "📢 Thông Báo", 
                "📋 Danh Bạ", 
                "🎉 Sự Kiện", 
                "💰 Thu Chi", 
                "⚠️ Phản Ánh",
                "🏆 Vinh Danh",
                "🛒 Chợ Quê",
                "📅 Đặt Lịch"
            ])
            
            with tab_tb:
                st.markdown("#### Quản lý Thông Báo")
                edited_tb = st.data_editor(df_tb, num_rows="dynamic", key="editor_tb_free", use_container_width=True)
                if st.button("💾 Lưu thay đổi", key="btn_save_tb"):
                    if save_entire_sheet("ThongBao", edited_tb):
                        st.success("Đã lưu thành công!")
                        st.rerun()

            with tab_db:
                st.markdown("#### Quản trị Danh Bạ")
                edited_db = st.data_editor(df_db, num_rows="dynamic", key="editor_db_free", use_container_width=True)
                if st.button("💾 Lưu thay đổi", key="btn_save_db"):
                    if save_entire_sheet("DanhBaThon", edited_db):
                        st.success("Đã lưu thành công!")
                        st.rerun()

            with tab_sk:
                st.markdown("#### Quản lý Sự Kiện")
                edited_sk = st.data_editor(df_sk, num_rows="dynamic", key="editor_sk_free", use_container_width=True)
                if st.button("💾 Lưu thay đổi", key="btn_save_sk"):
                    if save_entire_sheet("SuKien", edited_sk):
                        st.success("Đã lưu thành công!")
                        st.rerun()

            with tab_tc:
                st.markdown("#### Quản lý Thu Chi")
                edited_tc = st.data_editor(df_tc, num_rows="dynamic", key="editor_tc_free", use_container_width=True)
                if st.button("💾 Lưu thay đổi", key="btn_save_tc"):
                    if save_entire_sheet("CongKhaiThuChi", edited_tc):
                        st.success("Đã lưu thành công!")
                        st.rerun()

            with tab_pa:
                st.markdown("#### Quản lý Phản Ánh")
                edited_pa = st.data_editor(df_pa, num_rows="dynamic", key="editor_pa_free", use_container_width=True)
                if st.button("💾 Lưu thay đổi", key="btn_save_pa"):
                    if save_entire_sheet("PhanAnh", edited_pa):
                        st.success("Đã lưu thành công!")
                        st.rerun()

            with tab_vd:
                st.markdown("#### Quản lý Vinh Danh")
                edited_vd = st.data_editor(df_vd, num_rows="dynamic", key="editor_vd_free", use_container_width=True)
                if st.button("💾 Lưu thay đổi", key="btn_save_vd"):
                    if save_entire_sheet("VinhDanh", edited_vd):
                        st.success("Đã lưu thành công!")
                        st.rerun()

            with tab_cq:
                st.markdown("#### Quản lý Chợ Quê")
                edited_cq = st.data_editor(df_cq, num_rows="dynamic", key="editor_cq_free", use_container_width=True)
                if st.button("💾 Lưu thay đổi", key="btn_save_cq"):
                    if save_entire_sheet("ChoQue", edited_cq):
                        st.success("Đã lưu thành công!")
                        st.rerun()

            with tab_dl:
                st.markdown("#### Quản lý Đặt Lịch")
                edited_dl = st.data_editor(df_dl, num_rows="dynamic", key="editor_dl_free", use_container_width=True)
                if st.button("💾 Lưu thay đổi", key="btn_save_dl"):
                    if save_entire_sheet("DatLichNhaVanHoa", edited_dl):
                        st.success("Đã lưu thành công!")
                        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# --- CHÂN TRANG ỨNG DỤNG ---
st.markdown("""
    <div class="app-footer">
        Chương trình mục tiêu quốc gia xây dựng nông thôn mới, giảm nghèo bền vững<br>
        © 2026 Khu Dân Cư Lăng Tô
    </div>
""", unsafe_allow_html=True)
