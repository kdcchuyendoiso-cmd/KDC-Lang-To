/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  experimental: {
    serverActions: {
      bodySizeLimit: "10mb", // cho phép tải lên file Excel sao lưu khi khôi phục dữ liệu
    },
  },
};

export default nextConfig;
