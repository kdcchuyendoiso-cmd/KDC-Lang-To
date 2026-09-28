"use server";

import { redirect } from "next/navigation";
import { insertRow } from "@/lib/db";
import { cleanPhone, todayStr, validPhone } from "@/lib/helpers";

export async function submitProduct(formData) {
  const ten = String(formData.get("ten_san_pham") || "").trim();
  const loai = String(formData.get("phan_loai") || "").trim();
  const gia = Math.max(0, Number.parseInt(formData.get("gia_ban"), 10) || 0);
  const donVi = String(formData.get("don_vi") || "").trim();
  const sdt = String(formData.get("so_dien_thoai") || "").trim();

  if (!ten) {
    redirect(`/cho-que?tab=post&flash=warning:${encodeURIComponent("Vui lòng nhập tên sản phẩm.")}`);
  }
  if (!validPhone(sdt)) {
    redirect(
      `/cho-que?tab=post&flash=warning:${encodeURIComponent("Số điện thoại chưa đúng, vui lòng nhập lại (9-11 chữ số).")}`
    );
  }

  await insertRow("cho_que", {
    ten_san_pham: ten,
    phan_loai: loai,
    gia_ban: String(gia),
    don_vi: donVi,
    so_dien_thoai: cleanPhone(sdt),
    ngay_dang: todayStr(),
  });

  redirect(
    `/cho-que?tab=view&flash=success:${encodeURIComponent("Đã đăng bán sản phẩm. Bà con có thể xem ở tab 'Xem nông sản'.")}`
  );
}
