/** @type {import('next').NextConfig} */
const nextConfig = {
  typescript: {
    // ⚠️ Ignore Type Errors during deployment
    ignoreBuildErrors: true,
  },
  eslint: {
    // ⚠️ Ignore Linting Errors during deployment
    ignoreDuringBuilds: true,
  },
};

export default nextConfig;