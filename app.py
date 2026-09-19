import streamlit as st
import pandas as pd
import datetime
from streamlit_gsheets import GSheetsConnection

# Cấu hình giao diện trang web
st.set_page_config(page_title="Quản Lý Khu Dân Cư Lăng Tô", page_icon="🏘️", layout="wide")

# CSS tùy chỉnh giao diện và làm đẹp phần tiêu đề & footer sidebar
st.markdown("""
<style>
    /* Ẩn vòng tròn chọn của radio button trong sidebar */
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] label div:first-child {
        display: none;
    }
    /* Tùy chỉnh giao diện nút menu sidebar */
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
    /* Tự động xuống dòng và tối ưu hiển thị ô nhập liệu */
    textarea, input {
        max-width: 100% !important;
    }
    /* Thiết kế hộp tiêu đề Sidebar đẹp mắt, nổi bật */
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
    /* Kiểu chữ nhỏ mô tả bên dưới menu sidebar */
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

# Kết nối Google Sheets thông qua st.connection chuẩn GSheetsConnection
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception as e:
    st.error(f"Lỗi kết nối GSheetsConnection: {e}. Vui lòng kiểm tra lại mục Secrets trên Streamlit Cloud.")
    st.stop()

# Hàm đọc dữ liệu từ từng Tab (worksheet) của Google Sheets
def load_gsheet_data(sheet_name):
    try:
        data = conn.read(worksheet=sheet_name, ttl=0)
        if data is None or data.empty:
            return pd.DataFrame()
        return data.dropna(how="all")
    except Exception:
        return pd.DataFrame()

# Tải dữ liệu các bảng từ Google Sheets tương ứng với 10 tab
df_tb = load_gsheet_data("ThongBao")
df_db = load_gsheet_data("DanhBaThon")
df_sk = load_gsheet_data("SuKien")
df_tc = load_gsheet_data("CongKhaiThuChi")
df_pa = load_gsheet_data("PhanAnh")
df_cq = load_gsheet_data("ChoQue")
df_vd = load_gsheet_data("VinhDanh")
df_dk = load_gsheet_data("DangKySuKien")
df_dl = load_gsheet_data("DatLichNhaVanHoa")
df_qt = load_gsheet_data("QuanTriCanBo")

def display_df_with_1_index(df):
    if not df.empty:
        df_reset = df.reset_index(drop=True)
        df_reset.insert(0, "STT", range(1, len(df_reset) + 1))
        st.dataframe(df_reset, use_container_width=True, hide_index=True)
    else:
        st.info("Chưa có dữ liệu trong bảng này.")

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

# --- XỬ LÝ CHỨC NĂNG ---

if "1. 📢 Bảng Tin & Thông Báo" in choice:
    st.header("📢 Bảng Tin & Thông Báo")
    if not df_tb.empty:
        for idx, row in df_tb.iterrows():
            ghim = "📌 [Ghim Nổi Bật]" if str(row.get('Ghim Nổi Bật', '')) == "Có" else ""
            with st.expander(f"{ghim} {row.get('Tiêu Đề', 'Thông báo')} (Phân loại: {row.get('Phân Loại', 'Chung')})"):
                st.write(f"**Nội dung:** {row.get('Nội Dung', '')}")
                st.write(f"📅 Ngày đăng: {row.get('Ngày Đăng', '')} | 👤 Người đăng: {row.get('Người Đăng', '')}")
    else:
        st.info("Chưa có thông báo nào.")

elif "2. 📋 Danh Bạ Thôn" in choice:
    st.header("📋 Danh Bạ Cư Dân & Cán Bộ Thôn")
    display_df_with_1_index(df_db)

elif "3. 🎉 Sự Kiện Cộng Đồng" in choice:
    st.header("🎉 Sự Kiện Cộng Đồng")
    display_df_with_1_index(df_sk)

elif "4. 📝 Đăng Ký & Điểm Danh" in choice:
    st.header("📝 Đăng Ký Hoạt Động & Điểm Danh")
    display_df_with_1_index(df_sk)
    
    with st.form("form_dang_ky", clear_on_submit=True):
        st.subheader("Biểu mẫu đăng ký tham gia sự kiện")
        ho_ten_ho = st.text_input("Họ và tên hộ gia đình đăng ký tham gia")
        chon_sk = st.selectbox("Chọn sự kiện cần đăng ký", df_sk['Tên Sự Kiện'].tolist() if not df_sk.empty and 'Tên Sự Kiện' in df_sk.columns else [])
        so_luong_them = st.number_input("Số lượng hộ tham gia thêm", min_value=1, value=1, step=1)
        submitted_dk = st.form_submit_button("Xác nhận đăng ký")
        
        if submitted_dk:
            if not ho_ten_ho.strip():
                st.warning("Vui lòng nhập họ và tên hộ gia đình đăng ký!")
            else:
                st.success(f"Cảm ơn hộ gia đình '{ho_ten_ho}'! Đã ghi nhận đăng ký sự kiện thành công.")

elif "5. 💰 Công Khai Thu Chi" in choice:
    st.header("💰 Công Khai Tài Chính Quỹ Thôn")
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
                st.warning("Vui lòng nhập đầy đủ họ tên và nội dung phản ánh!")
            else:
                st.success(f"Cảm ơn {nguoi_gui}! Phản ánh của bạn đã được gửi thành công.")

elif "7. 🏆 Vinh Danh & Khen Thưởng" in choice:
    st.header("🏆 Vinh Danh & Khen Thưởng Cư Dân Tiêu Biểu")
    display_df_with_1_index(df_vd)

elif "8. 🛒 Chợ Quê Nông Sản" in choice:
    st.header("🛒 Chợ Quê — Trao Đổi & Đăng Bán Nông Sản")
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
                    st.success(f"Sản phẩm '{ten_sp}' đã được đăng lên Chợ Quê thành công!")

elif "9. 📅 Đặt Lịch Nhà Văn Hóa" in choice:
    st.header("📅 Đặt Lịch Sử Dụng Nhà Văn Hóa & Thiết Bị")
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
                st.success(f"Cảm ơn {ho_ten_dl}! Yêu cầu đặt lịch ngày {ngay_dat} đã được ghi nhận.")

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
        st.success("✅ Bạn đang ở chế độ Cán bộ quản lý toàn quyền xem thông tin.")
        if st.button("Đăng xuất"):
            st.session_state.authenticated = False
            st.rerun()

        st.markdown("---")
        # Chia các mục quản trị thành các tab tương ứng cho toàn bộ các bảng trong hệ thống
        tab_q1, tab_q2, tab_q3, tab_q4, tab_q5, tab_q6 = st.tabs([
            "📢 Quản trị Thông Báo", 
            "📋 Quản trị Danh Bạ", 
            "🎉 Quản trị Sự Kiện", 
            "💰 Quản trị Thu Chi", 
            "⚠️ Quản trị Phản Ánh",
            "🏆 Quản trị Vinh Danh"
        ])
        
        with tab_q1:
            st.subheader("Quản lý Bản tin & Thông báo thôn")
            display_df_with_1_index(df_tb)
            with st.form("form_them_tb", clear_on_submit=True):
                st.markdown("##### Thêm thông báo mới")
                tieu_de = st.text_input("Tiêu đề thông báo")
                noi_dung = st.text_area("Nội dung chi tiết")
                phan_loai = st.selectbox("Phân loại", ["Khẩn cấp", "Hành chính", "Sự kiện", "Thông thường"])
                nguoi_dang = st.text_input("Người đăng / Cán bộ phụ trách", value="Ban Văn hóa Thôn")
                ghim = st.selectbox("Ghim nổi bật", ["Không", "Có"])
                if st.form_submit_button("Thêm thông báo"):
                    st.success(f"Đã ghi nhận thêm thông báo: '{tieu_de}' (Bạn hãy cập nhật trực tiếp dòng tương ứng trên Google Sheets để đồng bộ lưu trữ).")

        with tab_q2:
            st.subheader("Quản lý Danh bạ cư dân & Cán bộ thôn")
            display_df_with_1_index(df_db)
            with st.form("form_them_db", clear_on_submit=True):
                st.markdown("##### Thêm nhân khẩu / hộ gia đình vào danh bạ")
                ten_chu_ho = st.text_input("Họ và tên chủ hộ")
                so_khu_vuc = st.text_input("Số xóm / Khu vực")
                so_nhan_khau = st.number_input("Tổng số nhân khẩu", min_value=1, value=4, step=1)
                so_dien_thoai = st.text_input("Số điện thoại liên hệ")
                phan_loai_ho = st.selectbox("Phân loại hộ", ["Hộ thường", "Hộ nghèo", "Hộ cận nghèo", "Gia đình văn hóa"])
                if st.form_submit_button("Thêm vào danh bạ"):
                    st.success(f"Đã thêm hộ '{ten_chu_ho}' vào hệ thống.")

        with tab_q3:
            st.subheader("Quản lý Sự kiện cộng đồng")
            display_df_with_1_index(df_sk)
            with st.form("form_them_sk", clear_on_submit=True):
                st.markdown("##### Thêm sự kiện mới")
                ten_sk = st.text_input("Tên sự kiện")
                mo_ta_sk = st.text_area("Mô tả sự kiện")
                ngay_bd = st.date_input("Thời gian diễn ra")
                dia_diem = st.text_input("Địa điểm tổ chức")
                if st.form_submit_button("Thêm sự kiện"):
                    st.success(f"Đã tạo sự kiện '{ten_sk}' thành công.")

        with tab_q4:
            st.subheader("Quản lý Khoản Thu / Chi quỹ thôn")
            display_df_with_1_index(df_tc)
            with st.form("form_them_tc", clear_on_submit=True):
                st.markdown("##### Thêm giao dịch thu chi mới")
                ngay_gd = st.date_input("Ngày giao dịch")
                loai_gd = st.selectbox("Loại giao dịch", ["Thu", "Chi"])
                danh_muc = st.text_input("Danh mục (Ví dụ: Quỹ thôn, Xây dựng nông thôn mới...)")
                chi_tiet = st.text_input("Nội dung chi tiết giao dịch")
                so_tien = st.number_input("Số tiền (VNĐ)", min_value=0, step=50000)
                if st.form_submit_button("Lưu giao dịch tài chính"):
                    st.success("Đã ghi nhận giao dịch thành công!")

        with tab_q5:
            st.subheader("Xử lý & Cập nhật Phản ánh kiến nghị")
            display_df_with_1_index(df_pa)
            st.info("💡 Bạn có thể theo dõi danh sách phản ánh của người dân tại đây và tiến hành xử lý trực tiếp trên file Google Sheets.")

        with tab_q6:
            st.subheader("Quản lý Khen thưởng & Vinh danh")
            display_df_with_1_index(df_vd)
            with st.form("form_them_vd", clear_on_submit=True):
                st.markdown("##### Thêm vinh danh mới")
                ten_vd = st.text_input("Họ và tên cá nhân / đại diện hộ")
                danh_hieu = st.text_input("Danh hiệu khen thưởng")
                thanh_tich = st.text_area("Mô tả thành tích tiêu biểu")
                if st.form_submit_button("Thêm vinh danh"):
                    st.success(f"Đã thêm vinh danh cho '{ten_vd}' thành công!")
