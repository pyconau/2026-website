// @ts-check
import { readdirSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { defineConfig } from "astro/config";
import mdx from "@astrojs/mdx";
import tailwindcss from "@tailwindcss/vite";
import sitemap from "@astrojs/sitemap";

// Legacy /program/<code>-<variant>.png session graphic URLs were shared (e.g.
// via email) before these moved to /graphics/sessions/. A param redirect can't
// point at a public/ asset (Astro can't enumerate getStaticPaths for it), so
// build one explicit static redirect per known session code instead. Codes are
// the session content filenames.
const sessionsDir = fileURLToPath(new URL("./src/content/sessions", import.meta.url));
const sessionGraphicVariants = ["social", "og", "square"];
const programGraphicRedirects = Object.fromEntries(
  readdirSync(sessionsDir)
    .filter((file) => file.endsWith(".md"))
    .map((file) => file.replace(/\.md$/, ""))
    .flatMap((code) =>
      sessionGraphicVariants.map((variant) => [
        `/program/${code}-${variant}.png`,
        `/graphics/sessions/${code}-${variant}.png`,
      ]),
    ),
);

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
    // Legacy /program/* URLs (e.g. session links shared before the move to
    // /schedule/*) redirect to their /schedule/* equivalents.
    ...programGraphicRedirects,
    "/program/[code]": "/schedule/[code]",
    "/program/specialist-tracks/[...slug]": "/schedule/specialist-tracks/[...slug]",
    // Specialist track shortcuts
    "/data-and-ai": "/schedule/specialist-tracks/data-and-ai",
    "/education": "/schedule/specialist-tracks/education",
    "/cybersecurity": "/schedule/specialist-tracks/cybersecurity",
    "/devrel": "/schedule/specialist-tracks/devrel",
    "/platform-engineering": "/schedule/specialist-tracks/platform-engineering",
    "/research-software-engineering": "/schedule/specialist-tracks/research-software-engineering",
  },
  vite: {
    plugins: [tailwindcss()],
  },
});