APP_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;500;600;700;800&display=swap');

:root {
    color-scheme: light;
    --brand: #2559d8;
    --brand-dark: #17346b;
    --brand-soft: #e6efff;
    --bg: #f2f5fa;
    --card: #ffffff;
    --ink: #0f1b33;
    --muted: #5f6f89;
    --line: #e3e9f3;
    --ok: #2b8552;
    --ok-soft: #dff4e8;
    --bad: #d64545;
    --bad-soft: #fde6e4;
    --warn: #9a5f03;
    --warn-soft: #fff1d1;
    --radius: 18px;
    --shadow: 0 1px 2px rgba(15,27,51,.05), 0 8px 22px rgba(15,27,51,.06);
}

html, body, .stApp, .stApp p, .stApp label, .stApp input, .stApp textarea, .stApp button, .stApp li, .stApp h1, .stApp h2, .stApp h3, .stApp [data-baseweb="select"] *, .stApp [data-testid="stMarkdownContainer"] {
    font-family: 'Be Vietnam Pro', system-ui, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif !important;
}

html {
    -webkit-text-size-adjust: 100%;
}

.stApp {
    background: var(--bg);
    color: var(--ink);
}

#MainMenu, footer, [data-testid="stToolbar"], [data-testid="stDecoration"], [data-testid="stStatusWidget"], [data-testid="stAppDeployButton"] {
    display: none !important;
}

[data-testid="stHeader"] {
    background: transparent !important;
    height: 0 !important;
    min-height: 0 !important;
}
"""
