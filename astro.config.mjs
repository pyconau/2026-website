// @ts-check
import { defineConfig } from "astro/config"
import mdx from "@astrojs/mdx"

// https://astro.build/config
export default defineConfig({
  markdown: {
    syntaxHighlight: "prism",
  },
  integrations: [mdx()],
  redirects: {
    // Add any necessary redirects here
  },
})
