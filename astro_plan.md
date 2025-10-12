# Astro Migration Plan - PyCon AU 2026 Website

## Overview
This document outlines the plan to migrate the current static Vite-based website to Astro, converting the existing `index.html` into a reusable splash layout that can be used for future landing pages.

## Current State Analysis

### Existing Technology Stack
- **Build Tool**: Vite 7.1.2
- **CSS Framework**: Tailwind CSS 4.1.12 with @tailwindcss/vite plugin
- **JavaScript Libraries**:
  - Alpine.js 3.15.0 (for reactive components)
  - GSAP 3.13.0 with ScrollTrigger (for animations)
  - Lottie (loaded via CDN for animation playback)
- **External Dependencies**:
  - Google Fonts (Inter, Manrope, Plus Jakarta Sans, Roboto Slab)
  - Font Awesome 7.0.1
  - Fathom Analytics

### Current Structure
```
/
├── index.html (main landing page)
├── src/
│   ├── style.css (Tailwind configuration and custom styles)
│   └── main.js (GSAP animations and Alpine.js initialization)
├── public/
│   ├── CurlyBoi_Animated.json (Lottie animation)
│   ├── *.svg (various image assets)
│   └── files/ (PDF documents)
├── package.json
└── vite.config.js (assumed to exist)
```

### Key Features in Current Implementation
1. **Hero Section** with:
   - Lottie animation (CurlyBoi) on first visit only (using sessionStorage)
   - GSAP animations for logo and date reveal
   - Smooth scroll functionality
2. **Content Sections**:
   - Conference information with fade-up animations
   - Sponsorship call-to-action
   - Social media links
   - Footer
3. **Interactive Elements**:
   - Alpine.js for scroll functionality
   - GSAP ScrollTrigger for scroll-based animations
   - Session storage to skip animations on return visits
4. **SEO/Metadata**:
   - Schema.org structured data (Event markup)
   - Open Graph tags (implied)
   - Fathom Analytics

## Target State (Based on 2025 Website)

### Astro Technology Stack
- **Framework**: Astro 5.14.4 (latest stable as of October 2025)
- **Content Management**: Astro Content Collections with MDX support (@astrojs/mdx 4.3.6)
- **Styling**: SCSS/Sass 1.93.2
- **TypeScript**: Yes (TypeScript 5.9.3)
- **Additional Tools**:
  - Prettier 3.6.2 with Astro plugin (prettier-plugin-astro 0.14.1) for code formatting
  - Custom utility libraries (execa, jsdom, luxon)

### Proposed Structure
```
/
├── astro.config.mjs
├── tsconfig.json
├── package.json
├── src/
│   ├── env.d.ts
│   ├── layouts/
│   │   ├── Base.astro (base HTML layout)
│   │   ├── Splash.astro (new: converted from index.html)
│   │   └── Page.astro (standard page layout for future pages)
│   ├── pages/
│   │   └── index.astro (uses Splash layout)
│   ├── components/
│   │   ├── HeroSection.astro
│   │   ├── SponsorSection.astro
│   │   ├── SocialLinks.astro
│   │   └── Footer.astro
│   ├── styles/
│   │   ├── global.scss
│   │   └── splash.scss (splash-specific styles)
│   └── scripts/
│       ├── animations.js (GSAP setup)
│       └── alpine-setup.js (Alpine.js initialization)
├── public/ (unchanged)
└── _redirects (for Netlify/deployment)
```

## Migration Steps

### Phase 1: Setup and Configuration

#### 1.1 Install Astro and Dependencies
```bash
# Remove Vite-specific dependencies
npm uninstall vite @tailwindcss/vite

# Install Astro core (latest stable)
npm install --save-dev astro@^5.14.4

# Install Astro integrations
npm install --save-dev @astrojs/mdx@^4.3.6

# Install styling dependencies
npm install --save-dev sass@^1.93.2 typescript@^5.9.3

# Install development tools
npm install --save-dev prettier@^3.6.2 prettier-plugin-astro@^0.14.1

# Keep existing runtime dependencies
# (alpinejs, gsap are already installed)
```

#### 1.2 Create Astro Configuration
Create `astro.config.mjs`:
```javascript
// @ts-check
import { defineConfig } from "astro/config"
import mdx from "@astrojs/mdx"

export default defineConfig({
  markdown: {
    syntaxHighlight: "prism",
  },
  integrations: [mdx()],
  legacy: {
    collections: true, // For compatibility if using older content collections API
  },
  redirects: {
    // Add any necessary redirects here
  },
})
```

#### 1.3 Create TypeScript Configuration
Create `tsconfig.json` (reference 2025 website):
```json
{
  "extends": "astro/tsconfigs/strict",
  "compilerOptions": {
    "target": "ES2022",
    "module": "ES2022",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "allowJs": true,
    "jsx": "preserve"
  }
}
```

#### 1.4 Create Environment Type Definitions
Create `src/env.d.ts`:
```typescript
/// <reference types="astro/client" />
```

#### 1.5 Update package.json Scripts
```json
{
  "scripts": {
    "dev": "astro dev",
    "build": "astro build",
    "preview": "astro preview",
    "start": "astro dev",
    "astro": "astro"
  }
}
```

#### 1.6 Setup Prettier Configuration (Optional but Recommended)
Create `.prettierrc.toml`:
```toml
plugins = ["prettier-plugin-astro"]
```

Create `.prettierignore`:
```
dist/
node_modules/
```

### Phase 2: Convert Styles

#### 2.1 Convert Tailwind CSS to SCSS
Current implementation uses Tailwind v4 with the new `@import "tailwindcss"` syntax. Astro typically works better with traditional Tailwind v3 approach or pure SCSS.

**Option A: Keep Tailwind (Recommended for Minimal Changes)**
- Install Tailwind v3 with PostCSS integration
- Convert `src/style.css` to work with Astro's asset pipeline

**Option B: Convert to Pure SCSS (More Aligned with 2025 Website)**
- Extract Tailwind theme values into SCSS variables
- Convert utility classes to SCSS mixins/extends
- Create `src/styles/global.scss` with base styles
- Create `src/styles/splash.scss` for splash-specific styles

#### 2.2 Create Base Styles Structure
```
src/
├── styles/
│   ├── _variables.scss (colors, fonts, sizes from Tailwind theme)
│   ├── _mixins.scss (button styles, utilities)
│   ├── global.scss (body, common styles)
│   └── splash.scss (splash layout specific)
```

**Action Items:**
- Extract CSS custom properties from `@theme` block into SCSS variables
- Convert `.btn`, `.btn-primary`, etc. into SCSS classes or mixins
- Keep `.bg-separator` and `.bg-pattern` as they are complex utilities

### Phase 3: Create Layout Components

#### 3.1 Create Base Layout (`src/layouts/Base.astro`)
This layout should include:
- HTML document structure
- `<head>` with meta tags
- Font preloads and stylesheets
- Analytics scripts (Fathom)
- Common Schema.org data structure
- Slot for page content

```astro
---
export interface Props {
  title: string;
  description?: string;
  ogImage?: string;
  schemaData?: object;
}

const { title, description, ogImage, schemaData } = Astro.props;
---

<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <link rel="icon" type="image/svg+xml" href="/favicon2.svg" />
    <title>{title}</title>
    {description && <meta name="description" content={description} />}

    <!-- Font preconnects and stylesheets -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:...&display=swap" rel="stylesheet">

    <!-- Font Awesome -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/7.0.1/css/all.min.css" />

    <!-- Fathom Analytics -->
    <script src="https://cdn.usefathom.com/script.js" data-site="BETINVUJ" defer></script>

    <!-- Schema.org structured data -->
    {schemaData && (
      <script type="application/ld+json" set:html={JSON.stringify(schemaData)} />
    )}
  </head>
  <body>
    <slot />
  </body>
</html>
```

#### 3.2 Create Splash Layout (`src/layouts/Splash.astro`)
This layout extends Base.astro and implements the splash page structure:
- Uses Base layout with Schema.org event data
- Includes scripts for Lottie, GSAP, Alpine.js
- Provides named slots for hero, content, footer sections

```astro
---
import Base from './Base.astro';

const schemaData = {
  "@context": "https://schema.org",
  "@type": "Event",
  // ... rest of Schema.org data
};
---

<Base title="PyCon AU 2026" schemaData={schemaData}>
  <slot name="hero" />
  <slot name="content" />
  <slot name="footer" />

  <!-- Lottie -->
  <script src="https://cdnjs.cloudflare.com/ajax/libs/bodymovin/5.11.0/lottie.min.js" crossorigin></script>

  <!-- Main scripts -->
  <script src="/src/scripts/animations.js"></script>
</Base>
```

#### 3.3 Create Page Layout (`src/layouts/Page.astro`)
Standard layout for future content pages (not used initially):
```astro
---
import Base from './Base.astro';

export interface Props {
  title: string;
  description?: string;
}

const { title, description } = Astro.props;
---

<Base title={title} description={description}>
  <main>
    <slot />
  </main>
</Base>
```

### Phase 4: Create Components

#### 4.1 Extract Hero Section (`src/components/HeroSection.astro`)
- Extract hero section HTML from index.html (lines 85-119)
- Keep Alpine.js directives
- Keep GSAP target IDs and classes

#### 4.2 Extract Content Section (`src/components/ContentSection.astro`)
- Extract main content section (lines 121-151)
- Break into sub-components if needed:
  - `IntroCard.astro` (conference intro)
  - `SponsorCallout.astro` (sponsor information)

#### 4.3 Extract Social Links (`src/components/SocialLinks.astro`)
- Extract social section (lines 154-174)
- Consider making links configurable via props

#### 4.4 Extract Footer (`src/components/Footer.astro`)
- Extract footer section (lines 176-188)
- Make copyright year dynamic

### Phase 5: Migrate JavaScript

#### 5.1 Create Animation Script (`src/scripts/animations.js`)
Move content from `src/main.js` with these changes:
- Keep GSAP and ScrollTrigger initialization
- Keep Alpine.js initialization
- Ensure scripts run client-side (use `<script>` tag in Astro, not `<script is:inline>`)
- Maintain sessionStorage logic for first-time visitors

**Astro Integration Options:**
- **Option A**: Keep as external script loaded via `<script>` tag (simpler)
- **Option B**: Use Astro's `<script>` tag with `is:inline` for client-side execution
- **Option C**: Break into smaller, component-specific scripts using `<script>` in components

#### 5.2 Handle Client-Side Dependencies
In Astro, client-side JS needs special handling:
```astro
<!-- In layout or component -->
<script>
  import Alpine from 'alpinejs'
  import { gsap } from "gsap"
  import { ScrollTrigger } from "gsap/ScrollTrigger"

  // Initialize on client
  if (typeof window !== 'undefined') {
    window.Alpine = Alpine
    Alpine.start()

    gsap.registerPlugin(ScrollTrigger)
    window.gsap = gsap

    // ... rest of animation code
  }
</script>
```

### Phase 6: Create Pages

#### 6.1 Create Index Page (`src/pages/index.astro`)
Convert `index.html` to use Splash layout and components:

```astro
---
import Splash from '../layouts/Splash.astro';
import HeroSection from '../components/HeroSection.astro';
import ContentSection from '../components/ContentSection.astro';
import SocialLinks from '../components/SocialLinks.astro';
import Footer from '../components/Footer.astro';
---

<Splash>
  <HeroSection slot="hero" />
  <ContentSection slot="content" />
  <SocialLinks slot="footer" />
  <Footer slot="footer" />
</Splash>
```

### Phase 7: Migration and Testing

#### 7.1 Asset Migration
- Verify all assets in `public/` are accessible
- Ensure paths remain correct (Astro serves `public/` at root)
- No changes needed for most assets

#### 7.2 Development Testing
```bash
npm run dev
```

**Test Cases:**
1. ✅ Page loads correctly
2. ✅ Fonts load properly
3. ✅ Lottie animation plays on first visit (desktop only)
4. ✅ Animation skipped on return visits (sessionStorage works)
5. ✅ GSAP animations trigger on scroll
6. ✅ Alpine.js smooth scroll works
7. ✅ Social links work
8. ✅ All images and SVGs display
9. ✅ PDF download works
10. ✅ Schema.org data validates
11. ✅ Fathom analytics loads
12. ✅ Mobile responsive design works

#### 7.3 Build Testing
```bash
npm run build
npm run preview
```

Verify:
- Build completes without errors
- Preview server works
- All assets are correctly bundled
- No console errors in browser

### Phase 8: Deployment Configuration

#### 8.1 Create Deployment Files
Create `_redirects` (for Netlify):
```
# Add any necessary redirects
```

#### 8.2 Update .gitignore
```
# Astro
dist/
.astro/

# dependencies
node_modules/

# logs
npm-debug.log*

# environment variables
.env
.env.production

# macOS
.DS_Store
```

#### 8.3 Deployment Testing
- Deploy to staging environment
- Test all functionality
- Verify analytics work
- Check performance metrics

## Future Enhancements

### Content Collections
Once basic migration is complete, consider adding:
- News/announcements collection
- Sponsor information collection
- Team member profiles

Example structure:
```
src/
├── content/
│   ├── config.ts (defines collections)
│   ├── news/
│   │   └── *.md
│   ├── sponsors/
│   │   └── *.md
│   └── team/
│       └── *.md
```

### Additional Pages
Using the Page layout, create:
- About page
- Code of Conduct page
- Venue information page
- Schedule page (once available)

### Component Library
Build reusable components:
- Button variants
- Card components
- Section wrappers
- Header/Navigation (when needed)

## Rollback Plan

If migration issues arise:

1. **Keep Vite setup**: Don't delete `vite.config.js` or Vite dependencies until Astro is fully working
2. **Git branch strategy**: Create `astro-migration` branch, keep `main` stable
3. **Parallel development**: Both systems can coexist temporarily
4. **Incremental cutover**: Test on staging before production deployment

## Timeline Estimate

- **Phase 1 (Setup)**: 2-3 hours
- **Phase 2 (Styles)**: 3-4 hours
- **Phase 3 (Layouts)**: 2-3 hours
- **Phase 4 (Components)**: 3-4 hours
- **Phase 5 (JavaScript)**: 2-3 hours
- **Phase 6 (Pages)**: 1 hour
- **Phase 7 (Testing)**: 2-3 hours
- **Phase 8 (Deployment)**: 1-2 hours

**Total**: ~16-23 hours

## Key Considerations

### Alpine.js in Astro
- Alpine.js works well with Astro
- Keep `x-data`, `x-init`, etc. directives in components
- Initialize Alpine in client-side script

### GSAP in Astro
- GSAP works great with Astro
- Ensure ScrollTrigger registration happens on client
- Watch for hydration timing issues with animations

### Tailwind vs SCSS
- **Keep Tailwind**: Faster migration, but may need Tailwind v3
- **Switch to SCSS**: More aligned with 2025 website, more work upfront

### CSS Custom Properties
- Current implementation uses CSS custom properties in `@theme`
- These can be preserved in SCSS or standard CSS

### Performance Considerations
- Astro provides better initial page load (static HTML)
- Client-side JavaScript hydration only where needed
- Consider code splitting for animations if page grows

## References

- [Astro Documentation](https://docs.astro.build)
- [Astro Migration Guide](https://docs.astro.build/en/guides/migrate-to-astro/)
- [PyCon AU 2025 Website Repository](https://github.com/pyconau/2025-website)
- Current project structure and dependencies

## Success Criteria

Migration is complete when:

1. ✅ Site builds without errors
2. ✅ All pages render correctly
3. ✅ All animations work as expected
4. ✅ All interactive features functional
5. ✅ Analytics tracking works
6. ✅ Schema.org markup validates
7. ✅ Performance equal or better than Vite version
8. ✅ Development experience improved (hot reload, etc.)
9. ✅ Documentation updated
10. ✅ Team members can work with Astro setup

---

**Document Version**: 1.1
**Last Updated**: 2025-10-12
**Author**: Development Plan for PyCon AU 2026 Astro Migration

## Changelog

### Version 1.1 (2025-10-12)
- Updated all package versions to latest stable releases as of October 2025:
  - Astro: 5.5.2 → 5.14.4
  - @astrojs/mdx: 4.2.0 → 4.3.6
  - Sass: 1.77.8 → 1.93.2
  - TypeScript: 5.5.4 → 5.9.3
  - Prettier: 3.3.3 → 3.6.2
  - prettier-plugin-astro: 0.11.1 → 0.14.1

### Version 1.0 (2025-10-12)
- Initial migration plan created
