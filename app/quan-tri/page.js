import { isAdmin, isUsingDefaultPassword } from "@/lib/auth";
import { PAGES } from "@/lib/pages-config";
import { Flash, PageHeader } from "@/app/components/ui";
import AdminPicker from "@/app/components/AdminPicker";
import AdminSheetEditor from "@/app/components/AdminSheetEditor";
import { loginAction, logoutAction, restoreAction } from "./actions";

export const dynamic = "force-dynamic";

function BackupPanel() {
  return (
    <>
      <p style={{ fontSize: 12.5, color: "var(--muted)", lineHeight: 1.5 }}>
        Dữ liệu được lưu trong cơ sở dữ liệu Postgres của dự án trên Vercel, không mất khi triển khai lại. Vẫn
        nên tải file sao lưu định kỳ để phòng trường hợp cần khôi phục.
      </p>
      <a className="btn-link" href="/quan-tri/backup">
        ⬇️ Tải file Excel sao lưu
      </a>
      <div className="sec">
        <b>Khôi phục từ file sao lưu</b>
      </div>
      <form className="form-card" action={restoreAction} encType="multipart/form-data">
        <div className="field">
          <label>Chọn file .xlsx (toàn bộ dữ liệu hiện tại sẽ bị thay thế)</label>
          <input type="file" name="file" accept=".xlsx" required />
        </div>
        <button className="btn-primary" type="submit">
          Khôi phục dữ liệu
        </button>
      </form>
    </>
  );
}

export default async function Page({ searchParams }) {
  const admin = isAdmin();
  
  // ⭐️ ĐÃ SỬA: Await searchParams để tương thích hoàn toàn với Next.js mới
  const sp = await searchParams;
  const sheet = sp?.sheet || "thongbao";

  return (
    <>
      <PageHeader page={PAGES["quan-tri"]} />
      {sp?.error ? <div className="alert error">{decodeURIComponent(sp.error)}</div> : null}
      <Flash searchParams={sp} />

      {!admin ? (
        <form className="form-card" action={loginAction}>
          <div className="field">
            <label>Mật khẩu cán bộ</label>
            <input type="password" name="password" required />
          </div>
          <button className="btn-primary" type="submit">
            Đăng nhập
          </button>
        </form>
      ) : (
        <>
          {isUsingDefaultPassword() ? (
            <div className="alert warning">
              Đang dùng mật khẩu mặc định. Hãy đặt biến môi trường <code>ADMIN_PASSWORD</code> trên Vercel để bảo mật hơn.
            </div>
          ) : null}
          <form action={logoutAction} style={{ marginBottom: 14 }}>
            <button className="btn-secondary" type="submit">
              Đăng xuất
            </button>
          </form>

          <AdminPicker current={sheet} />

          {sheet === "backup" ? <BackupPanel /> : <AdminSheetEditor table={sheet} />}
        </>
      )}
    </>
  );
}
