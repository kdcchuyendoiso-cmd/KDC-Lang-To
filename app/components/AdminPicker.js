"use client";

import { useRouter } from "next/navigation";
import { TABLE_ORDER, TABLES } from "@/lib/schema";

export default function AdminPicker({ current }) {
  const router = useRouter();
  return (
    <select
      className="admin-select"
      value={current}
      onChange={(e) => router.push(`/quan-tri?sheet=${e.target.value}`)}
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
