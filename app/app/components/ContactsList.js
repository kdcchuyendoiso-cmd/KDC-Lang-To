"use client";

import { useMemo, useState } from "react";
import { cleanPhone, fold, formatPhone, initials, isYes } from "@/lib/helpers";
import { EmptyState } from "@/app/components/ui";

export default function ContactsList({ rows }) {
  const [query, setQuery] = useState("");
  const [onlyOfficers, setOnlyOfficers] = useState(false);

  const filtered = useMemo(() => {
    let list = rows.map((r) => ({ ...r, _off: isYes(r.can_bo) }));
    if (onlyOfficers) list = list.filter((r) => r._off);
    const needle = fold(query);
    if (needle.trim()) {
      list = list.filter((r) => fold(Object.values(r).join(" ")).includes(needle));
    }
    return list.sort((a, b) => Number(b._off) - Number(a._off));
  }, [rows, query, onlyOfficers]);

  if (!rows.length) {
    return <EmptyState title="Danh bạ đang trống" hint="Cán bộ thôn sẽ cập nhật số điện thoại tại đây." />;
  }

  return (
    <>
      <div className="field">
        <input
          placeholder="🔍 Tìm theo tên, chức vụ hoặc số điện thoại"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
      </div>
      <label style={{ display: "flex", alignItems: "center", gap: 8, fontSize: 13.5, fontWeight: 600, margin: "0 2px 12px", color: "#2a3a57" }}>
        <input type="checkbox" checked={onlyOfficers} onChange={(e) => setOnlyOfficers(e.target.checked)} />
        Chỉ hiện cán bộ thôn
      </label>
      {filtered.length === 0 ? (
        <EmptyState title="Không tìm thấy kết quả" hint="Thử gõ tên ngắn hơn hoặc bỏ bộ lọc." icon="🔍" />
      ) : (
        filtered.map((r) => {
          const phone = cleanPhone(r.so_dien_thoai);
          return (
            <div key={r.id} className="card person">
              <div className="avatar">{initials(r.ho_ten)}</div>
              <div className="info">
                <div className="name">
                  {r.ho_ten} {r._off ? <span className="badge">Cán bộ</span> : null}
                </div>
                <div className="role">{r.chuc_vu}</div>
                {phone ? <div className="phone">{formatPhone(phone)}</div> : null}
              </div>
              {phone ? (
                <a className="callbtn" href={`tel:${phone}`}>
                  📞 Gọi
                </a>
              ) : null}
            </div>
          );
        })
      )}
    </>
  );
}
