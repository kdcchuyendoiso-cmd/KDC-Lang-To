import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# 1. Cấu hình giao diện trang web
st.set_page_config(
    page_title="Chuyển Đổi Số Khu Dân Cư Lăng Tô",
    page_icon="🏡",
    layout="wide"
)

# 2. Khởi tạo kết nối Google Sheets an toàn
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception as e:
    st.error(f"Lỗi kết nối GSheetsConnection: {e}. Vui lòng kiểm tra lại mục Secrets trên Streamlit Cloud.")
    st.stop()

# 3. Hàm đọc dữ liệu từ từng Tab (worksheet)
def load_gsheet_data(sheet_name):
    try:
        data = conn.read(worksheet=sheet_name, ttl=0)
        if data is None or data.empty:
            return pd.DataFrame()
        return data.dropna(how="all")
    except Exception as e:
        st.warning(f"Không thể tải dữ liệu từ tab '{sheet_name}': {e}")
        return pd.DataFrame()

# 4. Danh sách 10 Tab chuẩn của hệ thống
TABS_CONFIG = [
    ("Danh Ba Thôn", "DanhBaThon"),
    ("Thông Báo", "ThongBao"),
    ("Sự Kiện", "SuKien"),
    ("Công Khai Thu Chi", "CongKhaiThuChi"),
    ("Phản Ánh", "PhanAnh"),
    ("Chợ Quê", "ChoQue"),
    ("Vinh Danh", "VinhDanh"),
    ("Đăng Ký Sự Kiện", "DangKySuKien"),
    ("Đặt Lịch Nhà Văn Hóa", "DatLichNhaVanHoa"),
    ("Quản Trị Cán Bộ", "QuanTriCanBo")
]

# 5. Sidebar: Giao diện & Nội dung Chương trình Mục tiêu Quốc gia chuyển đổi số
st.sidebar.title("🏡 KDC LĂNG TÔ")
st.sidebar.markdown("---")
st.sidebar.markdown(
    "### 🚀 Ứng dụng Chuyển đổi số\n"
    "**Chương trình Mục tiêu Quốc gia**\n"
    "Giai đoạn **2026 - 2035**\n\n"
    "Thúc đẩy ứng dụng công nghệ thông tin, xây dựng hạ tầng số thông minh, minh bạch và phát triển cộng đồng bền vững."
)
st.sidebar.markdown("---")

# Chọn tab hiển thị
tab_titles = [item[0] for item in TABS_CONFIG]
selected_tab_title = st.sidebar.radio("📋 Danh Mục Quản Lý", tab_titles)

# Lấy mã worksheet tương ứng
current_sheet_name = next(sheet[1] for sheet in TABS_CONFIG if sheet[0] == selected_tab_title)

# Tiêu đề chính giao diện
st.title(f"📌 {selected_tab_title}")
st.markdown("---")

# Tải và hiển thị dữ liệu
df = load_gsheet_data(current_sheet_name)

if not df.empty:
    df_display = df.copy()
    df_display.insert(0, "STT", range(1, len(df_display) + 1))
    st.dataframe(df_display, use_container_width=True, hide_index=True)
else:
    st.info("💡 Bảng này hiện chưa có dữ liệu hoặc đang được cập nhật.")

# 6. Khu vực Quản trị viên Thêm / Sửa / Xóa dữ liệu bảo mật
st.markdown("---")
st.subheader("🛠️ Khu Vực Quản Trị Hệ Thống")
admin_pass = st.text_input("Nhập mật khẩu quản trị viên để thay đổi dữ liệu:", type="password", key="admin_key")

if admin_pass == "admin123":
    st.success("✅ Đã xác thực quyền Quản trị thành công!")
    
    action = st.selectbox("Chọn thao tác quản lý:", ["Thêm mới bản ghi", "Cập nhật / Sửa bản ghi", "Xóa bản ghi"])
    
    columns = list(df.columns) if not df.empty else ["No_Data"]

    if action == "Thêm mới bản ghi":
        st.write("### ➕ Nhập thông tin bản ghi mới")
        with st.form("add_form"):
            new_data = {}
            for col in columns:
                new_data[col] = st.text_input(f"Nhập {col}:")
            submitted = st.form_submit_button("Lưu bản ghi mới")
            if submitted:
                new_row_df = pd.DataFrame([new_data])
                updated_df = pd.concat([df, new_row_df], ignore_index=True)
                try:
                    conn.update(worksheet=current_sheet_name, data=updated_df)
                    st.success("🎉 Thêm mới dữ liệu thành công! Hãy tải lại trang để xem kết quả.")
                except Exception as e:
                    st.error(f"Lỗi khi lưu lên Google Sheets: {e}")

    elif action == "Cập nhật / Sửa bản ghi" and not df.empty:
        st.write("### ✏️ Sửa thông tin bản ghi")
        row_idx = st.number_input("Chọn số thứ tự hàng trong bảng (bắt đầu từ 0):", min_value=0, max_value=len(df)-1, step=1)
        with st.form("edit_form"):
            edited_data = {}
            for col in columns:
                default_val = str(df.loc[row_idx, col]) if col in df.columns else ""
                edited_data[col] = st.text_input(f"Sửa {col}:", value=default_val)
            update_submitted = st.form_submit_button("Cập nhật thay đổi")
            if update_submitted:
                for col, val in edited_data.items():
                    df.loc[row_idx, col] = val
                try:
                    conn.update(worksheet=current_sheet_name, data=df)
                    st.success("✏️ Cập nhật dữ liệu thành công!")
                except Exception as e:
                    st.error(f"Lỗi khi cập nhật Google Sheets: {e}")

    elif action == "Xóa bản ghi" and not df.empty:
        st.write("### 🗑️ Xóa bản ghi")
        del_idx = st.number_input("Chọn số thứ tự hàng cần xóa (bắt đầu từ 0):", min_value=0, max_value=len(df)-1, step=1, key="del_input")
        if st.button("Xóa vĩnh viễn dòng này", type="primary"):
            df = df.drop(del_idx).reset_index(drop=True)
            try:
                conn.update(worksheet=current_sheet_name, data=df)
                st.warning("🗑️ Đã xóa dữ liệu thành công!")
            except Exception as e:
                st.error(f"Lỗi khi xóa dữ liệu trên Google Sheets: {e}")
elif admin_pass:
    st.error("❌ Mật khẩu quản trị không chính xác! (Mật khẩu mặc định: admin123)")
