"""CSS giao diện ưu tiên điện thoại. Nhúng vào trang bằng st.markdown(<style>...)."""

APP_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;500;600;700;800&display=swap');

:root{ color-scheme: light; ... }
/* Các dòng CSS khác của bạn */
"""
  --brand:#2559d8; --brand-dark:#17346b; --brand-soft:#e6efff;
  --bg:#f2f5fa; --card:#ffffff; --ink:#0f1b33; --muted:#5f6f89; --line:#e3e9f3;
  --ok:#2b8552; --ok-soft:#dff4e8; --bad:#d64545; --bad-soft:#fde6e4;
  --warn:#9a5f03; --warn-soft:#fff1d1;
  --radius:18px;
  --shadow:0 1px 2px rgba(15,27,51,.05), 0 8px 22px rgba(15,27,51,.06);
}

/* ---------- nền tảng ---------- */
html, body, .stApp, .stApp p, .stApp label, .stApp input, .stApp textarea, .stApp button,
.stApp li, .stApp h1, .stApp h2, .stApp h3, .stApp [data-baseweb="select"] *,
.stApp [data-testid="stMarkdownContainer"]{
  font-family:'Be Vietnam Pro', system-ui, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif !important;
}
html{ -webkit-text-size-adjust:100%; }
.stApp{ background:var(--bg); color:var(--ink); }

/* ẩn phần thừa của Streamlit để giống một ứng dụng */
#MainMenu, footer, [data-testid="stToolbar"], [data-testid="stDecoration"],
[data-testid="stStatusWidget"], [data-testid="stAppDeployButton"]{ display:none !important; }
[data-testid="stHeader"]{ background:transparent !important; height:0 !important; min-height:0 !important; }

.block-container{
  max-width:560px !important;
  padding:.9rem .9rem 108px !important;
}
[data-testid="stVerticalBlock"]{ gap:.65rem; }

/* ---------- liên kết do mình tạo ---------- */
.stApp a.tile, .stApp a.chip, .stApp a.back, .stApp a.callbtn, .stApp a.btn-link,
.stApp .bottom-nav a, .stApp .sec a, .stApp .admin-link a{ text-decoration:none !important; }

/* ---------- trang chủ ---------- */
.hero{
  position:relative; overflow:hidden; color:#fff; border-radius:24px; padding:22px 20px 18px;
  background:linear-gradient(140deg, var(--brand-dark) 0%, #1f4fc4 62%, #3d84f0 100%);
  box-shadow:0 14px 30px rgba(23,52,107,.28);
}
.hero::after{
  content:""; position:absolute; right:-36px; top:-36px; width:150px; height:150px;
  border-radius:50%; background:rgba(255,255,255,.11);
}
.hero-mark{ font-size:30px; line-height:1; }
.hero-title{ font-size:23px; font-weight:800; line-height:1.2; margin:10px 0 4px; }
.hero-sub{ font-size:13.5px; line-height:1.5; opacity:.92; max-width:30ch; }
.chips{ display:flex; flex-wrap:wrap; gap:8px; margin-top:14px; position:relative; z-index:1; }
.stApp a.chip{
  background:rgba(255,255,255,.16); border:1px solid rgba(255,255,255,.3); border-radius:999px;
  padding:6px 12px; font-size:12.5px; font-weight:600; color:#fff !important;
}

.sec{ display:flex; align-items:baseline; justify-content:space-between; margin:20px 2px 8px; }
.sec b{ font-size:15px; font-weight:700; }
.stApp .sec a{ font-size:12.5px; font-weight:600; color:var(--brand) !important; }

.grid3{ display:grid; grid-template-columns:repeat(3, minmax(0,1fr)); gap:10px; margin:16px 0 4px; }
.stApp a.tile{
  display:flex; flex-direction:column; align-items:center; gap:9px; padding:15px 4px 12px;
  background:var(--card); border:1px solid var(--line); border-radius:var(--radius);
  box-shadow:var(--shadow); color:var(--ink) !important; -webkit-tap-highlight-color:transparent;
  transition:transform .12s ease;
}
.stApp a.tile:active{ transform:scale(.96); }
.tile .ico{ width:50px; height:50px; border-radius:16px; display:grid; place-items:center; font-size:25px; }
.tile .lbl{ font-size:12.5px; font-weight:700; text-align:center; line-height:1.2; padding:0 2px; }

.admin-link{ text-align:center; margin:18px 0 6px; }
.stApp .admin-link a{
  display:inline-block; padding:9px 16px; border-radius:999px; font-size:12.5px; font-weight:600;
  color:var(--muted) !important; background:#fff; border:1px solid var(--line);
}
.tip{ text-align:center; color:var(--muted); font-size:12px; line-height:1.5; margin:8px 14px 0; }

/* ---------- đầu trang con ---------- */
.page-head{ display:flex; align-items:center; gap:12px; margin:2px 0 14px; }
.stApp a.back{
  flex:none; width:42px; height:42px; border-radius:14px; background:#fff; border:1px solid var(--line);
  display:grid; place-items:center; font-size:28px; line-height:1; padding-bottom:4px;
  color:var(--ink) !important; box-shadow:var(--shadow);
}
.ph-title{ font-size:18px; font-weight:800; line-height:1.25; }
.ph-sub{ font-size:12.5px; color:var(--muted); margin-top:2px; }

/* ---------- thẻ nội dung ---------- */
.card{
  background:var(--card); border:1px solid var(--line); border-radius:var(--radius);
  padding:14px 15px; margin:0 0 10px; box-shadow:var(--shadow);
}
.card.pinned{ border-color:#f1cf7a; background:linear-gradient(180deg,#fffaea,#fff 55%); }
.card-top{ display:flex; flex-wrap:wrap; gap:6px; }
.card-title{ font-size:15.5px; font-weight:700; line-height:1.35; margin:8px 0 4px; }
.card-title.tight{ margin-top:0; }
.card-body{ font-size:13.5px; line-height:1.6; color:#33435f; overflow-wrap:anywhere; }
.card-meta{ display:flex; flex-wrap:wrap; gap:4px 14px; margin-top:10px; font-size:12px; color:var(--muted); }

.badge{
  display:inline-flex; align-items:center; gap:4px; font-size:11.5px; font-weight:700;
  padding:3px 10px; border-radius:999px; background:var(--brand-soft); color:var(--brand); white-space:nowrap;
}
.badge.ok{ background:var(--ok-soft); color:var(--ok); }
.badge.warn{ background:var(--warn-soft); color:var(--warn); }
.badge.bad{ background:var(--bad-soft); color:var(--bad); }
.badge.gray{ background:#edf0f5; color:var(--muted); }

.row-card{ display:flex; align-items:center; gap:12px; }
.rc-main{ flex:1; min-width:0; }
.rc-main .card-meta{ margin-top:4px; }

.cal{
  flex:none; width:52px; padding:8px 0 7px; border-radius:14px; text-align:center;
  background:var(--brand-soft); color:var(--brand);
}
.cal b{ display:block; font-size:21px; line-height:1; font-weight:800; }
.cal span{ display:block; font-size:11px; font-weight:700; margin-top:3px; }
.cal.alt{ font-size:24px; padding:11px 0; }

.stApp a.btn-link{
  display:flex; align-items:center; justify-content:center; margin-top:12px; padding:12px 14px;
  border-radius:13px; background:var(--brand); color:#fff !important; font-weight:700; font-size:14px;
}

/* danh bạ */
.person{ display:flex; align-items:center; gap:12px; }
.avatar{
  flex:none; width:46px; height:46px; border-radius:50%; display:grid; place-items:center;
  color:#fff; font-weight:800; font-size:15px; background:linear-gradient(135deg,#3d84f0,#17346b);
}
.person .info{ flex:1; min-width:0; }
.person .name{ font-size:14.5px; font-weight:700; line-height:1.3; }
.person .role{ font-size:12.5px; color:var(--muted); margin-top:1px; }
.person .phone{ font-size:12.5px; color:var(--ink); margin-top:2px; font-weight:600; }
.stApp a.callbtn{
  flex:none; display:inline-flex; align-items:center; gap:6px; padding:10px 15px; border-radius:999px;
  background:var(--ok); color:#fff !important; font-weight:700; font-size:13px;
}

/* thu chi */
.stat-main{
  border-radius:20px; padding:16px 18px; color:#fff;
  background:linear-gradient(140deg,var(--brand-dark),#1f4fc4);
}
.stat-main.neg{ background:linear-gradient(140deg,#8f2323,#d64545); }
.stat-main .l{ font-size:12.5px; opacity:.88; }
.stat-main .v{ font-size:28px; font-weight:800; margin-top:2px; letter-spacing:-.01em; }
.stat-row{ display:grid; grid-template-columns:1fr 1fr; gap:10px; margin:10px 0 14px; }
.stat{ background:var(--card); border:1px solid var(--line); border-radius:16px; padding:12px 14px; }
.stat .l{ font-size:12px; color:var(--muted); }
.stat .v{ font-size:18px; font-weight:800; margin-top:2px; }
.stat .v.in, .lr-amt.in{ color:var(--ok); }
.stat .v.out, .lr-amt.out{ color:var(--bad); }
.ledger{ padding:4px 15px; }
.lrow{ display:flex; justify-content:space-between; gap:12px; padding:12px 0; border-bottom:1px solid var(--line); }
.lrow:last-child{ border-bottom:0; }
.lr-main{ min-width:0; }
.lr-title{ font-size:14px; font-weight:600; line-height:1.4; overflow-wrap:anywhere; }
.lr-sub{ font-size:12px; color:var(--muted); margin-top:2px; }
.lr-amt{ flex:none; text-align:right; font-size:14px; font-weight:800; white-space:nowrap; line-height:1.5; }

/* vinh danh */
.honor{ display:flex; gap:13px; align-items:flex-start; }
.trophy{
  flex:none; width:48px; height:48px; border-radius:15px; display:grid; place-items:center; font-size:25px;
  background:linear-gradient(135deg,#ffe9a8,#f6c445);
}
.h-info{ flex:1; min-width:0; }
.h-name{ font-size:15px; font-weight:700; line-height:1.3; }
.h-title{ font-size:12.5px; font-weight:700; color:var(--warn); margin-top:2px; }
.h-reason{ font-size:13px; color:#33435f; line-height:1.55; margin-top:6px; }

/* chợ quê */
.prod-top{ display:flex; justify-content:space-between; align-items:flex-start; gap:10px; }
.price{ font-size:18px; font-weight:800; color:var(--ok); white-space:nowrap; margin-top:6px; }
.price small{ font-size:12px; font-weight:600; color:var(--muted); }

/* trạng thái rỗng */
.empty{
  text-align:center; padding:34px 18px; background:#fff; border:1px dashed #c4d0e4;
  border-radius:var(--radius); color:var(--muted); font-size:13px; line-height:1.5;
}
.empty .e-ico{ font-size:34px; margin-bottom:6px; }
.empty b{ display:block; color:var(--ink); font-size:15px; margin-bottom:3px; }

/* ---------- thanh điều hướng dưới ---------- */
.bottom-nav{
  position:fixed; left:50%; bottom:0; transform:translateX(-50%); z-index:999;
  width:min(100%, 560px); display:grid; grid-template-columns:repeat(5, 1fr); gap:2px;
  padding:6px 6px calc(6px + env(safe-area-inset-bottom));
  background:rgba(255,255,255,.95); -webkit-backdrop-filter:blur(12px); backdrop-filter:blur(12px);
  border-top:1px solid var(--line); box-shadow:0 -8px 22px rgba(15,27,51,.06);
}
.bottom-nav a{
  display:flex; flex-direction:column; align-items:center; gap:3px; padding:7px 0 6px; border-radius:13px;
  color:var(--muted) !important; font-size:10.5px; font-weight:600; -webkit-tap-highlight-color:transparent;
}
.bottom-nav a .i{ font-size:20px; line-height:1; }
.bottom-nav a.on{ color:var(--brand) !important; background:var(--brand-soft); font-weight:700; }

/* ---------- ô nhập liệu, nút bấm của Streamlit ---------- */
.stApp input, .stApp textarea{ font-size:16px !important; }   /* 16px: iPhone không tự phóng to khi chạm vào ô */
.stApp [data-baseweb="input"], .stApp [data-baseweb="base-input"],
.stApp [data-baseweb="textarea"], .stApp [data-baseweb="select"] > div{ border-radius:12px !important; }
.stApp [data-testid="stWidgetLabel"] p{ font-size:13.5px !important; font-weight:600; color:#2a3a57; }

[data-testid="stForm"]{
  background:#fff; border:1px solid var(--line) !important; border-radius:var(--radius) !important;
  padding:16px !important; box-shadow:var(--shadow);
}
.stApp .stButton > button, .stApp [data-testid="stDownloadButton"] > button,
.stApp [data-testid="stFormSubmitButton"] > button{
  width:100%; min-height:48px; border-radius:14px; font-weight:700; border:1px solid var(--line);
}
.stApp [data-testid="stFormSubmitButton"] > button{
  background:var(--brand); border-color:var(--brand); color:#fff;
}
.stApp [data-testid="stFormSubmitButton"] > button p{ color:#fff !important; font-size:15px; font-weight:700; }
.stApp [data-testid="stFormSubmitButton"] > button:hover{ background:#1c47b4; border-color:#1c47b4; }
.stApp [data-testid="stAlert"]{ border-radius:14px; }
.stApp [data-testid="stExpander"]{ border-radius:14px; background:#fff; }
.stApp button[data-baseweb="tab"]{ font-weight:700; }

@media (max-width:370px){
  .tile .lbl{ font-size:11.5px; }
  .hero-title{ font-size:21px; }
  .bottom-nav a{ font-size:10px; }
}
@media (prefers-reduced-motion:reduce){ *{ transition:none !important; } }
"""
