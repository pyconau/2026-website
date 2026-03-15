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
    // Specialist track shortcuts
    "/data-and-ai": "/program/specialist-tracks/data-and-ai",
    "/education": "/program/specialist-tracks/education",
    "/cybersecurity": "/program/specialist-tracks/cybersecurity",
    "/devrel": "/program/specialist-tracks/devrel",
    "/platform-engineering": "/program/specialist-tracks/platform-engineering",
    "/research-software-engineering": "/program/specialist-tracks/research-software-engineering",
  },
  vite: {
    plugins: [tailwindcss()],
  },
});