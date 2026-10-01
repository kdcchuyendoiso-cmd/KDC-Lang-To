import Link from "next/link";
import { getAll } from "@/lib/db";
import { isYes, parseDate, showDate } from "@/lib/helpers";
import { PAGES, TILE_SLUGS } from "@/lib/pages-config";
import { Flash } from "@/app/components/ui";

export const dynamic = "force-dynamic";

function sortNews(rows) {
  return [...rows].sort((a, b) => {
    const pa = isYes(a.ghim_noi_bat) ? 1 : 0;
    const pb = isYes(b.ghim_noi_bat) ? 1 : 0;
    if (pa !== pb) return pb - pa;
    const da = parseDate(a.ngay_dang)?.getTime() ?? -Infinity;
    const db_ = parseDate(b.ngay_dang)?.getTime() ?? -Infinity;
    return db_ - da;
  });
}

export default async function HomePage({ searchParams }) {
  const [newsRaw, events, contacts] = await Promise.all([
    getAll("thongbao"),
    getAll("su_kien"),
    getAll("danhba_thon"),
  ]);
  const news = sortNews(newsRaw);
  const latest = news[0];

  return (
    <>
      <Flash searchParams={searchParams} />
      <div className="hero">
        <div className="hero-row">
          <div className="hero-mark">🏡</div>
          <div className="hero-title">Khu dân cư Lăng Tô</div>
        </div>
        <div className="hero-sub">Trang thông tin và điều hành (chạy thử nghiệm).</div>
        <div className="chips">
          <Link className="chip" href="/bang-tin">
            📢 {news.length} thông báo
          </Link>
          <Link className="chip" href="/su-kien">
            🎉 {events.length} sự kiện
          </Link>
        </div>
      </div>

      <div className="grid3">
        {TILE_SLUGS.map((slug) => {
          const p = PAGES[slug];
          return (
            <Link key={slug} className="tile" href={`/${slug}`}>
              <span className="ico" style={{ background: p.bg, color: p.fg }}>
                {p.icon}
              </span>
              <span className="lbl">{p.short}</span>
            </Link>
          );
        })}
      </div>

      {latest ? (
        <>
          <div className="sec">
            <b>Tin mới nhất</b>
            <Link href="/bang-tin">Xem tất cả</Link>
          </div>
          <NewsCard r={latest} />
        </>
      ) : null}

      <div className="admin-link">
        <Link href="/quan-tri">🔐 Khu vực cán bộ</Link>
      </div>
      <div className="tip">
        Mẹo: mở menu trình duyệt và chọn “Thêm vào màn hình chính” để dùng như một ứng dụng.
      </div>
      <div style={{ height: 0 }}>{contacts.length /* giữ dữ liệu đã tải, tránh cảnh báo lint không dùng */}</div>
    </>
  );
}

function NewsCard({ r }) {
  const pinned = isYes(r.ghim_noi_bat);
  const cat = (r.phan_loai || "").trim() || "Chung";
  return (
    <div className={`card${pinned ? " pinned" : ""}`}>
      <div className="card-top">
        {pinned ? <span className="badge warn">📌 Ghim</span> : null}
        <span className="badge">{cat}</span>
      </div>
      <div className="card-title">{(r.tieu_de || "").trim() || "Thông báo"}</div>
      <div className="card-body">{r.noi_dung}</div>
      <div className="card-meta">
        {(r.ngay_dang || "").trim() ? <span>🗓 {showDate(r.ngay_dang)}</span> : null}
        {(r.nguoi_dang || "").trim() ? <span>👤 {r.nguoi_dang}</span> : null}
      </div>
    </div>
  );
}
