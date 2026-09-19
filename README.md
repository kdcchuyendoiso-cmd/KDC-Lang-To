# Cổng thông tin Khu dân cư Lăng Tô

Ứng dụng Streamlit giúp cán bộ thôn và bà con cùng dùng trên điện thoại: bảng tin, danh bạ gọi nhanh, sự kiện và đăng ký, công khai thu chi, phản ánh kiến nghị, vinh danh, chợ quê nông sản, đặt lịch nhà văn hóa, và khu vực quản trị cho cán bộ. Dữ liệu lưu trong một file Excel.

## Giao diện điện thoại

- Trang chủ dạng lưới 3 cột, mỗi ô đủ lớn để chạm bằng ngón tay.
- Thanh điều hướng cố định phía dưới (Trang chủ, Bảng tin, Sự kiện, Danh bạ, Phản ánh).
- Nội dung hiển thị dạng thẻ thay cho bảng rộng, không phải kéo ngang.
- Danh bạ và Chợ quê có nút **Gọi** bấm là gọi ngay; tìm kiếm không cần gõ dấu.
- Thu chi có tổng thu, tổng chi, số còn lại và lọc theo tháng.
- Chữ nhập liệu 16px để iPhone không tự phóng to khi chạm vào ô.
- Nút Back của điện thoại hoạt động; mỗi trang có đường dẫn riêng, có thể gửi qua Zalo, ví dụ `https://<ten-app>.streamlit.app/?page=phan-anh`.

| Đường dẫn | Trang |
|---|---|
| `?page=bang-tin` | Bảng tin |
| `?page=danh-ba` | Danh bạ |
| `?page=su-kien` | Sự kiện |
| `?page=thu-chi` | Công khai thu chi |
| `?page=dang-ky` | Đăng ký sự kiện |
| `?page=phan-anh` | Phản ánh, kiến nghị |
| `?page=vinh-danh` | Vinh danh |
| `?page=cho-que` | Chợ quê |
| `?page=dat-lich` | Đặt lịch nhà văn hóa |
| `?page=quan-tri` | Khu vực cán bộ |

## Chạy thử trên máy

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

Lần chạy đầu tiên ứng dụng tự tạo file `dulieu_langto.xlsx`. Nếu đã có file cũ, chép vào cùng thư mục với `app.py`. Tên sheet và tên cột giữ nguyên như bản trước.

## Đưa lên GitHub

Nên tạo repo ở chế độ **Private**, vì dữ liệu có số điện thoại, phản ánh và lịch đặt của bà con.

```bash
git init
git add .
git commit -m "Giao diện mobile cho cổng thông tin Khu dân cư Lăng Tô"
git branch -M main
git remote add origin https://github.com/<tai-khoan>/langto-portal.git
git push -u origin main
```

File `dulieu_langto.xlsx` và `.streamlit/secrets.toml` đã nằm trong `.gitignore`, sẽ không bị đẩy lên. Repo Private và muốn mang dữ liệu theo thì xóa dòng `dulieu_langto.xlsx` trong `.gitignore` trước khi `git add`.

## Triển khai trên Streamlit Community Cloud

1. Vào https://share.streamlit.io, chọn **New app**, chọn repo, nhánh `main`, file `app.py`.
2. Mở **Advanced settings > Secrets** và dán:
   ```toml
   ADMIN_PASSWORD = "mat-khau-cua-ban"
   ```
3. Bấm **Deploy**, rồi gửi đường link cho bà con.

Nếu không đặt `ADMIN_PASSWORD`, ứng dụng dùng mật khẩu mặc định `admin123` và sẽ nhắc trong khu vực quản trị. Hãy đổi trước khi đưa cho người khác dùng.

## Lưu ý quan trọng về dữ liệu

Streamlit Community Cloud không giữ file lâu dài: khi ứng dụng khởi động lại hoặc được cập nhật, file Excel có thể quay về trống. Vì vậy:

- Vào **Quản trị > Sao lưu & khôi phục** để tải file Excel về định kỳ, và tải lên lại khi cần khôi phục.
- Để dùng lâu dài, nên chuyển nơi lưu sang Google Sheets hoặc cơ sở dữ liệu, hoặc chạy trên máy chủ có ổ đĩa lưu trữ cố định. Logic đọc/ghi nằm gọn trong `storage.py` nên việc thay thế không ảnh hưởng phần giao diện.

## Cấu trúc

```
app.py          giao diện và các trang
storage.py      đọc/ghi file Excel (có khóa, tự sao lưu .bak)
helpers.py      định dạng tiền, ngày, số điện thoại, escape HTML
styles.py       CSS cho điện thoại
requirements.txt
.streamlit/config.toml            giao diện sáng, thanh công cụ tối giản
.streamlit/secrets.toml.example   mẫu mật khẩu quản trị
```
