import streamlit as st
import pandas as pd
from streamlit_gsheets import GsheetsConnection

# Cấu hình giao diện trang web
st.set_page_config(
    page_title="Quản Lý Khu Dân Cư Lăng Tô",
    page_icon="🏡",
    layout="wide"
)

# Khởi tạo kết nối Google Sheets an toàn ở đầu ứng dụng
try:
    conn = st.connection("gsheets", type=GsheetsConnection)
except Exception as e:
    st.error(f"Lỗi kết nối GsheetsConnection: {e}. Vui lòng kiểm tra lại mục Secrets trên Streamlit Cloud.")
    st.stop()

# Hàm đọc dữ liệu từ từng Tab (worksheet) của Google Sheets
def load_gsheet_data(sheet_name):
    try:
        data = conn.read(worksheet=sheet_name, ttl=0)
        if data is None or data.empty:
            return pd.DataFrame()
        return data.dropna(how="all")
    except Exception as e:
        st.warning(f"Không thể tải dữ liệu từ tab '{sheet_name}': {e}")
        return pd.DataFrame()

# Danh sách 10 Tab chuẩn của hệ thống
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

# Sidebar hệ thống
st.sidebar.title("🏡 KDC Lăng Tô")
st.sidebar.markdown("---")
st.sidebar.info(
    "🌟 **Chương trình Mục tiêu Quốc gia**\n"
    "Giai đoạn **2026 - 2035**\n\n"
    "Phát triển hạ tầng số, xây dựng khu dân cư thông minh, đoàn kết và phát triển bền vững."
)
st.sidebar.markdown("---")

# Chọn tab hiển thị
tab_titles = [item[0] for item in TABS_CONFIG]
selected_tab_title = st.sidebar.radio("📋 Chọn Chức Năng Quản Lý", tab_titles)

# Lấy mã worksheet tương ứng
current_sheet_name = next(sheet[1] for sheet in TABS_CONFIG if sheet[0] == selected_tab_title)

st.title(f"📌 {selected_tab_title}")
st.markdown("---")

# Tải dữ liệu từ Google Sheets
df = load_gsheet_data(current_sheet_name)

# Hiển thị dữ liệu kèm số thứ tự bắt đầu từ 1
if not df.empty:
    df_display = df.copy()
    df_display.insert(0, "STT", range(1, len(df_display) + 1))
    st.dataframe(df_display, use_container_width=True, hide_index=True)
else:
    st.info("Hiện tại chưa có dữ liệu nào trong bảng này hoặc đang cập nhật.")

st.markdown("---")
st.subheader("🛠️ Khu Vực Quản Trị & Cập Nhật Dữ Liệu")
admin_pass = st.text_input("Nhập mật khẩu quản trị viên để Thêm/Sửa/Xóa:", type="password", key="admin_key")

if admin_pass == "admin123":
    st.success("✅ Đã xác thực quyền Quản trị viên thành công!")
    
    action = st.selectbox("Chọn thao tác:", ["Thêm mới", "Cập nhật / Sửa", "Xóa dòng"])
    
    if not df.empty:
        columns = list(df.columns)
    else:
        columns = ["No_Data"]

    if action == "Thêm mới":
        st.write("### Nhập thông tin bản ghi mới")
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
                    st.success("🎉 Thêm mới dữ liệu thành công! Hãy tải lại trang để thấy thay đổi.")
                except Exception as e:
                    st.error(f"Lỗi khi lưu dữ liệu lên Google Sheets: {e}")

    elif action == "Cập nhật / Sửa" and not df.empty:
        st.write("### Chọn dòng cần chỉnh sửa (theo chỉ số hàng)")
        row_idx = st.number_input("Chọn số thứ tự hàng trong bảng gốc (bắt đầu từ 0):", min_value=0, max_value=len(df)-1, step=1)
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

    elif action == "Xóa dòng" and not df.empty:
        st.write("### Chọn dòng cần xóa")
        del_idx = st.number_input("Chọn chỉ số dòng cần xóa (bắt đầu từ 0):", min_value=0, max_value=len(df)-1, step=1, key="del_input")
        if st.button("Xóa vĩnh viễn dòng này", type="primary"):
            df = df.drop(del_idx).reset_index(drop=True)
            try:
                conn.update(worksheet=current_sheet_name, data=df)
                st.warning("🗑️ Đã xóa dữ liệu thành công!")
            except Exception as e:
                st.error(f"Lỗi khi xóa dữ liệu trên Google Sheets: {e}")
elif admin_pass:
    st.error("❌ Mật khẩu quản trị không chính xác! (Mật khẩu mặc định: admin123)")
