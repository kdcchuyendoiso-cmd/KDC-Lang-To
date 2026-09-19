import streamlit as st
import pandas as pd
import datetime

# Cấu hình giao diện trang web
st.set_page_config(page_title="Quản Lý Khu Dân Cư Lăng Tô", page_icon="🏘️", layout="wide")

# CSS tùy chỉnh giao diện và làm đẹp phần tiêu đề sidebar
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
    /* Định cấu hình hiển thị số thứ tự bảng (index) bắt đầu từ 1 */
    tbody tr th:first-child {
        counter-increment: row-num;
    }
    tbody tr th:first-child::before {
        content: counter(row-num);
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
    /* Kiểu chữ nhỏ mô tả bên dưới menu sidebar - Đã thu nhỏ font-size xuống 9.5px */
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
# Khởi tạo dữ liệu vào session_state để lưu trữ sự thay đổi xuyên suốt các phiên tương tác
if "dfs" not in st.session_state:
    st.session_state.dfs = {
        "DanhBaThon": pd.DataFrame({
            "Họ và Tên": ["Nguyễn Văn An", "Trần Thị Bình", "Lê Văn Cường", "Phạm Thị Dung"],
            "Chức Vụ": ["Trưởng thôn", "Phó thôn", "Người dân", "Người dân"],
            "Số Điện Thoại": ["0912345678", "0987654321", "0901122334", "0933445566"],
            "Là Cán Bộ Thôn": ["Có", "Có", "Không", "Không"]
        }),
        "ThongBao": pd.DataFrame({
            "Tiêu Đề": ["Họp tổng kết cuối năm của thôn", "Lịch phun thuốc khử trùng khu dân cư"],
            "Nội Dung": ["Kính mời toàn thể bà con có mặt tại nhà văn hóa vào lúc 19h tối chủ nhật.", "Đề nghị các hộ gia đình dọn dẹp vệ sinh và đóng cửa sổ vào ngày mai."],
            "Phân Loại": ["Hành chính", "Khẩn cấp"],
            "Ngày Đăng": ["2026-06-01", "2026-06-05"],
            "Người Đăng": ["Nguyễn Văn An", "Trần Thị Bình"],
            "Ghim Nổi Bật": ["Có", "Không"]
        }),
        "SuKien": pd.DataFrame({
            "Tên Sự Kiện": ["Ngày hội Đại đoàn kết toàn dân tộc", "Giải bóng đá thanh niên thôn"],
            "Mô Tả": ["Tổ chức văn nghệ, thể thao và bữa cơm đoàn kết toàn thôn.", "Thi đấu giao lưu giữa các xóm trong thôn."],
            "Thời Gian Bắt Đầu": ["2026-11-18", "2026-09-02"],
            "Địa Điểm": ["Nhà văn hóa thôn", "Sân bóng khu thể thao"],
            "Tổng Số Hộ Tham Gia": [15, 8]
        }),
        "CongKhaiThuChi": pd.DataFrame({
            "Ngày": ["2026-05-10", "2026-05-15"],
            "Loại Giao Dịch": ["Thu", "Chi"],
            "Danh Mục": ["Quỹ thôn", "Sửa chữa đường điện"],
            "Nội Dung Chi Tiết": ["Đóng góp quỹ xây dựng nông thôn mới tháng 5", "Mua bóng đèn đường chiếu sáng"],
            "Số Tiền (VNĐ)": [15000000, 3500000]
        }),
        "PhanAnh": pd.DataFrame({
            "Người Phản Ánh": ["Lê Văn Cường", "Phạm Thị Dung"],
            "Ngày Phản Ánh": ["2026-06-02", "2026-06-04"],
            "Lĩnh Vực": ["Môi trường", "Hạ tầng / Đường xá"],
            "Nội Dung Phản Ánh": ["Rác thải ùn ứ tại khu vực ngã ba xóm 2.", "Bóng đèn đường ngõ số 4 bị hỏng tối qua."],
            "Vị Trí": ["Ngã ba xóm 2", "Ngõ số 4"],
            "Trạng Thái": ["Đang xử lý", "Đã tiếp nhận"]
        }),
        "ChoQue": pd.DataFrame({
            "Tên Sản Phẩm": ["Rau cải sạch nhà trồng", "Gạo nương Điện Biên chuẩn"],
            "Phân Loại": ["Nông sản", "Thực phẩm"],
            "Giá Bán": [15000, 30000],
            "Đơn Vị Tính": ["kg", "kg"],
            "Số Điện Thoại Liên Hệ": ["0901122334", "0933445566"]
        }),
        "VinhDanh": pd.DataFrame({
            "Họ và Tên": ["Nguyễn Văn An", "Lê Văn Cường"],
            "Danh Hiệu Khen Thưởng": ["Cán bộ thôn xuất sắc tiêu biểu", "Gia đình văn hóa tiêu biểu 2025"],
            "Mô Tả Thành Tích": ["Hoàn thành xuất sắc nhiệm vụ điều hành thôn.", "Gương sáng trong phong trào xây dựng nông thôn mới."]
        })
    }

dfs = st.session_state.dfs

# Hàm hiển thị số thứ tự bảng bắt đầu từ 1
def display_df_with_1_index(df):
    df_reset = df.reset_index(drop=True)
    df_reset.index = df_reset.index + 1
    st.dataframe(df_reset, use_container_width=True)

# --- THANH BÊN (SIDEBAR) ---
with st.sidebar:
    st.markdown("""
        <div class="sidebar-header-box">
            <h2>🏘️ Khu Dân Cư Lăng Tô</h2>
            <p> Quản lý và Kết nối cộng đồng (V1.0)</p>
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
    "10. 🛠️ Ban quản lý KDC"
]

choice = st.sidebar.radio("📌 Chọn Chức Năng", modules, label_visibility="collapsed")

# Bổ sung dòng chữ nhỏ mô tả chương trình mục tiêu quốc gia dưới mục số 10
st.sidebar.markdown("""
    <div class="sidebar-footer-note">
        Ứng dụng chuyển đổi số thực hiện Chương trình mục tiêu quốc gia xây dựng nông thôn mới, giảm nghèo bền vững và phát triển kinh tế - xã hội vùng đồng bào dân tộc thiểu số và miền núi giai đoạn 2026 - 2035.
    </div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")
# --- XỬ LÝ CHỨC NĂNG ---

# 1. BẢNG TIN & THÔNG BÁO
if "1. 📢 Bảng Tin & Thông Báo" in choice:
    st.header("📢 Bảng Tin & Thông Báo")
    df_tb = dfs.get("ThongBao")
    for idx, row in df_tb.iterrows():
        ghim = "📌 [Ghim Nổi Bật]" if str(row.get('Ghim Nổi Bật', '')) == "Có" else ""
        with st.expander(f"{ghim} {row.get('Tiêu Đề', 'Thông báo')} (Phân loại: {row.get('Phân Loại', 'Chung')})"):
            st.write(f"**Nội dung:** {row.get('Nội Dung', '')}")
            st.write(f"📅 Ngày đăng: {row.get('Ngày Đăng', '')} | 👤 Người đăng: {row.get('Người Đăng', '')}")

# 2. DANH BẠ THÔN
elif "2. 📋 Danh Bạ Thôn" in choice:
    st.header("📋 Danh Bạ Cư Dân & Cán Bộ Thôn")
    display_df_with_1_index(dfs.get("DanhBaThon"))

# 3. SỰ KIỆN CỘNG ĐỒNG
elif "3. 🎉 Sự Kiện Cộng Đồng" in choice:
    st.header("🎉 Sự Kiện Cộng Đồng")
    display_df_with_1_index(dfs.get("SuKien"))

# 4. ĐĂNG KÝ & ĐIỂM DANH
elif "4. 📝 Đăng Ký & Điểm Danh" in choice:
    st.header("📝 Đăng Ký Hoạt Động & Điểm Danh")
    st.info("Đăng ký tham gia các sự kiện, ngày hội đại đoàn kết, hệ thống sẽ tự động tổng hợp số lượng hộ tham gia.")
    
    df_sk = dfs.get("SuKien")
    st.subheader("Danh sách sự kiện và tổng hợp số hộ tham gia:")
    display_df_with_1_index(df_sk)
    
    with st.form("form_dang_ky", clear_on_submit=True):
        st.subheader("Biểu mẫu đăng ký tham gia sự kiện")
        ho_ten_ho = st.text_input("Họ và tên hộ gia đình đăng ký tham gia")
        chon_sk = st.selectbox("Chọn sự kiện cần đăng ký", df_sk['Tên Sự Kiện'].tolist() if 'Tên Sự Kiện' in df_sk.columns else [])
        so_luong_them = st.number_input("Số lượng hộ tham gia thêm", min_value=1, value=1, step=1)
        submitted_dk = st.form_submit_button("Xác nhận đăng ký")
        
        if submitted_dk:
            if not ho_ten_ho.strip():
                st.warning("Vui lòng nhập họ và tên hộ gia đình đăng ký!")
            else:
                idx_match = df_sk.index[df_sk['Tên Sự Kiện'] == chon_sk].tolist()
                if idx_match:
                    i = idx_match[0]
                    current_val = int(df_sk.loc[i, 'Tổng Số Hộ Tham Gia'])
                    df_sk.loc[i, 'Tổng Số Hộ Tham Gia'] = current_val + int(so_luong_them)
                    st.success(f"Cảm ơn hộ gia đình '{ho_ten_ho}'! Đã cập nhật thành công sự kiện '{chon_sk}' thêm {so_luong_them} hộ tham gia.")
                    st.rerun()

# 5. CÔNG KHAI THU CHI
elif "5. 💰 Công Khai Thu Chi" in choice:
    st.header("💰 Công Khai Tài Chính Quỹ Thôn")
    display_df_with_1_index(dfs.get("CongKhaiThuChi"))

# 6. PHẢN ÁNH & KIẾN NGHỊ
elif "6. ⚠️ Phản Ánh & Kiến Nghị" in choice:
    st.header("⚠️ Gửi Phản Ánh & Kiến Nghị Đến Cán Bộ Thôn")
    st.info("Phản ánh các vấn đề về môi trường, hạ tầng đường xá, an ninh trật tự tại khu dân cư.")
    
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
                new_pa = pd.DataFrame({
                    "Người Phản Ánh": [nguoi_gui],
                    "Ngày Phản Ánh": [str(datetime.date.today())],
                    "Lĩnh Vực": [linh_vuc_pa],
                    "Nội Dung Phản Ánh": [noi_dung_pa],
                    "Vị Trí": [vi_tri_pa if vi_tri_pa else "Không rõ"],
                    "Trạng Thái": ["Đã tiếp nhận"]
                })
                dfs["PhanAnh"] = pd.concat([dfs["PhanAnh"], new_pa], ignore_index=True)
                st.success(f"Cảm ơn {nguoi_gui}! Phản ánh của bạn đã được gửi thành công đến Cán bộ thôn để xử lý.")
                st.rerun()

# 7. VINH DANH & KHEN THƯỞNG
elif "7. 🏆 Vinh Danh & Khen Thưởng" in choice:
    st.header("🏆 Vinh Danh & Khen Thưởng Cư Dân Tiêu Biểu")
    display_df_with_1_index(dfs.get("VinhDanh"))

# 8. CHỢ QUÊ NÔNG SẢN
elif "8. 🛒 Chợ Quê Nông Sản" in choice:
    st.header("🛒 Chợ Quê — Trao Đổi & Đăng Bán Nông Sản")
    st.info("Nơi bà con đăng bán các sản phẩm nông sản sạch, đồ thủ công trong thôn.")
    
    tab_xem, tab_dang = st.tabs(["🛍️ Xem nông sản", "➕ Đăng bán sản phẩm"])
    with tab_xem:
        display_df_with_1_index(dfs.get("ChoQue"))
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
                    new_cq = pd.DataFrame({
                        "Tên Sản Phẩm": [ten_sp],
                        "Phân Loại": [phan_loai_sp],
                        "Giá Bán": [gia_sp],
                        "Đơn Vị Tính": [don_vi_sp if don_vi_sp else "cái"],
                        "Số Điện Thoại Liên Hệ": [sdt_lh]
                    })
                    dfs["ChoQue"] = pd.concat([dfs["ChoQue"], new_cq], ignore_index=True)
                    st.success(f"Sản phẩm '{ten_sp}' đã được đăng lên Chợ Quê thành công!")
                    st.rerun()

# 9. ĐẶT LỊCH NHÀ VĂN HÓA
elif "9. 📅 Đặt Lịch Nhà Văn Hóa" in choice:
    st.header("📅 Đặt Lịch Sử Dụng Nhà Văn Hóa & Thiết Bị")
    st.info("Đăng ký mượn nhà văn hóa tổ chức sự kiện gia đình hoặc mượn bàn ghế, loa đài.")
    
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
                st.success(f"Cảm ơn {ho_ten_dl}! Yêu cầu đặt lịch ngày {ngay_dat} của bạn đã được gửi và đang chờ Cán bộ thôn phê duyệt.")

# 10. Ban quản lý khu dân cư
elif "10. 🛠️ Ban quản lý KDC" in choice:
    st.header("🔐 Đăng Nhập")
    st.info("Khu vực dành riêng cho cán bộ quản lý đăng bài, duyệt phản ánh và quản lý thu chi.")
    
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
                    st.error("Mật khẩu không chính xác! Vui lòng thử lại.")
    else:
        st.success("✅ Bạn đang ở chế độ Cán bộ quản lý.")
        if st.button("Đăng xuất"):
            st.session_state.authenticated = False
            st.rerun()

        st.markdown("---")
        tab1, tab2, tab3 = st.tabs(["📢 Đăng thông báo mới", "💰 Cập nhật thu chi quỹ", "⚠️ Duyệt phản ánh"])
        
        with tab1:
            st.subheader("Tạo bản tin / Thông báo thôn mới")
            with st.form("form_them_tb", clear_on_submit=True):
                tieu_de = st.text_input("Tiêu đề thông báo")
                noi_dung = st.text_area("Nội dung chi tiết")
                phan_loai = st.selectbox("Phân loại", ["Khẩn cấp", "Hành chính", "Sự kiện", "Thông thường"])
                ghim = st.checkbox("Ghim nổi bật lên đầu bảng tin")
                submit_tb = st.form_submit_button("Đăng thông báo lên hệ thống")
                if submit_tb:
                    if not tieu_de.strip():
                        st.warning("Vui lòng nhập tiêu đề thông báo!")
                    else:
                        new_tb = pd.DataFrame({
                            "Tiêu Đề": [tieu_de],
                            "Nội Dung": [noi_dung],
                            "Phân Loại": [phan_loai],
                            "Ngày Đăng": [str(datetime.date.today())],
                            "Người Đăng": ["Cán bộ thôn"],
                            "Ghim Nổi Bật": ["Có" if ghim else "Không"]
                        })
                        dfs["ThongBao"] = pd.concat([new_tb, dfs["ThongBao"]], ignore_index=True)
                        st.success(f"Đã đăng thông báo thành công: '{tieu_de}'!")
                        st.rerun()

        with tab2:
            st.subheader("Thêm khoản thu / chi quỹ thôn")
            with st.form("form_them_tc", clear_on_submit=True):
                loai_gd = st.selectbox("Loại giao dịch", ["Thu", "Chi"])
                danh_muc = st.text_input("Danh mục (Ví dụ: Quỹ thôn, Hỗ trợ hộ nghèo...)")
                so_tien = st.number_input("Số tiền (VNĐ)", min_value=0, step=100000)
                nd_gd = st.text_input("Nội dung giao dịch chi tiết")
                submit_tc = st.form_submit_button("Lưu giao dịch tài chính")
                if submit_tc:
                    if not danh_muc.strip() or so_tien <= 0:
                        st.warning("Vui lòng nhập đầy đủ danh mục và số tiền hợp lệ!")
                    else:
                        new_tc = pd.DataFrame({
                            "Ngày": [str(datetime.date.today())],
                            "Loại Giao Dịch": [loai_gd],
                            "Danh Mục": [danh_muc],
                            "Nội Dung Chi Tiết": [nd_gd if nd_gd else "Không có mô tả"],
                            "Số Tiền (VNĐ)": [so_tien]
                        })
                        dfs["CongKhaiThuChi"] = pd.concat([dfs["CongKhaiThuChi"], new_tc], ignore_index=True)
                        st.success(f"Đã ghi nhận giao dịch {loai_gd} số tiền {so_tien:,.0f} VNĐ thành công!")
                        st.rerun()

        with tab3:
            st.subheader("Tiếp nhận và phản hồi kiến nghị dân cư")
            display_df_with_1_index(dfs.get("PhanAnh"))
            st.info("Danh sách phản ánh từ người dân hiển thị ở trên. Bạn có thể theo dõi trực tiếp trạng thái xử lý.")