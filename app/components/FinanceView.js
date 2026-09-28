"use client";

import { useMemo, useState } from "react";
import { fmtCompact, fmtVnd, parseDate, parseMoney, showDate } from "@/lib/helpers";
import { EmptyState } from "@/app/components/ui";

export default function FinanceView({ rows }) {
  const enriched = useMemo(
    () =>
      rows.map((r) => {
        const d = parseDate(r.ngay);
        return { ...r, _d: d, _thu: parseMoney(r.thu), _chi: parseMoney(r.chi) };
      }),
    [rows]
  );

  const months = useMemo(() => {
    const set = new Map();
    for (const r of enriched) {
      if (!r._d) continue;
      const key = `${r._d.getFullYear()}-${r._d.getMonth() + 1}`;
      set.set(key, { y: r._d.getFullYear(), m: r._d.getMonth() + 1 });
    }
    return [...set.values()].sort((a, b) => (b.y - a.y) * 100 + (b.m - a.m));
  }, [enriched]);

  const ALL = "Tất cả các tháng";
  const [pick, setPick] = useState(ALL);

  let filtered = enriched;
  let balanceLabel = "Còn lại";
  if (pick !== ALL) {
    const [y, m] = pick.split("/").map(Number);
    filtered = enriched.filter((r) => r._d && r._d.getFullYear() === y && r._d.getMonth() + 1 === m);
    balanceLabel = `Chênh lệch tháng ${String(m).padStart(2, "0")}/${y}`;
  }
  filtered = [...filtered].sort((a, b) => (b._d?.getTime() ?? -Infinity) - (a._d?.getTime() ?? -Infinity));

  if (!rows.length) {
    return (
      <EmptyState
        title="Chưa có khoản thu, chi nào được công khai"
        hint="Cán bộ sẽ cập nhật tại đây để bà con cùng theo dõi."
        icon="💰"
      />
    );
  }

  const thu = filtered.reduce((s, r) => s + r._thu, 0);
  const chi = filtered.reduce((s, r) => s + r._chi, 0);
  const conLai = thu - chi;

  return (
    <>
      {months.length ? (
        <select className="admin-select" value={pick} onChange={(e) => setPick(e.target.value)}>
          <option value={ALL}>{ALL}</option>
          {months.map(({ y, m }) => (
            <option key={`${y}-${m}`} value={`${y}/${m}`}>
              {`Tháng ${String(m).padStart(2, "0")}/${y}`}
            </option>
          ))}
        </select>
      ) : null}

      <div className={`stat-main${conLai < 0 ? " neg" : ""}`}>
        <div className="l">{balanceLabel}</div>
        <div className="v">{fmtVnd(conLai)}</div>
      </div>
      <div className="stat-row">
        <div className="stat">
          <div className="l">Tổng thu</div>
          <div className="v in">{fmtCompact(thu)}</div>
        </div>
        <div className="stat">
          <div className="l">Tổng chi</div>
          <div className="v out">{fmtCompact(chi)}</div>
        </div>
      </div>

      {filtered.length === 0 ? (
        <EmptyState title="Tháng này chưa có khoản nào" />
      ) : (
        <div className="card ledger">
          {filtered.map((r) => {
            const sub = [showDate(r.ngay), (r.ghi_chu || "").trim()].filter(Boolean).join(" · ");
            return (
              <div key={r.id} className="lrow">
                <div className="lr-main">
                  <div className="lr-title">{r.noi_dung}</div>
                  <div className="lr-sub">{sub}</div>
                </div>
                <div>
                  {r._thu ? <div className="lr-amt in">+{fmtVnd(r._thu)}</div> : null}
                  {r._chi ? <div className="lr-amt out">−{fmtVnd(r._chi)}</div> : null}
                </div>
              </div>
            );
          })}
        </div>
      )}
    </>
  );
}
