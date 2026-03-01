// @ts-check
import { defineConfig } from "astro/config";
import mdx from "@astrojs/mdx";
import tailwindcss from "@tailwindcss/vite";
import sitemap from "@astrojs/sitemap";

// https://astro.build/config
export default defineConfig({
  site: "https://2026.pycon.org.au",
  markdown: {
    syntaxHighlight: "prism",
  },
  integrations: [mdx(), sitemap()],
  redirects: {
    "/student-showcase": "/cfp/student-showcase",
  },
  vite: {
    plugins: [tailwindcss()],
  },
});