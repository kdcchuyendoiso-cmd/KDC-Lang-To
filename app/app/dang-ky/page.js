import { eventsWithCounts } from "@/lib/db";
import { showDate } from "@/lib/helpers";
import { PAGES } from "@/lib/pages-config";
import { EmptyState, Flash, PageHeader } from "@/app/components/ui";
import { submitRegistration } from "./actions";

export const dynamic = "force-dynamic";

export default async function Page({ searchParams }) {
  const events = await eventsWithCounts();
  const names = events.map((e) => (e.ten_su_kien || "").trim()).filter(Boolean);
  const preset = String(searchParams?.sk || "");

  return (
    <>
      <PageHeader page={PAGES["dang-ky"]} />
      <Flash searchParams={searchParams} />

      {names.length === 0 ? (
        <EmptyState
          title="Hiện chưa có sự kiện để đăng ký"
          hint="Bà con quay lại sau khi cán bộ đăng sự kiện mới nhé."
          icon="📝"
        />
      ) : (
        <form className="form-card" action={submitRegistration}>
          <div className="field">
            <label>Họ và tên hộ gia đình / cá nhân *</label>
            <input name="ho_ten" placeholder="Ví dụ: Nguyễn Văn A" maxLength={80} required />
          </div>
          <div className="field">
            <label>Sự kiện *</label>
            <select name="su_kien" defaultValue={names.includes(preset) ? preset : names[0]}>
              {names.map((n) => (
                <option key={n} value={n}>
                  {n}
                </option>
              ))}
            </select>
          </div>
          <div className="field">
            <label>Số người tham gia</label>
            <input name="so_luong" type="number" min={1} max={50} defaultValue={1} step={1} />
          </div>
          <div className="field">
            <label>Ghi chú (không bắt buộc)</label>
            <input name="ghi_chu" maxLength={200} />
          </div>
          <button className="btn-primary" type="submit">
            Xác nhận đăng ký
          </button>
        </form>
      )}

      <div className="sec">
        <b>Số đăng ký hiện tại</b>
      </div>
      <div className="card ledger">
        {events.map((r) => (
          <div key={r.id} className="lrow">
            <div className="lr-main">
              <div className="lr-title">{r.ten_su_kien}</div>
              <div className="lr-sub">{showDate(r.thoi_gian_bat_dau)}</div>
            </div>
            <div className="lr-amt">{(r.tong_so_ho_tham_gia || "0").trim() || "0"} 👥</div>
          </div>
        ))}
      </div>
    </>
  );
}
