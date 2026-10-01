import { getAll } from "@/lib/db";

export default async function AdminSummaryView() {
  const rows = await getAll("dang_ky", { orderBy: "id", desc: true });

  const totalRegistered = rows.length;
  const totalAttended = rows.filter((r) => r.trang_thai === "Đã tham gia").length;
  const totalAbsent = rows.filter((r) => r.trang_thai === "Vắng mặt").length;

  return (
    <div style={{ marginBottom: 24 }}>
      <div className="sec">
        <b>📊 Tổng hợp danh sách họp cuối năm &amp; bình xét đánh giá</b>
      </div>

      {/* Thẻ thống kê nhanh */}
      <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: 12, marginBottom: 16 }}>
        <div className="form-card" style={{ textAlign: "center", padding: "12px", margin: 0 }}>
          <div style={{ fontSize: 22, fontWeight: "bold", color: "var(--primary)" }}>{totalRegistered}</div>
          <div style={{ fontSize: 12, color: "var(--muted)" }}>Tổng số hộ đăng ký</div>
        </div>
        <div className="form-card" style={{ textAlign: "center", padding: "12px", margin: 0 }}>
          <div style={{ fontSize: 22, fontWeight: "bold", color: "#137333" }}>{totalAttended}</div>
          <div style={{ fontSize: 12, color: "var(--muted)" }}>Đã tham gia họp</div>
        </div>
        <div className="form-card" style={{ textAlign: "center", padding: "12px", margin: 0 }}>
          <div style={{ fontSize: 22, fontWeight: "bold", color: "#c5221f" }}>{totalAbsent}</div>
          <div style={{ fontSize: 12, color: "var(--muted)" }}>Vắng mặt</div>
        </div>
      </div>

      {/* Bảng tổng hợp chi tiết */}
      <div className="form-card" style={{ overflowX: "auto", margin: 0 }}>
        <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 13.5 }}>
          <thead>
            <tr style={{ borderBottom: "2px solid #eaeaea", textAlign: "left" }}>
              <th style={{ padding: "8px" }}>STT</th>
              <th style={{ padding: "8px" }}>Hộ gia đình</th>
              <th style={{ padding: "8px" }}>Số người</th>
              <th style={{ padding: "8px" }}>Trạng thái</th>
              <th style={{ padding: "8px" }}>Ghi chú / Đánh giá</th>
            </tr>
          </thead>
          <tbody>
            {rows.length === 0 ? (
              <tr>
                <td colSpan="5" style={{ textAlign: "center", padding: "20px", color: "var(--muted)" }}>
                  Chưa có dữ liệu đăng ký họp nào.
                </td>
              </tr>
            ) : (
              rows.map((row, index) => (
                <tr key={row.id} style={{ borderBottom: "1px solid #f2f2f2" }}>
                  <td style={{ padding: "8px" }}>{index + 1}</td>
                  <td style={{ padding: "8px", fontWeight: 500 }}>{row.ho_gia_dinh}</td>
                  <td style={{ padding: "8px" }}>{row.so_nguoi_tham_gia}</td>
                  <td style={{ padding: "8px" }}>
                    <span
                      style={{
                        padding: "2px 8px",
                        borderRadius: "4px",
                        fontSize: "11.5px",
                        background:
                          row.trang_thai === "Đã tham gia"
                            ? "#e6f4ea"
                            : row.trang_thai === "Vắng mặt"
                            ? "#fce8e6"
                            : "#f1f3f4",
                        color:
                          row.trang_thai === "Đã tham gia"
                            ? "#137333"
                            : row.trang_thai === "Vắng mặt"
                            ? "#c5221f"
                            : "#3c4043",
                      }}
                    >
                      {row.trang_thai || "Đăng ký tham gia"}
                    </span>
                  </td>
                  <td style={{ padding: "8px", color: "var(--muted)" }}>{row.ghi_chu}</td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
