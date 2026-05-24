// @ts-check
import { defineConfig } from "astro/config";
import mdx from "@astrojs/mdx";
import tailwindcss from "@tailwindcss/vite";
import sitemap from "@astrojs/sitemap";

// Determine site URL based on environment
const getSiteUrl = () => {
  // On Vercel, both preview and production deployments set VERCEL_URL
  // For preview deployments, use VERCEL_BRANCH_URL if available (newer Vercel versions)
  if (process.env.VERCEL_BRANCH_URL) {
    console.log("[astro] Using VERCEL_BRANCH_URL:", process.env.VERCEL_BRANCH_URL);
    return `https://${process.env.VERCEL_BRANCH_URL}`;
  }
  // Production Vercel deployments use VERCEL_URL
  if (process.env.VERCEL_URL) {
    const url = `https://${process.env.VERCEL_URL}`;
    console.log("[astro] Using VERCEL_URL:", url);
    return url;
  }
  // Custom dev environment variable
  if (process.env.SITE_URL) {
    console.log("[astro] Using SITE_URL:", process.env.SITE_URL);
    return process.env.SITE_URL;
  }
  // Default to production
  console.log("[astro] Using default production URL");
  return "https://2026.pycon.org.au";
};

// https://astro.build/config
export default defineConfig({
  site: getSiteUrl(),
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