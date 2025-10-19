// @ts-check
import { defineConfig } from "astro/config"
import mdx from "@astrojs/mdx"
import tailwind from "@astrojs/tailwind"

// https://astro.build/config
export default defineConfig({
  site: 'https://2026.pycon.org.au',
  markdown: {
    syntaxHighlight: "prism",
  },
  integrations: [
    mdx(),
    tailwind({
      applyBaseStyles: false, // We'll use our own base styles
    }),
  ],
  redirects: {
    // Add any necessary redirects here
  },
})
