import { defineConfig } from "vite";

// Built into mock/dist with relative paths, so the map page can open it in an iframe from the repo
// (web/gidi-maps.html -> ../mock/dist/index.html) and the city data is found at ../../web/.
export default defineConfig({
  base: "./",
  build: { target: "es2022", chunkSizeWarningLimit: 4000 },
  server: { fs: { allow: [".."] } },
});
