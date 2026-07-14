# PyCon AU 2026 Website

The official website for [PyCon AU 2026](https://2026.pycon.org.au) — Australia's national Python conference, held 26–30 August 2026 at Sofitel Brisbane Central.

## Prerequisites

- Node.js 22.11.0 (see `.tool-versions`)
- Python 3.11+ with [uv](https://docs.astral.sh/uv/) (for schedule sync and graphics scripts)

## Getting Started

1. **Install dependencies**
   ```bash
   npm install
   ```

2. **Start development server**
   ```bash
   npm run dev
   ```
   This will start the development server at `http://localhost:4321`

3. **Build for production**
   ```bash
   npm run build
   ```
   This creates a `dist/` folder with the production build

4. **Preview production build**
   ```bash
   npm run preview
   ```
   This serves the production build locally for testing

5. **Type check**
   ```bash
   npm run check
   ```
   Type-checks all `.astro` files via `astro check`

## Astro Content Collections Migration Note

Astro 7 no longer supports the legacy content config location at `src/content/config.ts`.

- Use `src/content.config.ts` for content collection definitions.
- Ensure each collection defines a `loader` (for example `glob(...)` from `astro/loaders`).

If `npm run dev` fails with a legacy content config error, verify that no `src/content/config.ts` file exists.

## Project Structure

```
├── src/
│   ├── components/         # Astro components
│   ├── content/            # Content collections (posts, sessions, people, sponsors, tracks)
│   ├── layouts/            # Base.astro and Page.astro
│   ├── pages/              # File-based routing
│   ├── styles/             # Global CSS (Tailwind)
│   └── constants.ts        # Site-wide constants (URLs, SEO defaults)
├── public/                 # Static assets
├── scripts/                # Schedule sync and graphics generation (Python/uv)
└── .github/workflows/      # CI: PR checks, production deploy, schedule sync
```

## Technologies Used

- [Astro](https://astro.build) (framework)
- [Tailwind CSS](https://tailwindcss.com) (styling)
- [Alpine.js](https://alpinejs.dev) (JavaScript)
- [GSAP](https://gsap.com) (animations)

## Media / Credits
* [Brisbane City at Sunset](/public/images/attend/beda-sunset.jpeg) Credit: @brizzy.pix, supplied by Brisbane Economic Development Agency
* [Brisbane Cyclists](/public/images/attend/beda-cyclists.jpeg) Credit: Tourism Australia, supplied by Brisbane Economic Development Agency
* [Brisbane Airport](/public/images/attend/beda-airport.jpeg) Credit: Jen Dainer, supplied by Brisbane Economic Development Agency
* Other photography by [Jack Skinner](https://jackskinner.com.au) used with permission.
