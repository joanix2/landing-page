import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  server: {
    host: "0.0.0.0",
    port: 3000,
    allowedHosts: [
      "axynis.cloud",
      ".axynis.cloud", // Permet tous les sous-domaines
      "localhost",
    ],
    hmr: {
      protocol: "wss",
      host: "axynis.cloud",
      clientPort: 443,
    },
  },
});
