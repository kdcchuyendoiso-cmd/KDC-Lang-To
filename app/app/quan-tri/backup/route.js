import { NextResponse } from "next/server";
import { exportWorkbookBuffer } from "@/lib/db";
import { isAdmin } from "@/lib/auth";

export async function GET() {
  if (!isAdmin()) {
    return NextResponse.json({ error: "Không có quyền truy cập." }, { status: 401 });
  }
  const buffer = await exportWorkbookBuffer();
  const today = new Date();
  const stamp = `${today.getFullYear()}${String(today.getMonth() + 1).padStart(2, "0")}${String(
    today.getDate()
  ).padStart(2, "0")}`;
  return new NextResponse(buffer, {
    headers: {
      "Content-Type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
      "Content-Disposition": `attachment; filename="dulieu_langto_${stamp}.xlsx"`,
    },
  });
}
