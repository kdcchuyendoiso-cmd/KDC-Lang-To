"use server";

import { redirect } from "next/navigation";
import { getAll, insertRow } from "@/lib/db";
import { parseDate, statusClass, todayStr } from "@/lib/helpers";

export async function submitBooking(formData) {
  const hoTen = String(formData.get("ho_ten") || "").trim();
  const dichVu = String(formData.get("dich_vu") || "").trim();
  const ngay = String(formData.get("ngay_su_dung") || "").trim();
  const mucDich = String(formData.get("muc_dich") || "").trim();

  if (!hoTen) {
    redirect(`/dat-lich?flash=warning:${encodeURIComponent("Vui lòng nhập họ và tên người đăng ký.")}`);
  }

  const existing = await getAll("dat_lich_nha_van_hoa");
  const targetDate = parseDate(ngay)?.getTime();
  const busy = existing.some(
    (r) =>
      (r.dich_vu || "").trim() === dichVu &&
      parseDate(r.ngay_su_dung)?.getTime() === targetDate &&
      statusClass(r.trang_thai) !== "bad"
  );

  await insertRow("dat_lich_nha_van_hoa", {
    ho_ten: hoTen,
    dich_vu: dichVu,
    ngay_su_dung: ngay,
    muc_dich: mucDich,
    trang_thai: "Chờ duyệt",
  });

  const msg = busy
    ? "Đã gửi yêu cầu. Lưu ý: ngày này đã có người đăng ký cùng dịch vụ, cán bộ sẽ liên hệ để sắp xếp."
    : "Đã gửi yêu cầu đặt lịch. Vui lòng chờ cán bộ duyệt.";
  const kind = busy ? "warning" : "success";
  redirect(`/dat-lich?flash=${kind}:${encodeURIComponent(msg)}`);
}
