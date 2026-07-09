// @ts-check
import { defineConfig } from "astro/config";
import mdx from "@astrojs/mdx";
import tailwindcss from "@tailwindcss/vite";
import sitemap from "@astrojs/sitemap";

// Determine site URL based on environment
// Reference: https://vercel.com/docs/projects/environment-variables/system-environment-variables
const getSiteUrl = () => {
  // Vercel preview deployments have VERCEL_BRANCH_URL (format: preview-{code}-{slug}.vercel.app)
  // Main/production deployments have VERCEL_URL pointing to custom domain
  if (process.env.VERCEL_BRANCH_URL && process.env.VERCEL_ENV === "preview") {
    console.log("[astro] Using VERCEL_BRANCH_URL (preview):", process.env.VERCEL_BRANCH_URL);
    return `https://${process.env.VERCEL_BRANCH_URL}`;
  }
  // Fallback: VERCEL_URL is available on all Vercel deployments
  if (process.env.VERCEL_URL) {
    const url = `https://${process.env.VERCEL_URL}`;
    console.log("[astro] Using VERCEL_URL:", url);
    return url;
  }
  // Custom dev environment variable (for local testing)
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
  integrations: [mdx(), sitemap({ filter: (page) => !page.includes("/dev/") })],
  redirects: {
    "/student-showcase": "/cfp/student-showcase",
    "/workshops": "/schedule/workshops",
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