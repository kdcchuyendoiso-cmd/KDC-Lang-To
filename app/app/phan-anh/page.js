import { PAGES } from "@/lib/pages-config";
import { Flash, PageHeader } from "@/app/components/ui";
import { submitFeedback } from "./actions";

export const dynamic = "force-dynamic";

export default function Page({ searchParams }) {
  return (
    <>
      <PageHeader page={PAGES["phan-anh"]} />
      <Flash searchParams={searchParams} />
      <div className="card-body" style={{ margin: "0 2px 12px" }}>
        🔒 Phản ánh chỉ hiển thị với cán bộ thôn, không đăng công khai.
      </div>
      <form className="form-card" action={submitFeedback}>
        <div className="field">
          <label>Họ và tên của bạn *</label>
          <input name="nguoi_gui" maxLength={80} required />
        </div>
        <div className="field">
          <label>Lĩnh vực</label>
          <select name="linh_vuc" defaultValue="Môi trường">
            {["Môi trường", "An ninh trật tự", "Hạ tầng / Đường xá", "Tranh chấp", "Khác"].map((o) => (
              <option key={o}>{o}</option>
            ))}
          </select>
        </div>
        <div className="field">
          <label>Nội dung phản ánh *</label>
          <textarea
            name="noi_dung"
            placeholder="Mô tả rõ sự việc để cán bộ xử lý nhanh hơn"
            maxLength={2000}
            rows={5}
            required
          />
        </div>
        <div className="field">
          <label>Địa điểm xảy ra</label>
          <input name="dia_diem" placeholder="Ví dụ: đầu ngõ 12, gần nhà văn hóa" maxLength={200} />
        </div>
        <button className="btn-primary" type="submit">
          Gửi phản ánh
        </button>
      </form>
    </>
  );
}
