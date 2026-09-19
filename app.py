import streamlit as st
import pandas as pd
import datetime
import openpyxl

# --- CẤU HÌNH TRANG WEB ---
st.set_page_config(
    page_title="Quản Lý Khu Dân Cư Lăng Tô", 
    page_icon="🏘️", 
    layout="wide"
)

# --- TÊN FILE EXCEL TRÊN GITHUB ---
EXCEL_FILE = "dulieu_langto.xlsx"

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

# --- HÀM ĐỌC & GHI DỮ LIỆU EXCEL THÔNG MINH ---
@st.cache_data(ttl=2)
def load_excel_data(sheet_name):
    try:
        xls = pd.ExcelFile(EXCEL_FILE)
        sheet_map = {s.lower(): s for s in xls.sheet_names}
        target_lower = sheet_name.lower()
        
        if target_lower in sheet_map:
            df = pd.read_excel(EXCEL_FILE, sheet_name=sheet_map[target_lower])
            if df is None or df.empty:
                return pd.DataFrame()
            return df.dropna(how="all")
        else:
            return pd.DataFrame()
    except Exception as e:
        return pd.DataFrame()

def save_entire_sheet(sheet_name, df_modified):
    """Hàm lưu toàn bộ bảng dữ liệu sau khi cán bộ sửa trực tiếp"""
    try:
        xls = pd.ExcelFile(EXCEL_FILE)
        sheet_map = {s.lower(): s for s in xls.sheet_names}
        actual_sheet_name = sheet_map.get(sheet_name.lower(), sheet_name)
        
        # Đọc tất cả các sheet khác để không bị mất khi ghi đè
        with pd.ExcelWriter(EXCEL_FILE, engine='openpyxl', mode='w') as writer:
            for s in xls.sheet_names:
                if s.lower() == sheet_name.lower():
                    df_modified.to_excel(writer, sheet_name=actual_sheet_name, index=False)
                else:
                    df_s = pd.read_excel(EXCEL_FILE, sheet_name=s)
                    df_s.to_excel(writer, sheet_name=s, index=False)
        st.cache_data.clear()
        return True
    except Exception as e:
        st.error(f"Lỗi khi lưu file Excel: {e}")
        return False

def save_row_to_excel(sheet_name, new_data_dict):
    try:
        xls = pd.ExcelFile(EXCEL_FILE)
        sheet_map = {s.lower(): s for s in xls.sheet_names}
        actual_sheet_name = sheet_map.get(sheet_name.lower(), sheet_name)
        
        df_current = pd.read_excel(EXCEL_FILE, sheet_name=actual_sheet_name)
        df_new = pd.DataFrame([new_data_dict])
        df_combined = pd.concat([df_current, df_new], ignore_index=True)
        
        return save_entire_sheet(sheet_name, df_combined)
    except Exception as e:
        st.error(f"Lỗi khi thêm dữ liệu: {e}")
        return False

def display_df_with_1_index(df):
    if not df.empty:
        df_reset = df.reset_index(drop=True)
        df_reset.insert(0, "STT", range(1, len(df_reset) + 1))
        st.dataframe(df_reset, use_container_width=True, hide_index=True)
    else:
        st.info("💡 Bảng này hiện chưa có dữ liệu hoặc tên tab trong file Excel không khớp.")

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
            if 'Số Lượng' not in df_sk_hien_thi.columns:
                df_sk_hien_thi['Số Lượng'] = 0
    else:
        df_sk_hien_thi = df_sk.copy()
        if not df_sk_hien_thi.empty and 'Số Lượng' not in df_sk_hien_thi.columns:
            df_sk_hien_thi['Số Lượng'] = 0

    st.subheader("📅 Danh sách sự kiện & Tổng hợp số lượng đăng ký tham gia")
    display_df_with_1_index(df_sk_hien_thi)
    
    with st.form("form_dang_ky", clear_on_submit=True):
        st.subheader("Biểu mẫu đăng ký tham gia sự kiện")
        ho_ten_ho = st.text_input("Họ và tên hộ gia đình / cá nhân đăng ký")
        list_sk = df_sk['Tên Sự Kiện'].tolist() if not df_sk.empty and 'Tên Sự Kiện' in df_sk.columns else []
        chon_sk = st.selectbox("Chọn sự kiện cần đăng ký", list_sk)
        so_luong_them = st.number_input("Số lượng tham gia", min_value=1, value=1, step=1)
        ghi_chu_dk = st.text_input("Ghi chú")
        submitted_dk = st.form_submit_button("Xác nhận đăng ký")
        
        if submitted_dk:
            if not ho_ten_ho.strip():
                st.warning("Vui lòng nhập họ và tên hộ gia đình đăng ký!")
            else:
                data_dang_ky = {
                    "Họ Tên": ho_ten_ho,
                    "Tên Sự Kiện": chon_sk,
                    "Số Lượng": so_luong_them,
                    "Ghi Chú": ghi_chu_dk,
                    "Ngày Đăng Ký": str(datetime.date.today())
                }
                if save_row_to_excel("DangKySuKien", data_dang_ky):
                    st.success(f"Cảm ơn hộ gia đình '{ho_ten_ho}'! Đã ghi nhận đăng ký thành công {so_luong_them} người tham gia.")
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
        st.success("✅ Bạn đang ở chế độ Quản lý toàn quyền. Bạn có thể sửa trực tiếp nội dung các bảng hoặc thêm mới bên dưới.")
        if st.button("Đăng xuất"):
            st.session_state.authenticated = False
            st.rerun()

        st.markdown("---")
        
        df_tb = load_excel_data("ThongBao")
        df_db = load_excel_data("DanhBaThon")
        df_sk = load_excel_data("SuKien")
        df_tc = load_excel_data("CongKhaiThuChi")
        df_pa = load_excel_data("PhanAnh")
        df_vd = load_excel_data("VinhDanh")

        tab_q1, tab_q2, tab_q3, tab_q4, tab_q5, tab_q6 = st.tabs([
            "📢 Quản trị Thông Báo", 
            "📋 Quản trị Danh Bạ", 
            "🎉 Quản trị Sự Kiện", 
            "💰 Quản trị Thu Chi", 
            "⚠️ Quản trị Phản Ánh",
            "🏆 Quản trị Vinh Danh"
        ])
        
        with tab_q1:
            st.subheader("Chỉnh sửa trực tiếp Thông Báo & Bản Tin")
            st.info("💡 Bạn có thể click trực tiếp vào các ô bên dưới để sửa chữ, thêm dòng hoặc xóa dòng, sau đó nhấn nút lưu.")
            edited_tb = st.data_editor(df_tb, num_rows="dynamic", key="editor_tb")
            if st.button("💾 Lưu thay đổi Thông Báo"):
                if save_entire_sheet("ThongBao", edited_tb):
                    st.success("Đã cập nhật và lưu thay đổi thông báo thành công!")
                    st.rerun()

        with tab_q2:
            st.subheader("Chỉnh sửa trực tiếp Danh Bạ Thôn")
            st.info("💡 Bạn có thể click trực tiếp vào các ô bên dưới để sửa thông tin nhân khẩu, chức vụ, số điện thoại hoặc xóa dòng.")
            edited_db = st.data_editor(df_db, num_rows="dynamic", key="editor_db")
            if st.button("💾 Lưu thay đổi Danh Bạ"):
                if save_entire_sheet("DanhBaThon", edited_db):
                    st.success("Đã cập nhật và lưu danh bạ thành công!")
                    st.rerun()

        with tab_q3:
            st.subheader("Quản lý Sự kiện cộng đồng")
            edited_sk = st.data_editor(df_sk, num_rows="dynamic", key="editor_sk")
            if st.button("💾 Lưu thay đổi Sự Kiện"):
                if save_entire_sheet("SuKien", edited_sk):
                    st.success("Đã cập nhật sự kiện thành công!")
                    st.rerun()

        with tab_q4:
            st.subheader("Quản lý Khoản Thu / Chi quỹ thôn")
            edited_tc = st.data_editor(df_tc, num_rows="dynamic", key="editor_tc")
            if st.button("💾 Lưu thay đổi Thu Chi"):
                if save_entire_sheet("CongKhaiThuChi", edited_tc):
                    st.success("Đã cập nhật thu chi thành công!")
                    st.rerun()

        with tab_q5:
            st.subheader("Xử lý & Cập nhật Phản ánh kiến nghị")
            edited_pa = st.data_editor(df_pa, num_rows="dynamic", key="editor_pa")
            if st.button("💾 Lưu thay đổi Phản Ánh"):
                if save_entire_sheet("PhanAnh", edited_pa):
                    st.success("Đã cập nhật phản ánh thành công!")
                    st.rerun()

        with tab_q6:
            st.subheader("Quản lý Khen thưởng & Vinh danh")
            edited_vd = st.data_editor(df_vd, num_rows="dynamic", key="editor_vd")
            if st.button("💾 Lưu thay đổi Vinh Danh"):
                if save_entire_sheet("VinhDanh", edited_vd):
                    st.success("Đã cập nhật vinh danh thành công!")
                    st.rerun()
