// Cấu hình các "sheet" dữ liệu (trước đây là các sheet Excel, giờ là bảng Postgres).
// Mỗi bảng: tên bảng DB, tên hiển thị, và danh sách cột (khoá DB + nhãn tiếng Việt + loại ô nhập).

export const TABLES = {
  thongbao: {
    label: "Thông báo",
    icon: "📢",
    columns: [
      { key: "tieu_de", label: "Tiêu Đề", type: "text" },
      { key: "noi_dung", label: "Nội Dung", type: "textarea" },
      { key: "phan_loai", label: "Phân Loại", type: "text" },
      { key: "ngay_dang", label: "Ngày Đăng", type: "date" },
      { key: "nguoi_dang", label: "Người Đăng", type: "text" },
      { key: "ghim_noi_bat", label: "Ghim Nổi Bật", type: "select", options: ["Không", "Có"] },
    ],
  },
  danhba_thon: {
    label: "Danh bạ",
    icon: "📋",
    columns: [
      { key: "ho_ten", label: "Họ Tên", type: "text" },
      { key: "chuc_vu", label: "Chức Vụ", type: "text" },
      { key: "so_dien_thoai", label: "Số Điện Thoại", type: "text" },
      { key: "can_bo", label: "Cán Bộ", type: "select", options: ["Không", "Có"] },
    ],
  },
  su_kien: {
    label: "Sự kiện",
    icon: "🎉",
    columns: [
      { key: "ten_su_kien", label: "Tên Sự Kiện", type: "text" },
      { key: "mo_ta", label: "Mô Tả", type: "textarea" },
      { key: "thoi_gian_bat_dau", label: "Thời Gian Bắt Đầu", type: "text" },
      { key: "dia_diem", label: "Địa Điểm", type: "text" },
      { key: "tong_so_ho_tham_gia", label: "Tổng Số Hộ Tham Gia", type: "text", readOnlyInAdmin: true },
    ],
  },
  dang_ky_su_kien: {
    label: "Đăng ký sự kiện",
    icon: "📝",
    columns: [
      { key: "ho_ten", label: "Họ Tên", type: "text" },
      { key: "ten_su_kien", label: "Tên Sự Kiện", type: "text" },
      { key: "so_luong", label: "Số Lượng", type: "text" },
      { key: "ghi_chu", label: "Ghi Chú", type: "text" },
      { key: "ngay_dang_ky", label: "Ngày Đăng Ký", type: "date" },
    ],
  },
  // 👉 Bảng bổ sung: Tổng hợp danh sách họp cuối năm & bình xét đánh giá
  dang_ky: {
    label: "Đăng ký họp & Bình xét",
    icon: "📊",
    columns: [
      { key: "ho_gia_dinh", label: "Hộ gia đình / Chủ hộ", type: "text" },
      { key: "so_nguoi_tham_gia", label: "Số người tham gia", type: "text" },
      { 
        key: "trang_thai", 
        label: "Trạng Thái", 
        type: "select", 
        options: ["Đăng ký tham gia", "Đã tham gia", "Vắng mặt"] 
      },
      { key: "ghi_chu", label: "Ghi Chú / Đánh Giá", type: "textarea" },
      { key: "ngay_dang_ky", label: "Ngày Đăng Ký", type: "date" },
    ],
  },
  cong_khai_thu_chi: {
    label: "Thu chi",
    icon: "💰",
    columns: [
      { key: "ngay", label: "Ngày", type: "date" },
      { key: "noi_dung", label: "Nội Dung", type: "text" },
      { key: "thu", label: "Thu (VNĐ)", type: "text" },
      { key: "chi", label: "Chi (VNĐ)", type: "text" },
      { key: "ghi_chu", label: "Ghi Chú", type: "text" },
    ],
  },
  phan_anh: {
    label: "Phản ánh",
    icon: "⚠️",
    columns: [
      { key: "nguoi_gui", label: "Người Gửi", type: "text" },
      { key: "linh_vuc", label: "Lĩnh Vực", type: "text" },
      { key: "noi_dung", label: "Nội Dung", type: "textarea" },
      { key: "dia_diem", label: "Địa Điểm", type: "text" },
      { key: "ngay_gui", label: "Ngày Gửi", type: "date" },
      {
        key: "trang_thai",
        label: "Trạng Thái",
        type: "select",
        options: ["Chờ xử lý", "Đang xử lý", "Đã xử lý", "Từ chối"],
      },
    ],
  },
  vinh_danh: {
    label: "Vinh danh",
    icon: "🏆",
    columns: [
      { key: "ho_ten", label: "Họ Tên", type: "text" },
      { key: "danh_hieu", label: "Danh Hiệu", type: "text" },
      { key: "ly_do_khen_thuong", label: "Lý Do Khen Thưởng", type: "textarea" },
      { key: "nam", label: "Năm", type: "text" },
    ],
  },
  cho_que: {
    label: "Chợ quê",
    icon: "🛒",
    columns: [
      { key: "ten_san_pham", label: "Tên Sản Phẩm", type: "text" },
      { key: "phan_loai", label: "Phân Loại", type: "text" },
      { key: "gia_ban", label: "Giá Bán", type: "text" },
      { key: "don_vi", label: "Đơn Vị", type: "text" },
      { key: "so_dien_thoai", label: "Số Điện Thoại", type: "text" },
      { key: "ngay_dang", label: "Ngày Đăng", type: "date" },
    ],
  },
  dat_lich_nha_van_hoa: {
    label: "Đặt lịch",
    icon: "📅",
    columns: [
      { key: "ho_ten", label: "Họ Tên", type: "text" },
      { key: "dich_vu", label: "Dịch Vụ", type: "text" },
      { key: "ngay_su_dung", label: "Ngày Sử Dụng", type: "date" },
      { key: "muc_dich", label: "Mục Đích", type: "text" },
      {
        key: "trang_thai",
        label: "Trạng Thái",
        type: "select",
        options: ["Chờ duyệt", "Đã duyệt", "Từ chối"],
      },
    ],
  },
};

export const TABLE_ORDER = [
  "thongbao",
  "danhba_thon",
  "su_kien",
  "dang_ky_su_kien",
  "dang_ky", // Sắp xếp vị trí hiển thị trên AdminPicker
  "cong_khai_thu_chi",
  "phan_anh",
  "vinh_danh",
  "cho_que",
  "dat_lich_nha_van_hoa",
];

export function columnKeys(table) {
  return TABLES[table].columns.map((c) => c.key);
}

// Tên sheet Excel gốc (bản Streamlit cũ) <-> tên bảng Postgres mới.
// Giữ ánh xạ này để có thể xuất/nhập lại file .xlsx sao lưu từ bản cũ.
export const LEGACY_SHEET_NAMES = {
  thongbao: "ThongBao",
  danhba_thon: "DanhBaThon",
  su_kien: "SuKien",
  dang_ky_su_kien: "DangKySuKien",
  dang_ky: "DangKyHop",
  cong_khai_thu_chi: "CongKhaiThuChi",
  phan_anh: "PhanAnh",
  vinh_danh: "VinhDanh",
  cho_que: "ChoQue",
  dat_lich_nha_van_hoa: "DatLichNhaVanHoa",
};
