"use client";

import { useMemo, useState } from "react";
import { yearOf } from "@/lib/helpers";
import { EmptyState } from "@/app/components/ui";

export default function HonorsList({ rows }) {
  const enriched = useMemo(() => rows.map((r) => ({ ...r, _y: yearOf(r.nam) })), [rows]);
  const years = useMemo(
    () => [...new Set(enriched.map((r) => r._y).filter(Boolean))].sort((a, b) => b - a),
    [enriched]
  );
  const ALL = "Tất cả các năm";
  const [pick, setPick] = useState(ALL);

  const filtered = (pick === ALL ? enriched : enriched.filter((r) => r._y === Number(pick))).sort(
    (a, b) => b._y - a._y
  );

  if (!rows.length) {
    return (
      <EmptyState title="Chưa có danh sách vinh danh" hint="Những gương sáng của khu dân cư sẽ được ghi nhận tại đây." icon="🏆" />
    );
  }

  return (
    <>
      {years.length > 1 ? (
        <select className="admin-select" value={pick} onChange={(e) => setPick(e.target.value)}>
          <option>{ALL}</option>
          {years.map((y) => (
            <option key={y} value={y}>
              {y}
            </option>
          ))}
        </select>
      ) : null}
      {filtered.map((r) => (
        <div key={r.id} className="card honor">
          <div className="trophy">🏆</div>
          <div className="h-info">
            <div className="h-name">{r.ho_ten}</div>
            <div className="h-title">{r.danh_hieu}</div>
            {(r.ly_do_khen_thuong || "").trim() ? <div className="h-reason">{r.ly_do_khen_thuong}</div> : null}
          </div>
          {(r.nam || "").trim() ? <span className="badge gray">{r.nam}</span> : null}
        </div>
      ))}
    </>
  );
}
