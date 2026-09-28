// Hàm tiện ích thuần JS: định dạng, làm sạch dữ liệu (chuyển từ helpers.py).

const YES_WORDS = new Set([
  "có", "co", "x", "yes", "y", "true", "1", "ghim", "cán bộ", "can bo", "cb", "✓", "✔",
]);

export function isYes(value) {
  return YES_WORDS.has(String(value ?? "").trim().toLowerCase());
}

export function s(value) {
  return String(value ?? "").trim();
}

// Bỏ dấu tiếng Việt + chữ thường, để tìm kiếm "nguyen" vẫn ra "Nguyễn".
export function fold(text) {
  const t = String(text ?? "")
    .toLowerCase()
    .replace(/đ/g, "d");
  return t.normalize("NFD").replace(/[\u0300-\u036f]/g, "");
}

export function initials(name) {
  const parts = s(name).split(/\s+/).filter(Boolean);
  if (!parts.length) return "?";
  if (parts.length === 1) return parts[0][0].toUpperCase();
  return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase();
}

const ISO_RE = /^(\d{4})-(\d{2})-(\d{2})(?:[ T](\d{2}):(\d{2}))?/;

// Chuỗi ngày (ISO "YYYY-MM-DD[ HH:MM]" hoặc "DD/MM/YYYY") -> Date | null
export function parseDate(value) {
  const str = s(value);
  if (!str) return null;
  const iso = ISO_RE.exec(str);
  if (iso) {
    const [, y, mo, d, hh = "00", mm = "00"] = iso;
    const dt = new Date(Number(y), Number(mo) - 1, Number(d), Number(hh), Number(mm));
    return isNaN(dt.getTime()) ? null : dt;
  }
  const dmy = /^(\d{1,2})\/(\d{1,2})\/(\d{4})/.exec(str);
  if (dmy) {
    const [, d, mo, y] = dmy;
    const dt = new Date(Number(y), Number(mo) - 1, Number(d));
    return isNaN(dt.getTime()) ? null : dt;
  }
  const dt = new Date(str);
  return isNaN(dt.getTime()) ? null : dt;
}

export function dateOnlyStr(date) {
  const d = date instanceof Date ? date : new Date(date);
  const y = d.getFullYear();
  const mo = String(d.getMonth() + 1).padStart(2, "0");
  const da = String(d.getDate()).padStart(2, "0");
  return `${y}-${mo}-${da}`;
}

// "2025-06-20 19:00" -> "19:00, 20/06/2025"; các chuỗi khác giữ nguyên.
export function showDate(value) {
  const str = s(value);
  const m = ISO_RE.exec(str);
  if (!m) return str;
  const [, y, mo, d, hh, mm] = m;
  let out = `${d}/${mo}/${y}`;
  if (hh !== undefined && !(hh === "00" && mm === "00")) {
    out = `${hh}:${mm}, ${out}`;
  }
  return out;
}

export function yearOf(value) {
  const m = /\d{4}/.exec(s(value));
  return m ? Number(m[0]) : 0;
}

const GROUPED_RE = /^-?\d{1,3}([.,]\d{3})+$/;

// "1.500.000" / "1,500,000" / "1500000 đ" -> 1500000
export function parseMoney(value) {
  let str = s(value).replace(/[^\d.,-]/g, "");
  if (!str || ["-", ".", ","].includes(str)) return 0;
  if (GROUPED_RE.test(str)) {
    str = str.replace(/[.,]/g, "");
  } else {
    str = str.replace(",", ".");
  }
  const n = parseFloat(str);
  return Number.isFinite(n) ? Math.round(n) : 0;
}

export function fmtVnd(amount) {
  const n = Math.trunc(Number(amount) || 0);
  return n.toLocaleString("vi-VN") + " đ";
}

export function fmtCompact(amount) {
  const n = Number(amount) || 0;
  const a = Math.abs(n);
  const oneDecimal = (v) => {
    const str = v.toFixed(1).replace(".", ",");
    return str.endsWith(",0") ? str.slice(0, -2) : str;
  };
  if (a >= 1_000_000_000) return oneDecimal(n / 1e9) + " tỷ";
  if (a >= 1_000_000) return oneDecimal(n / 1e6) + " triệu";
  return fmtVnd(n);
}

// Chuẩn hoá SĐT Việt Nam: bỏ ký tự lạ, +84 -> 0, bù số 0 nếu thiếu.
export function cleanPhone(value) {
  let digits = s(value).replace(/\D/g, "");
  if (!digits) return "";
  if (digits.startsWith("84") && digits.length >= 11 && digits.length <= 12) {
    digits = "0" + digits.slice(2);
  }
  if (digits.length === 9 && "35789".includes(digits[0])) {
    digits = "0" + digits;
  }
  return digits;
}

export function formatPhone(digits) {
  if (digits.length === 10) return `${digits.slice(0, 4)} ${digits.slice(4, 7)} ${digits.slice(7)}`;
  if (digits.length === 11) return `${digits.slice(0, 4)} ${digits.slice(4, 8)} ${digits.slice(8)}`;
  return digits;
}

export function validPhone(value) {
  const d = cleanPhone(value);
  return d.length >= 9 && d.length <= 11;
}

// Tên trạng thái -> màu huy hiệu (ok / warn / bad / gray).
export function statusClass(status) {
  const t = s(status).toLowerCase();
  if (!t) return "gray";
  if (["từ chối", "hủy", "huỷ", "không duyệt"].some((k) => t.includes(k))) return "bad";
  if (["chờ", "chưa", "đang", "mới", "tiếp nhận"].some((k) => t.includes(k))) return "warn";
  if (["đã", "duyệt", "xong", "hoàn"].some((k) => t.includes(k))) return "ok";
  return "gray";
}

export function todayStr() {
  return dateOnlyStr(new Date());
}
