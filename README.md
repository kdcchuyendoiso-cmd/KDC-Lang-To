# Cổng thông tin Khu dân cư Lăng Tô (bản Next.js chạy trên Vercel)

Đây là bản chuyển đổi từ ứng dụng Streamlit gốc sang **Next.js**, để chạy mượt và triển khai trên **Vercel**.
Toàn bộ nghiệp vụ được giữ nguyên: bảng tin, danh bạ, sự kiện & đăng ký, công khai thu chi, phản ánh kiến
nghị, vinh danh, chợ quê, đặt lịch nhà văn hóa, và khu vực quản trị cho cán bộ.

## Vì sao không chỉ "chuyển code" mà phải viết lại?

- **Vercel không có ổ đĩa lưu trữ cố định.** Mỗi lần chạy là một hàm serverless độc lập, không thể đọc/ghi
  file Excel như bản Streamlit cũ (bản cũ cũng đã gặp vấn đề này trên Streamlit Cloud, ở đây chỉ là rõ hơn).
  Vì vậy dữ liệu được chuyển sang **Postgres** (dùng tích hợp Vercel Postgres / Neon).
- Streamlit là framework Python chạy giao diện phía máy chủ; Vercel chủ yếu chạy Next.js/Node.js. Giao diện,
  form, khu quản trị... được viết lại bằng React nhưng **giữ đúng bố cục, màu sắc, văn phong tiếng Việt** của
  bản gốc (xem `app/globals.css`, chuyển thẳng từ `styles.py`).

## Cấu trúc

```
lib/schema.js       cấu hình các bảng dữ liệu (trước là các sheet Excel)
lib/db.js           đọc/ghi Postgres, xuất/nhập file Excel sao lưu
lib/helpers.js       định dạng tiền, ngày, số điện thoại... (chuyển từ helpers.py)
lib/auth.js          đăng nhập khu vực cán bộ bằng 1 mật khẩu chung (cookie phiên)
app/globals.css       giao diện điện thoại (chuyển từ styles.py)
app/<slug>/page.js    10 trang, đúng slug với bản cũ (bang-tin, danh-ba, su-kien, ...)
app/quan-tri/         đăng nhập + quản lý dữ liệu + sao lưu/khôi phục Excel
```

## Chạy thử trên máy

```bash
npm install
```

Cần một Postgres để chạy thử (miễn phí: tạo project trên https://neon.tech, hoặc dùng Vercel Postgres).
Tạo file `.env.local`:

```
POSTGRES_URL="postgres://...chuỗi-kết-nối-của-bạn..."
ADMIN_PASSWORD=doi-mat-khau-nay
```

Rồi chạy:

```bash
npm run dev
```

Mở http://localhost:3000. Lần chạy đầu tiên ứng dụng tự tạo các bảng dữ liệu còn thiếu (giống `ensure_file()`
ở bản cũ, chỉ khác là tạo bảng Postgres thay vì sheet Excel).

## Triển khai lên Vercel

1. Đưa code này lên GitHub (repo **Private**, vì có số điện thoại, phản ánh và lịch đặt của bà con).
2. Vào https://vercel.com/new, chọn repo này, bấm **Deploy** (Next.js được nhận diện tự động, không cần cấu
   hình gì thêm).
3. Vào **Storage** trong project trên Vercel → **Create Database** → chọn **Postgres** (hoặc Neon) → bấm
   **Connect** vào project. Vercel sẽ tự thêm các biến `POSTGRES_URL`,... vào project — không cần nhập tay.
4. Vào **Settings → Environment Variables**, thêm:
   ```
   ADMIN_PASSWORD = mat-khau-cua-ban
   ```
   Nếu không đặt, hệ thống dùng mật khẩu mặc định `admin123` và sẽ nhắc trong khu vực quản trị. Hãy đổi
   trước khi đưa cho người khác dùng.
5. Vào tab **Deployments**, bấm **Redeploy** một lần (để ứng dụng nhận biến môi trường/DB vừa nối), rồi gửi
   đường link `https://<ten-project>.vercel.app` cho bà con.

## Mang dữ liệu cũ từ file Excel sang

Vào **Khu vực cán bộ → Sao lưu & khôi phục**, tải lên file `dulieu_langto.xlsx` cũ. Hệ thống nhận diện đúng
tên sheet cũ (`ThongBao`, `DanhBaThon`, `SuKien`...) và nhập toàn bộ dữ liệu vào Postgres. File tải xuống từ
đây sau này cũng đúng định dạng sheet như bản cũ, có thể mở lại bằng Excel bình thường.

## Khác biệt nhỏ so với bản Streamlit

- Dữ liệu nằm trong Postgres, không mất khi Vercel triển khai lại — không còn rủi ro "file Excel về trống"
  như cảnh báo ở bản cũ.
- Khu vực quản trị hiển thị từng dòng dưới dạng thẻ có thể sửa/xóa riêng (thay cho bảng tính có thể kéo sửa
  nhiều dòng một lúc), phù hợp hơn khi dùng trên điện thoại.
- Thanh điều hướng dưới cùng vẫn được ẩn như bản gốc (mỗi trang có nút "‹" quay về trang chủ).
