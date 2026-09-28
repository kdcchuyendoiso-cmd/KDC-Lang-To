import { Pool } from "pg";
import * as XLSX from "xlsx";
import { TABLES, TABLE_ORDER, columnKeys, LEGACY_SHEET_NAMES } from "./schema";

// Một pool duy nhất cho mỗi tiến trình (được giữ lại giữa các lần gọi khi lambda "nóng").
let pool;
function getPool() {
  if (!pool) {
    const connectionString =
      process.env.POSTGRES_URL || process.env.DATABASE_URL || process.env.POSTGRES_URL_NON_POOLING;
    if (!connectionString) {
      throw new Error(
        "Chưa cấu hình POSTGRES_URL. Vào Vercel → Storage → Create Database (Postgres/Neon) rồi Connect vào project này."
      );
    }
    const needsSsl = !/localhost|127\.0\.0\.1/.test(connectionString);
    pool = new Pool({
      connectionString,
      ssl: needsSsl ? { rejectUnauthorized: false } : undefined,
      max: 5,
    });
  }
  return pool;
}

async function query(text, params) {
  return getPool().query(text, params);
}

// Trên môi trường serverless, mỗi lambda "nóng" giữ biến này giữa các lần gọi
// nên chỉ cần tạo bảng một lần cho mỗi tiến trình.
let schemaReady = false;

export async function ensureSchema() {
  if (schemaReady) return;
  for (const table of TABLE_ORDER) {
    const cols = columnKeys(table);
    const colsSql = cols.map((c) => `"${c}" text NOT NULL DEFAULT ''`).join(", ");
    await query(
      `CREATE TABLE IF NOT EXISTS "${table}" (
         id serial PRIMARY KEY,
         ${colsSql},
         created_at timestamptz NOT NULL DEFAULT now()
       )`
    );
  }
  schemaReady = true;
}

export async function getAll(table, { orderBy = "id", desc = false } = {}) {
  await ensureSchema();
  const col = orderBy === "id" ? "id" : `"${orderBy}"`;
  const { rows } = await query(`SELECT * FROM "${table}" ORDER BY ${col} ${desc ? "DESC" : "ASC"}`);
  return rows;
}

export async function insertRow(table, data) {
  await ensureSchema();
  const cols = columnKeys(table).filter((c) => c in data);
  const values = cols.map((c) => String(data[c] ?? ""));
  const placeholders = cols.map((_, i) => `$${i + 1}`).join(", ");
  const colsSql = cols.map((c) => `"${c}"`).join(", ");
  const { rows } = await query(
    `INSERT INTO "${table}" (${colsSql}) VALUES (${placeholders}) RETURNING *`,
    values
  );
  return rows[0];
}

export async function updateRow(table, id, data) {
  await ensureSchema();
  const cols = columnKeys(table).filter((c) => c in data);
  if (!cols.length) return;
  const setSql = cols.map((c, i) => `"${c}" = $${i + 1}`).join(", ");
  const values = cols.map((c) => String(data[c] ?? ""));
  values.push(id);
  await query(`UPDATE "${table}" SET ${setSql} WHERE id = $${values.length}`, values);
}

export async function deleteRow(table, id) {
  await ensureSchema();
  await query(`DELETE FROM "${table}" WHERE id = $1`, [id]);
}

export async function deleteRows(table, ids) {
  if (!ids || !ids.length) return;
  await ensureSchema();
  const placeholders = ids.map((_, i) => `$${i + 1}`).join(", ");
  await query(`DELETE FROM "${table}" WHERE id IN (${placeholders})`, ids);
}

export async function countRows(table) {
  await ensureSchema();
  const { rows } = await query(`SELECT COUNT(*)::int AS n FROM "${table}"`);
  return rows[0].n;
}

// ---------------------------------------------------------------- sự kiện + đăng ký
// Số hộ tham gia mỗi sự kiện được tính lại từ bảng đăng ký (không lưu trùng dữ liệu).
export async function eventsWithCounts() {
  const [events, regs] = await Promise.all([getAll("su_kien"), getAll("dang_ky_su_kien")]);
  const totals = new Map();
  for (const r of regs) {
    const key = (r.ten_su_kien || "").trim();
    if (!key) continue;
    const n = Number.parseFloat(r.so_luong) || 1;
    totals.set(key, (totals.get(key) || 0) + n);
  }
  return events.map((e) => {
    const key = (e.ten_su_kien || "").trim();
    if (totals.has(key)) {
      return { ...e, tong_so_ho_tham_gia: String(Math.trunc(totals.get(key))) };
    }
    return e;
  });
}

// ---------------------------------------------------------------- sao lưu / khôi phục Excel
export async function exportWorkbookBuffer() {
  await ensureSchema();
  const wb = XLSX.utils.book_new();
  for (const table of TABLE_ORDER) {
    const cols = TABLES[table].columns;
    const rows = await getAll(table);
    const data = rows.map((r) => {
      const obj = {};
      for (const c of cols) obj[c.label] = r[c.key] ?? "";
      return obj;
    });
    const ws = XLSX.utils.json_to_sheet(data, { header: cols.map((c) => c.label) });
    XLSX.utils.book_append_sheet(wb, ws, LEGACY_SHEET_NAMES[table] || table);
  }
  return XLSX.write(wb, { type: "buffer", bookType: "xlsx" });
}

export async function restoreFromBuffer(buffer) {
  let wb;
  try {
    wb = XLSX.read(buffer, { type: "buffer" });
  } catch (exc) {
    throw new Error("Đây không phải file Excel (.xlsx) hợp lệ.");
  }
  const sheetLookup = new Map(wb.SheetNames.map((n) => [n.toLowerCase(), n]));
  const matches = TABLE_ORDER.filter((t) => sheetLookup.has((LEGACY_SHEET_NAMES[t] || t).toLowerCase()));
  if (!matches.length) {
    throw new Error("File không có sheet nào của hệ thống (ThongBao, DanhBaThon, SuKien...).");
  }
  await ensureSchema();
  for (const table of matches) {
    const sheetName = sheetLookup.get((LEGACY_SHEET_NAMES[table] || table).toLowerCase());
    const ws = wb.Sheets[sheetName];
    const json = XLSX.utils.sheet_to_json(ws, { defval: "" });
    const cols = TABLES[table].columns;
    const labelToKey = new Map(cols.map((c) => [c.label.trim().toLowerCase(), c.key]));
    const dataRows = json
      .map((row) => {
        const rec = {};
        for (const [label, value] of Object.entries(row)) {
          const key = labelToKey.get(String(label).trim().toLowerCase());
          if (key) rec[key] = String(value ?? "").trim();
        }
        return rec;
      })
      .filter((rec) => Object.values(rec).some((v) => v));
    await query(`DELETE FROM "${table}"`);
    for (const rec of dataRows) {
      await insertRow(table, rec);
    }
  }
}
