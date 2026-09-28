"use server";

import { redirect } from "next/navigation";
import { insertRow } from "@/lib/db";
import { todayStr } from "@/lib/helpers";

export async function submitRegistration(formData) {
  const hoTen = String(formData.get("ho_ten") || "").trim();
  const suKien = String(formData.get("su_kien") || "").trim();
  const soLuong = Math.max(1, Math.min(50, Number.parseInt(formData.get("so_luong"), 10) || 1));
  const ghiChu = String(formData.get("ghi_chu") || "").trim();

  if (!hoTen) {
    redirect(`/dang-ky?flash=warning:${encodeURIComponent("Vui lòng nhập họ và tên để cán bộ ghi nhận.")}`);
  }

  await insertRow("dang_ky_su_kien", {
    ho_ten: hoTen,
    ten_su_kien: suKien,
    so_luong: String(soLuong),
    ghi_chu: ghiChu,
    ngay_dang_ky: todayStr(),
  });

  redirect(
    `/dang-ky?flash=success:${encodeURIComponent(`Đã ghi nhận đăng ký của '${hoTen}' cho sự kiện '${suKien}'.`)}`
  );
}
