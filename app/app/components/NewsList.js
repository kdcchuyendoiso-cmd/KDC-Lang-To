"use client";

import { useMemo, useState } from "react";
import { isYes, showDate } from "@/lib/helpers";
import { EmptyState } from "@/app/components/ui";

function sortNews(rows) {
  return [...rows].sort((a, b) => {
    const pa = isYes(a.ghim_noi_bat) ? 1 : 0;
    const pb = isYes(b.ghim_noi_bat) ? 1 : 0;
    if (pa !== pb) return pb - pa;
    const da = a.ngay_dang || "";
    const db_ = b.ngay_dang || "";
    return da < db_ ? 1 : da > db_ ? -1 : 0;
  });
}

export default function NewsList({ rows }) {
  const sorted = useMemo(() => sortNews(rows), [rows]);
  const cats = useMemo(
    () => [...new Set(sorted.map((r) => (r.phan_loai || "").trim()).filter(Boolean))].sort(),
    [sorted]
  );
  const [cat, setCat] = useState("Tất cả");

  const filtered = cat === "Tất cả" ? sorted : sorted.filter((r) => (r.phan_loai || "").trim() === cat);

  if (!sorted.length) {
    return <EmptyState title="Chưa có thông báo nào" hint="Khi cán bộ đăng tin mới, bà con sẽ thấy ở đây." />;
  }

  return (
    <>
      {cats.length > 1 ? (
        <select className="admin-select" value={cat} onChange={(e) => setCat(e.target.value)}>
          <option>Tất cả</option>
          {cats.map((c) => (
            <option key={c}>{c}</option>
          ))}
        </select>
      ) : null}
      {filtered.map((r) => {
        const pinned = isYes(r.ghim_noi_bat);
        const category = (r.phan_loai || "").trim() || "Chung";
        return (
          <div key={r.id} className={`card${pinned ? " pinned" : ""}`}>
            <div className="card-top">
              {pinned ? <span className="badge warn">📌 Ghim</span> : null}
              <span className="badge">{category}</span>
            </div>
            <div className="card-title">{(r.tieu_de || "").trim() || "Thông báo"}</div>
            <div className="card-body">{r.noi_dung}</div>
            <div className="card-meta">
              {(r.ngay_dang || "").trim() ? <span>🗓 {showDate(r.ngay_dang)}</span> : null}
              {(r.nguoi_dang || "").trim() ? <span>👤 {r.nguoi_dang}</span> : null}
            </div>
          </div>
        );
      })}
    </>
  );
}
