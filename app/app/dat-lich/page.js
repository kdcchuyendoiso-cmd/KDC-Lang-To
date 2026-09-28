import { getAll } from "@/lib/db";
import { parseDate, showDate, statusClass, todayStr } from "@/lib/helpers";
import { PAGES } from "@/lib/pages-config";
import { EmptyState, Flash, PageHeader } from "@/app/components/ui";
import { submitBooking } from "./actions";

export const dynamic = "force-dynamic";

function BookingCard({ r }) {
  const status = (r.trang_thai || "").trim() || "Chờ duyệt";
  const d = parseDate(r.ngay_su_dung);
  return (
    <div className="card row-card">
      {d ? (
        <div className="cal">
          <b>{String(d.getDate()).padStart(2, "0")}</b>
          <span>Th{d.getMonth() + 1}</span>
        </div>
      ) : (
        <div className="cal alt">📅</div>
      )}
      <div className="rc-main">
        <div className="card-title tight">{r.dich_vu}</div>
        <div className="card-meta">
          <span>👤 {r.ho_ten}</span>
          <span>🗓 {showDate(r.ngay_su_dung)}</span>
        </div>
        {(r.muc_dich || "").trim() ? (
          <div className="card-meta">
            <span>{r.muc_dich}</span>
          </div>
        ) : null}
      </div>
      <span className={`badge ${statusClass(status)}`}>{status}</span>
    </div>
  );
}

export default async function Page({ searchParams }) {
  const rows = await getAll("dat_lich_nha_van_hoa");
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  const todayISO = todayStr();

  const withDate = rows.map((r) => {
    const d = parseDate(r.ngay_su_dung);
    if (d) d.setHours(0, 0, 0, 0);
    return { ...r, _d: d };
  });
  const upcoming = withDate.filter((r) => r._d && r._d >= today).sort((a, b) => a._d - b._d);
  const past = withDate.filter((r) => !r._d || r._d < today).sort((a, b) => (b._d ?? 0) - (a._d ?? 0));

  return (
    <>
      <PageHeader page={PAGES["dat-lich"]} />
      <Flash searchParams={searchParams} />

      <form className="form-card" action={submitBooking}>
        <div className="field">
          <label>Họ và tên người đăng ký *</label>
          <input name="ho_ten" maxLength={80} required />
        </div>
        <div className="field">
          <label>Loại dịch vụ</label>
          <select name="dich_vu" defaultValue="Mượn Nhà văn hóa">
            {["Mượn Nhà văn hóa", "Mượn bàn ghế / loa đài", "Đăng ký họp thôn"].map((o) => (
              <option key={o}>{o}</option>
            ))}
          </select>
        </div>
        <div className="field">
          <label>Ngày sử dụng</label>
          <input name="ngay_su_dung" type="date" min={todayISO} defaultValue={todayISO} required />
        </div>
        <div className="field">
          <label>Mục đích sử dụng</label>
          <textarea name="muc_dich" placeholder="Ví dụ: tổ chức đám cưới, họp tổ dân phố..." maxLength={500} rows={4} />
        </div>
        <button className="btn-primary" type="submit">
          Gửi yêu cầu đặt lịch
        </button>
      </form>

      <div className="sec">
        <b>Lịch sắp tới</b>
      </div>
      {upcoming.length === 0 ? (
        <EmptyState title="Chưa có lịch sắp tới" icon="📅" />
      ) : (
        upcoming.map((r) => <BookingCard key={r.id} r={r} />)
      )}

      {past.length > 0 ? (
        <details style={{ margin: "10px 0" }}>
          <summary style={{ cursor: "pointer", fontWeight: 700, fontSize: 13.5, color: "var(--muted)" }}>
            Lịch đã qua ({past.length})
          </summary>
          <div style={{ marginTop: 10 }}>
            {past.slice(0, 30).map((r) => (
              <BookingCard key={r.id} r={r} />
            ))}
          </div>
        </details>
      ) : null}
    </>
  );
}
