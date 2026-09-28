"use server";

import { redirect } from "next/navigation";
import { deleteRow, insertRow, restoreFromBuffer, updateRow } from "@/lib/db";
import { checkPassword, clearAdminSession, isAdmin, setAdminSession } from "@/lib/auth";
import { TABLES } from "@/lib/schema";

export async function loginAction(formData) {
  const password = String(formData.get("password") || "");
  if (!checkPassword(password)) {
    // Trễ một chút để hạn chế dò mật khẩu tự động, giống time.sleep(1) ở bản cũ.
    await new Promise((r) => setTimeout(r, 800));
    redirect(`/quan-tri?error=${encodeURIComponent("Mật khẩu chưa đúng. Vui lòng thử lại.")}`);
  }
  setAdminSession();
  redirect("/quan-tri");
}

export async function logoutAction() {
  clearAdminSession();
  redirect("/quan-tri");
}

function requireAdmin() {
  if (!isAdmin()) {
    redirect("/quan-tri");
  }
}

export async function saveRowAction(formData) {
  requireAdmin();
  const table = String(formData.get("table") || "");
  const config = TABLES[table];
  if (!config) redirect("/quan-tri");

  const id = String(formData.get("id") || "").trim();
  const record = {};
  for (const col of config.columns) {
    record[col.key] = String(formData.get(`col__${col.key}`) || "").trim();
  }

  if (id) {
    await updateRow(table, id, record);
  } else {
    // Bỏ dòng thêm mới hoàn toàn trống.
    if (Object.values(record).some((v) => v)) {
      await insertRow(table, record);
    }
  }
  redirect(`/quan-tri?sheet=${table}&flash=${encodeURIComponent("Đã lưu thay đổi.")}`);
}

export async function deleteRowAction(formData) {
  requireAdmin();
  const table = String(formData.get("table") || "");
  const id = String(formData.get("id") || "");
  if (TABLES[table] && id) {
    await deleteRow(table, id);
  }
  redirect(`/quan-tri?sheet=${table}&flash=${encodeURIComponent("Đã xóa dòng dữ liệu.")}`);
}

export async function restoreAction(formData) {
  requireAdmin();
  const file = formData.get("file");
  if (!file || typeof file === "string" || !file.size) {
    redirect(`/quan-tri?sheet=backup&error=${encodeURIComponent("Vui lòng chọn file .xlsx để khôi phục.")}`);
  }
  const buffer = Buffer.from(await file.arrayBuffer());
  try {
    await restoreFromBuffer(buffer);
  } catch (exc) {
    redirect(`/quan-tri?sheet=backup&error=${encodeURIComponent(String(exc.message || exc))}`);
  }
  redirect(`/quan-tri?sheet=backup&flash=${encodeURIComponent("Đã khôi phục dữ liệu từ file Excel.")}`);
}
