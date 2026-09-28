import Link from "next/link";

export function PageHeader({ page }) {
  return (
    <div className="page-head">
      <Link className="back" href="/" aria-label="Về trang chủ">
        ‹
      </Link>
      <div>
        <div className="ph-title">
          {page.icon} {page.title}
        </div>
        <div className="ph-sub">{page.subtitle}</div>
      </div>
    </div>
  );
}

export function EmptyState({ title, hint, icon = "📭" }) {
  return (
    <div className="empty">
      <div className="e-ico">{icon}</div>
      <b>{title}</b>
      {hint ? <span>{hint}</span> : null}
    </div>
  );
}

// Đọc "flash" từ query string (?flash=success:Đã lưu) và hiển thị banner.
// Dùng khi Server Action redirect về trang sau khi submit form, tương tự
// flash()/show_flash() bằng session_state trong bản Streamlit cũ.
export function Flash({ searchParams }) {
  const raw = searchParams?.flash;
  if (!raw) return null;
  const idx = raw.indexOf(":");
  const kind = idx === -1 ? "info" : raw.slice(0, idx);
  const message = idx === -1 ? raw : decodeURIComponent(raw.slice(idx + 1));
  const cls = ["success", "warning", "error"].includes(kind) ? kind : "success";
  return <div className={`alert ${cls}`}>{message}</div>;
}

export function flashHref(path, kind, message) {
  return `${path}?flash=${kind}:${encodeURIComponent(message)}`;
}
