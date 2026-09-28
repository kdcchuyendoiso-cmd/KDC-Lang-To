import Link from "next/link";
import { eventsWithCounts } from "@/lib/db";
import { parseDate, showDate, todayStr } from "@/lib/helpers";
import { PAGES } from "@/lib/pages-config";
import { EmptyState, PageHeader } from "@/app/components/ui";

export const dynamic = "force-dynamic";

export default async function Page() {
  const events = await eventsWithCounts();
  const today = new Date();
  today.setHours(0, 0, 0, 0);

  const order = (value) => {
    const d = parseDate(value);
    if (!d) return [1, 0];
    const t = new Date(d);
    t.setHours(0, 0, 0, 0);
    return t >= today ? [0, t.getTime()] : [2, -t.getTime()];
  };

  const sorted = [...events].sort((a, b) => {
    const [ga, ta] = order(a.thoi_gian_bat_dau);
    const [gb, tb] = order(b.thoi_gian_bat_dau);
    if (ga !== gb) return ga - gb;
    return ta - tb;
  });

  return (
    <>
      <PageHeader page={PAGES["su-kien"]} />
      {sorted.length === 0 ? (
        <EmptyState title="Chưa có sự kiện nào" hint="Sự kiện mới sẽ hiện ở đây ngay khi được đăng." icon="🎉" />
      ) : (
        sorted.map((r) => {
          const d = parseDate(r.thoi_gian_bat_dau);
          const dd = d ? new Date(d) : null;
          if (dd) dd.setHours(0, 0, 0, 0);
          const past = dd && dd < today;
          const isToday = dd && dd.getTime() === today.getTime();
          const joined = (r.tong_so_ho_tham_gia || "").trim();

          return (
            <div key={r.id} className="card">
              <div className="row-card top">
                {d ? (
                  <div className="cal">
                    <b>{String(d.getDate()).padStart(2, "0")}</b>
                    <span>Th{d.getMonth() + 1}</span>
                  </div>
                ) : (
                  <div className="cal alt">📅</div>
                )}
                <div className="rc-main">
                  <div className="card-top">
                    {isToday ? (
                      <span className="badge warn">Hôm nay</span>
                    ) : past ? (
                      <span className="badge gray">Đã diễn ra</span>
                    ) : (
                      <span className="badge ok">Sắp diễn ra</span>
                    )}
                    {joined && joined !== "0" ? <span className="badge">👥 {joined} đăng ký</span> : null}
                  </div>
                  <div className="card-title">{r.ten_su_kien}</div>
                </div>
              </div>
              <div className="card-body" style={{ marginTop: 8 }}>
                {r.mo_ta}
              </div>
              <div className="card-meta">
                {(r.thoi_gian_bat_dau || "").trim() ? <span>🕒 {showDate(r.thoi_gian_bat_dau)}</span> : null}
                {(r.dia_diem || "").trim() ? <span>📍 {r.dia_diem}</span> : null}
              </div>
              {!past ? (
                <Link className="btn-link" href={`/dang-ky?sk=${encodeURIComponent(r.ten_su_kien.trim())}`}>
                  Đăng ký tham gia
                </Link>
              ) : null}
            </div>
          );
        })
      )}
    </>
  );
}
