"use server";

import { redirect } from "next/navigation";
import { insertRow } from "@/lib/db";
import { todayStr } from "@/lib/helpers";

export async function submitFeedback(formData) {
  const nguoiGui = String(formData.get("nguoi_gui") || "").trim();
  const linhVuc = String(formData.get("linh_vuc") || "").trim();
  const noiDung = String(formData.get("noi_dung") || "").trim();
  const diaDiem = String(formData.get("dia_diem") || "").trim();

  if (!nguoiGui || !noiDung) {
    redirect(`/phan-anh?flash=warning:${encodeURIComponent("Vui lòng điền họ tên và nội dung phản ánh.")}`);
  }

  await insertRow("phan_anh", {
    nguoi_gui: nguoiGui,
    linh_vuc: linhVuc,
    noi_dung: noiDung,
    dia_diem: diaDiem,
    ngay_gui: todayStr(),
    trang_thai: "Chờ xử lý",
  });

  redirect(`/phan-anh?flash=success:${encodeURIComponent("Đã gửi phản ánh đến cán bộ thôn. Cảm ơn bà con!")}`);
}
