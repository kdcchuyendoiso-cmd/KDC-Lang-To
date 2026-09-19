import streamlit as st
import pandas as pd
import datetime
import os
import openpyxl

# --- CẤU HÌNH TRANG WEB ---
st.set_page_config(
    page_title="Quản Lý Khu Dân Cư Lăng Tô", 
    page_icon="🏘️", 
    layout="wide"
)

# --- TÊN FILE EXCEL TRÊN GITHUB ---
EXCEL_FILE = "dulieu_langto.xlsx"

# --- KHỞI TẠO FILE EXCEL AN TOÀN NẾU CHƯA CÓ HOẶC THIẾU SHEET ---
DEFAULT_SHEETS = {
    "ThongBao": pd.DataFrame(columns=["Tiêu Đề", "Nội Dung", "Phân Loại", "Ngày Đăng", "Người Đăng", "Ghim Nổi Bật"]),
    "DanhBaThon": pd.DataFrame(columns=["Họ Tên", "Chức Vụ", "Số Điện Thoại", "Cán Bộ"]),
    "SuKien": pd.DataFrame(columns=["Tên Sự Kiện", "Mô Tả", "Thời Gian Bắt Đầu", "Địa Điểm", "Tổng Số Hộ Tham Gia"]),
    "DangKySuKien": pd.DataFrame(columns=["Họ Tên", "Tên Sự Kiện", "Số Lượng", "Ghi Chú", "Ngày Đăng Ký"]),
    "CongKhaiThuChi": pd.DataFrame(columns=["Ngày", "Nội Dung", "Thu (VNĐ)", "Chi (VNĐ)", "Ghi Chú"]),
    "PhanAnh": pd.DataFrame(columns=["Người Gửi", "Lĩnh Vực", "Nội Dung", "Địa Điểm", "Ngày Gửi", "Trạng Thái"]),
    "VinhDanh": pd.DataFrame(columns=["Họ Tên", "Danh Hiệu", "Lý Do Khen Thưởng", "Năm"]),
    "ChoQue": pd.DataFrame(columns=["Tên Sản Phẩm", "Phân Loại", "Giá Bán", "Đơn Vị", "Số Điện Thoại", "Ngày Đăng"]),
    "DatLichNhaVanHoa": pd.DataFrame(columns=["Họ Tên", "Dịch Vụ", "Ngày Sử Dụng", "Mục Đích", "Trạng Thái"])
}

def init_excel_file():
    if not os.path.exists(EXCEL_FILE):
        with pd.ExcelWriter(EXCEL_FILE, engine='openpyxl') as writer:
            for sheet, df in DEFAULT_SHEETS.items():
                df.to_excel(writer, sheet_name=sheet, index=False)
    else:
        # Kiểm tra xem thiếu sheet nào thì bổ sung sheet đó
        try:
            xls = pd.ExcelFile(EXCEL_FILE)
            existing_sheets = [s.lower() for s in xls.sheet_names]
            with pd.ExcelWriter(EXCEL_FILE, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
                for sheet, df in DEFAULT_SHEETS.items():
                    if sheet.lower() not in existing_sheets:
                        df.to_excel(writer, sheet_name=sheet, index=False)
        except Exception:
            pass

init_excel_file()

# --- CSS TÙY CHỈNH GIAO DIỆN ---
st.markdown("""
<style>
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] label div:first-child {
        display: none;
    }
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] label {
        background-color: transparent;
        padding: 10px 14px;
        border-radius: 8px;
        margin-bottom: 6px;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:hover {
        background-color: rgba(0, 123, 255, 0.1);
    }
    textarea, input {
        max-width: 100% !important;
    }
    .sidebar-header-box {
        background: linear-gradient(135deg, #007bff, #00d2ff);
        padding: 16px;
        border-radius: 12px;
        text-align: center;
        color: white;
        margin-bottom: 15px;
        box-shadow: 0 4px 10px rgba(0, 123, 255, 0.2);
    }
    .sidebar-header-box h2 {
        margin: 0;
        font-size: 19px;
        font-weight: 700;
        letter-spacing: 0.5px;
    }
    .sidebar-header-box p {
        margin: 5px 0 0 0;
        font-size: 12px;
        opacity: 0.9;
    }
    .sidebar-footer-note {
        font-size: 9.5px;
        color: #6c757d;
        text-align: justify;
        line-height: 1.35;
        padding: 8px 4px;
        margin-top: 8px;
        border-top: 1px dashed #dee2e6;
    }
</style>
""", unsafe_allow_html=True)

# --- HÀM LÀM SẠCH & ĐỌC DỮ LIỆU EXCEL AN TOÀN ---
def clean_dataframe(df):
    if df is None or df.empty:
        return pd.DataFrame()
    df = df.loc[:, ~df.columns.astype(str).str.contains('Unnamed|none|nan', case=False, na=False)]
    df = df.dropna(how="all")
    for col in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            df[col] = df[col].dt.strftime('%Y-%m-%d')
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
            df = pd.read_excel(EXCEL_FILE, sheet_name=sheet_map[target_lower])
            df_clean = clean_dataframe(df)
            if df_clean.empty and sheet_name in DEFAULT_SHEETS:
                return DEFAULT_SHEETS[sheet_name].copy()
            return df_clean
        else:
            return DEFAULT_SHEETS.get(sheet_name, pd.DataFrame()).copy()
    except Exception as e:
        return DEFAULT_SHEETS.get(sheet_name, pd.DataFrame()).copy()

def save_entire_sheet(sheet_name, df_modified):
    try:
        df_modified = clean_dataframe(df_modified)
        init_excel_file()
        xls = pd.ExcelFile(EXCEL_FILE)
        sheet_map = {s.lower(): s for s in xls.sheet_names}
        actual_sheet_name = sheet_map.get(sheet_name.lower(), sheet_name)
        
        all_dfs = {}
        for s in xls.sheet_names:
            if s.lower() == sheet_name.lower():
                all_dfs[actual_sheet_name] = df_modified
            else:
                df_s = pd.read_excel(EXCEL_FILE, sheet_name=s)
                all_dfs[s] = clean_dataframe(df_s)
                
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
        return save_entire_sheet(sheet_name, df_combined)
    except Exception as e:
        st.error(f"Lỗi khi thêm dữ liệu: {e}")
        return False

def display_df_with_1_index(df):
    df_clean = clean_dataframe(df)
    if not df_clean.empty:
        df_reset = df_clean.reset_index(drop=True)
        df_reset.insert(0, "STT", range(1, len(df_reset) + 1))
        st.dataframe(df_reset, use_container_width=True, hide_index=True)
    else:
        st.info("💡 Bảng này hiện chưa có dữ liệu.")

def safe_int(val, default=0):
    try:
        if pd.isna(val):
            return default
        return int(float(val))
    except:
        return default

# --- THANH BÊN (SIDEBAR) ---
with st.sidebar:
    st.markdown("""
        <div class="sidebar-header-box">
            <h2>🏘️ Quản Lý Khu Dân Cư Lăng Tô</h2>
            <p>Hệ thống Quản lý & Kết nối cộng đồng</p>
        </div>
    """, unsafe_allow_html=True)

modules = [
    "1. 📢 Bảng Tin & Thông Báo",
    "2. 📋 Danh Bạ Thôn",
    "3. 🎉 Sự Kiện Cộng Đồng",
    "4. 📝 Đăng Ký & Điểm Danh",
    "5. 💰 Công Khai Thu Chi",
    "6. ⚠️ Phản Ánh & Kiến Nghị",
    "7. 🏆 Vinh Danh & Khen Thưởng",
    "8. 🛒 Chợ Quê Nông Sản",
    "9. 📅 Đặt Lịch Nhà Văn Hóa",
    "10. 🛠️ Khu Vực Quản Trị Cán Bộ"
]

choice = st.sidebar.radio("📌 Chọn Chức Năng", modules, label_visibility="collapsed")

st.sidebar.markdown("""
    <div class="sidebar-footer-note">
        Ứng dụng chuyển đổi số thực hiện Chương trình mục tiêu quốc gia xây dựng nông thôn mới, giảm nghèo bền vững và phát triển kinh tế - xã hội vùng đồng bào dân tộc thiểu số và miền núi giai đoạn 2026 - 2035.
    </div>
""", unsafe_allow_html=True)
st.sidebar.markdown("---")

# --- XỬ LÝ GIAO DIỆN CÁC CHỨC NĂNG ---

if "1. 📢 Bảng Tin & Thông Báo" in choice:
    st.header("📢 Bảng Tin & Thông Báo")
    df_tb = load_excel_data("ThongBao")
    if not df_tb.empty:
        for idx, row in df_tb.iterrows():
            ghim = "📌 [Ghim Nổi Bật]" if str(row.get('Ghim Nổi Bật', '')) == "Có" else ""
            with st.expander(f"{ghim} {row.get('Tiêu Đề', 'Thông báo')} (Phân loại: {row.get('Phân Loại', 'Chung')})"):
                st.write(f"**Nội dung:** {row.get('Nội Dung', '')}")
                st.write(f"📅 Ngày đăng: {row.get('Ngày Đăng', '')} | 👤 Người đăng: {row.get('Người Đăng', '')}")
    else:
        st.info("Chưa có thông báo nào trong hệ thống.")

elif "2. 📋 Danh Bạ Thôn" in choice:
    st.header("📋 Danh Bạ Cư Dân & Cán Bộ Thôn")
    df_db = load_excel_data("DanhBaThon")
    display_df_with_1_index(df_db)

elif "3. 🎉 Sự Kiện Cộng Đồng" in choice:
    st.header("🎉 Sự Kiện Cộng Đồng")
    df_sk = load_excel_data("SuKien")
    display_df_with_1_index(df_sk)

elif "4. 📝 Đăng Ký & Điểm Danh" in choice:
    st.header("📝 Đăng Ký Hoạt Động & Điểm Danh")
    df_sk = load_excel_data("SuKien")
    df_dk = load_excel_data("DangKySuKien")
    
    if not df_sk.empty and not df_dk.empty:
        if 'Tên Sự Kiện' in df_dk.columns and 'Số Lượng' in df_dk.columns:
            tong_hop = df_dk.groupby('Tên Sự Kiện')['Số Lượng'].sum().reset_index()
            df_sk_hien_thi = pd.merge(df_sk, tong_hop, on='Tên Sự Kiện', how='left')
            df_sk_hien_thi['Số Lượng'] = df_sk_hien_thi['Số Lượng'].fillna(0).astype(int)
        else:
            df_sk_hien_thi = df_sk.copy()
            df_sk_hien_thi['Số Lượng'] = 0
    else:
        df_sk_hien_thi = df_sk.copy()
        if not df_sk_hien_thi.empty:
            df_sk_hien_thi['Số Lượng'] = 0

    st.subheader("📅 Danh sách sự kiện & Tổng hợp số lượng đăng ký tham gia")
    display_df_with_1_index(df_sk_hien_thi)
    
    with st.form("form_dang_ky", clear_on_submit=True):
        st.subheader("Biểu mẫu đăng ký tham gia sự kiện")
        ho_ten_ho = st.text_input("Họ và tên hộ gia đình / cá nhân đăng ký")
        list_sk = df_sk['Tên Sự Kiện'].tolist() if not df_sk.empty and 'Tên Sự Kiện' in df_sk.columns else []
        chon_sk = st.selectbox("Chọn sự kiện cần đăng ký", list_sk if list_sk else ["Không có sự kiện"])
        so_luong_them = st.number_input("Số lượng tham gia", min_value=1, value=1, step=1)
        ghi_chu_dk = st.text_input("Ghi chú")
        submitted_dk = st.form_submit_button("Xác nhận đăng ký")
        
        if submitted_dk:
            if not ho_ten_ho.strip() or not list_sk:
                st.warning("Vui lòng nhập họ tên và đảm bảo có sự kiện để đăng ký!")
            else:
                data_dang_ky = {
                    "Họ Tên": ho_ten_ho,
                    "Tên Sự Kiện": chon_sk,
                    "Số Lượng": so_luong_them,
                    "Ghi Chú": ghi_chu_dk,
                    "Ngày Đăng Ký": str(datetime.date.today())
                }
                if save_row_to_excel("DangKySuKien", data_dang_ky):
                    st.success(f"Cảm ơn hộ gia đình '{ho_ten_ho}'! Đã ghi nhận đăng ký thành công.")
                    st.rerun()

elif "5. 💰 Công Khai Thu Chi" in choice:
    st.header("💰 Công Khai Tài Chính Quỹ Thôn")
    df_tc = load_excel_data("CongKhaiThuChi")
    display_df_with_1_index(df_tc)

elif "6. ⚠️ Phản Ánh & Kiến Nghị" in choice:
    st.header("⚠️ Gửi Phản Ánh & Kiến Nghị Đến Cán Bộ Thôn")
    with st.form("form_phan_anh", clear_on_submit=True):
        nguoi_gui = st.text_input("Họ và tên của bạn")
        linh_vuc_pa = st.selectbox("Lĩnh vực phản ánh", ["Môi trường", "An ninh trật tự", "Hạ tầng / Đường xá", "Tranh chấp", "Khác"])
        noi_dung_pa = st.text_area("Nội dung chi tiết phản ánh / kiến nghị")
        vi_tri_pa = st.text_input("Khu vực / Địa điểm xảy ra vấn đề")
        submitted_pa = st.form_submit_button("Gửi phản ánh")
        if submitted_pa:
            if not nguoi_gui.strip() or not noi_dung_pa.strip():
                st.warning("Vui lòng điền đầy đủ họ tên và nội dung phản ánh!")
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
                    st.success(f"Cảm ơn {nguoi_gui}! Phản ánh của bạn đã được gửi thành công.")

elif "7. 🏆 Vinh Danh & Khen Thưởng" in choice:
    st.header("🏆 Vinh Danh & Khen Thưởng Cư Dân Tiêu Biểu")
    df_vd = load_excel_data("VinhDanh")
    display_df_with_1_index(df_vd)

elif "8. 🛒 Chợ Quê Nông Sản" in choice:
    st.header("🛒 Chợ Quê — Trao Đổi & Đăng Bán Nông Sản")
    df_cq = load_excel_data("ChoQue")
    tab_xem, tab_dang = st.tabs(["🛍️ Xem nông sản", "➕ Đăng bán sản phẩm"])
    with tab_xem:
        display_df_with_1_index(df_cq)
    with tab_dang:
        with st.form("form_cho_que", clear_on_submit=True):
            ten_sp = st.text_input("Tên sản phẩm (Ví dụ: Rau cải sạch, Gạo nương...)")
            phan_loai_sp = st.selectbox("Phân loại", ["Nông sản", "Thực phẩm", "Thủ công mỹ nghệ", "Đồ dùng gia đình"])
            gia_sp = st.number_input("Giá bán (VNĐ)", min_value=0, step=1000)
            don_vi_sp = st.text_input("Đơn vị tính (kg, bó, lít, con...)")
            sdt_lh = st.text_input("Số điện thoại liên hệ")
            submitted_cq = st.form_submit_button("Đăng bán sản phẩm")
            if submitted_cq:
                if not ten_sp.strip() or not sdt_lh.strip():
                    st.warning("Vui lòng điền tên sản phẩm và số điện thoại liên hệ!")
                else:
                    data_cq = {
                        "Tên Sản Phẩm": ten_sp,
                        "Phân Loại": phan_loai_sp,
                        "Giá Bán": gia_sp,
                        "Đơn Vị": don_vi_sp,
                        "Số Điện Thoại": sdt_lh,
                        "Ngày Đăng": str(datetime.date.today())
                    }
                    if save_row_to_excel("ChoQue", data_cq):
                        st.success(f"Sản phẩm '{ten_sp}' đã được đăng lên Chợ Quê thành công!")

elif "9. 📅 Đặt Lịch Nhà Văn Hóa" in choice:
    st.header("📅 Đặt Lịch Sử Dụng Nhà Văn Hóa & Thiết Bị")
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
                    st.success(f"Cảm ơn {ho_ten_dl}! Yêu cầu đặt lịch đã được gửi.")

elif "10. 🛠️ Khu Vực Quản Trị Cán Bộ" in choice:
    st.header("🔐 Đăng Nhập Khu Vực Quản Trị Cán Bộ Thôn")
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
        st.success("✅ Cán bộ đã đăng nhập thành công. Bạn có thể chỉnh sửa trực tiếp dữ liệu bên dưới bằng bảng hoặc các biểu mẫu.")
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

        tab_q3, tab_q1, tab_q2, tab_q4, tab_q5, tab_q6, tab_q7 = st.tabs([
            "🎉 Quản trị Sự Kiện", 
            "📢 Đăng & Sửa Thông Báo", 
            "📋 Quản trị Danh Bạ Thôn", 
            "💰 Quản trị Thu Chi", 
            "⚠️ Xử lý Phản Ánh",
            "🏆 Quản trị Vinh Danh",
            "📅 Đặt Lịch & Chợ Quê"
        ])
        
        # TAB 3: SỰ KIỆN
        with tab_q3:
            st.subheader("🎉 Quản lý & Cập nhật Sự Kiện Cộng Đồng")
            edited_sk = st.data_editor(df_sk, num_rows="dynamic", key="editor_sk_full", use_container_width=True)
            if st.button("💾 Lưu thay đổi Sự Kiện"):
                if save_entire_sheet("SuKien", edited_sk):
                    st.success("Đã lưu sự kiện thành công!")
                    st.rerun()

        # TAB 1: THÔNG BÁO
        with tab_q1:
            st.subheader("📢 Quản lý Bảng Tin & Thông Báo")
            edited_tb = st.data_editor(df_tb, num_rows="dynamic", key="editor_tb_full", use_container_width=True)
            if st.button("💾 Lưu thay đổi Thông Báo"):
                if save_entire_sheet("ThongBao", edited_tb):
                    st.success("Đã lưu thông báo thành công!")
                    st.rerun()

        # TAB 2: DANH BẠ THÔN
        with tab_q2:
            st.subheader("📋 Quản trị Danh Bạ Thôn")
            edited_db = st.data_editor(df_db, num_rows="dynamic", key="editor_db_full", use_container_width=True)
            if st.button("💾 Lưu thay đổi Danh Bạ"):
                if save_entire_sheet("DanhBaThon", edited_db):
                    st.success("Đã lưu danh bạ thành công!")
                    st.rerun()

        # TAB 4: THU CHI
        with tab_q4:
            st.subheader("💰 Quản lý Quỹ Thôn & Thu Chi")
            edited_tc = st.data_editor(df_tc, num_rows="dynamic", key="editor_tc_full", use_container_width=True)
            if st.button("💾 Lưu thay đổi Thu Chi"):
                if save_entire_sheet("CongKhaiThuChi", edited_tc):
                    st.success("Đã lưu Thu Chi thành công!")
                    st.rerun()

        # TAB 5: PHẢN ÁNH
        with tab_q5:
            st.subheader("⚠️ Xử lý Phản Ánh Kiến Nghị")
            edited_pa = st.data_editor(df_pa, num_rows="dynamic", key="editor_pa_full", use_container_width=True)
            if st.button("💾 Lưu thay đổi Phản Ánh"):
                if save_entire_sheet("PhanAnh", edited_pa):
                    st.success("Đã lưu Phản Ánh thành công!")
                    st.rerun()

        # TAB 6: VINH DANH
        with tab_q6:
            st.subheader("🏆 Quản lý Vinh Danh & Khen Thưởng")
            edited_vd = st.data_editor(df_vd, num_rows="dynamic", key="editor_vd_full", use_container_width=True)
            if st.button("💾 Lưu thay đổi Vinh Danh"):
                if save_entire_sheet("VinhDanh", edited_vd):
                    st.success("Đã lưu Vinh Danh thành công!")
                    st.rerun()

        # TAB 7: ĐẶT LỊCH & CHỢ QUÊ
        with tab_q7:
            st.subheader("📅 Quản lý Đặt Lịch Nhà Văn Hóa")
            edited_dl = st.data_editor(df_dl, num_rows="dynamic", key="editor_dl_full", use_container_width=True)
            if st.button("💾 Lưu thay đổi Đặt Lịch"):
                save_entire_sheet("DatLichNhaVanHoa", edited_dl)
                st.success("Đã lưu Đặt Lịch thành công!")
            
            st.markdown("---")
            st.markdown("##### 🛒 Quản lý Chợ Quê Nông Sản")
            edited_cq = st.data_editor(df_cq, num_rows="dynamic", key="editor_cq_full", use_container_width=True)
            if st.button("💾 Lưu thay đổi Chợ Quê"):
                save_entire_sheet("ChoQue", edited_cq)
                st.success("Đã lưu Chợ Quê thành công!")
