import crypto from "crypto";
import { cookies } from "next/headers";

const COOKIE_NAME = "kdc_admin";
const DEFAULT_PASSWORD = "admin123";
const MAX_AGE = 60 * 60 * 8; // 8 giờ, giống một phiên làm việc

function adminPassword() {
  return process.env.ADMIN_PASSWORD || DEFAULT_PASSWORD;
}

export function isUsingDefaultPassword() {
  return !process.env.ADMIN_PASSWORD;
}

function sessionToken() {
  // Token suy ra từ mật khẩu hiện tại: đổi ADMIN_PASSWORD sẽ tự đăng xuất mọi phiên cũ.
  return crypto.createHash("sha256").update("kdc-langto-session:" + adminPassword()).digest("hex");
}

export function checkPassword(password) {
  const given = Buffer.from(String(password || ""), "utf8");
  const real = Buffer.from(adminPassword(), "utf8");
  if (given.length !== real.length) return false;
  return crypto.timingSafeEqual(given, real);
}

export function setAdminSession() {
  cookies().set(COOKIE_NAME, sessionToken(), {
    httpOnly: true,
    sameSite: "lax",
    secure: process.env.NODE_ENV === "production",
    path: "/",
    maxAge: MAX_AGE,
  });
}

export function clearAdminSession() {
  cookies().delete(COOKIE_NAME);
}

export function isAdmin() {
  const val = cookies().get(COOKIE_NAME)?.value;
  return Boolean(val) && val === sessionToken();
}
