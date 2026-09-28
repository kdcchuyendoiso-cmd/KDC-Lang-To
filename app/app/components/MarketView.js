"use client";

import { useMemo, useState } from "react";
import { fmtVnd, fold, formatPhone, parseMoney } from "@/lib/helpers";
import { EmptyState } from "@/app/components/ui";
import { submitProduct } from "@/app/cho-que/actions";

export default function MarketView({ rows, initialTab }) {
  const [tab, setTab] = useState(initialTab === "post" ? "post" : "view");

  return (
    <>
      <div className="tabs">
        <a className={tab === "view" ? "on" : ""} onClick={() => setTab("view")} href="#xem">
          🛍️ Xem nông sản
        </a>
        <a className={tab === "post" ? "on" : ""} onClick={() => setTab("post")} href="#dang">
          ➕ Đăng bán
        </a>
      </div>
      {tab === "view" ? <ViewTab rows={rows} /> : <PostTab />}
    </>
  );
}

function ViewTab({ rows }) {
  const [query, setQuery] = useState("");
  const [cat, setCat] = useState("Tất cả loại");
  const cats = useMemo(() => [...new Set(rows.map((r) => (r.phan_loai || "").trim()).filter(Boolean))].sort(), [rows]);

  let list = [...rows].reverse(); // mới đăng lên trước
  if (cat !== "Tất cả loại") list = list.filter((r) => (r.phan_loai || "").trim() === cat);
  if (query.trim()) {
    const needle = fold(query);
    list = list.filter((r) => fold(r.ten_san_pham).includes(needle));
  }

  if (!rows.length) {
    return <EmptyState title="Chợ quê chưa có sản phẩm" hint="Bà con bấm 'Đăng bán' để giới thiệu sản phẩm của nhà mình." icon="🛒" />;
  }

  return (
    <>
      <div className="field">
        <input placeholder="🔍 Tìm sản phẩm" value={query} onChange={(e) => setQuery(e.target.value)} />
      </div>
      {cats.length > 1 ? (
        <select className="admin-select" value={cat} onChange={(e) => setCat(e.target.value)}>
          <option>Tất cả loại</option>
          {cats.map((c) => (
            <option key={c}>{c}</option>
          ))}
        </select>
      ) : null}
      {list.length === 0 ? (
        <EmptyState title="Không tìm thấy sản phẩm" hint="Thử từ khóa khác." icon="🔍" />
      ) : (
        list.map((r) => {
          const price = parseMoney(r.gia_ban);
          const unit = (r.don_vi || "").trim();
          const phone = (r.so_dien_thoai || "").replace(/\D/g, "");
          return (
            <div key={r.id} className="card">
              <div className="prod-top">
                <div>
                  <div className="card-top">
                    {(r.phan_loai || "").trim() ? <span className="badge ok">{r.phan_loai}</span> : null}
                  </div>
                  <div className="card-title">{r.ten_san_pham}</div>
                </div>
                {price > 0 ? (
                  <div className="price">
                    {fmtVnd(price)}
                    {unit ? <small> / {unit}</small> : null}
                  </div>
                ) : (
                  <div className="price">
                    <small>Liên hệ để hỏi giá</small>
                  </div>
                )}
              </div>
              {(r.ngay_dang || "").trim() ? (
                <div className="card-meta">
                  <span>🗓 Đăng ngày {r.ngay_dang}</span>
                </div>
              ) : null}
              {phone ? (
                <a className="btn-link" href={`tel:${phone}`}>
                  📞 Gọi {formatPhone(phone)}
                </a>
              ) : null}
            </div>
          );
        })
      )}
    </>
  );
}

function PostTab() {
  return (
    <form className="form-card" action={submitProduct}>
      <div className="field">
        <label>Tên sản phẩm *</label>
        <input name="ten_san_pham" maxLength={100} required />
      </div>
      <div className="field">
        <label>Phân loại</label>
        <select name="phan_loai" defaultValue="Nông sản">
          {["Nông sản", "Thực phẩm", "Thủ công mỹ nghệ", "Đồ dùng gia đình"].map((o) => (
            <option key={o}>{o}</option>
          ))}
        </select>
      </div>
      <div className="field">
        <label>Giá bán (VNĐ) — để 0 nếu muốn người mua liên hệ để hỏi giá</label>
        <input name="gia_ban" type="number" min={0} step={1000} defaultValue={0} />
      </div>
      <div className="field">
        <label>Đơn vị tính</label>
        <input name="don_vi" placeholder="kg, bó, lít, chục..." maxLength={20} />
      </div>
      <div className="field">
        <label>Số điện thoại liên hệ *</label>
        <input name="so_dien_thoai" placeholder="09xx xxx xxx" maxLength={20} required />
      </div>
      <button className="btn-primary" type="submit">
        Đăng bán sản phẩm
      </button>
    </form>
  );
}
