"use client";

import { TABLE_ORDER, TABLES } from "@/lib/schema";

export default function AdminPicker({ current }) {
  return (
    <select
      className="admin-select"
      value={current}
      onChange={(e) => {
        const value = e.target.value;
        // Dùng window.location.href để ép tải lại hoàn toàn, loại bỏ triệt để cache cũ của Next.js
        window.location.href = `/quan-tri?sheet=${value}`;
      }}
    >
      {TABLE_ORDER.map((t) => (
        <option key={t} value={t}>
          {TABLES[t].icon} {TABLES[t].label}
        </option>
      ))}
      <option value="backup">🗄️ Sao lưu &amp; khôi phục</option>
    </select>
  );
}
