import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [(react as any)()],
  server: {
    proxy: {
      "/api": {
        target: "http://inventario:8000",
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ""),
      },
      "/app": {
        target: "http://pedidos:8001",
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/app/, ""),
      },
    },
  },
});
