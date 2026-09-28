import "./globals.css";

export const metadata = {
  title: "Khu dân cư Lăng Tô",
  description: "Cổng thông tin Khu dân cư Lăng Tô",
};

export const viewport = {
  width: "device-width",
  initialScale: 1,
  viewportFit: "cover",
};

export default function RootLayout({ children }) {
  return (
    <html lang="vi">
      <body>
        <div className="shell">{children}</div>
      </body>
    </html>
  );
}
