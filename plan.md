# PyCon AU 2026 Website Setup Plan

## Detailed Setup Plan for AstroJS + Tailwind CSS Hello World Project

Based on analysis of the PyCon AU 2025 website repository, here's a comprehensive setup plan:

PyCon AU 2025 website is at https://github.com/pyconau/2025-website

### **Phase 1: Project Initialization**
1. **Create AstroJS project with Tailwind CSS**
   ```bash
   npm create astro@latest -- --template minimal --add tailwind
   cd your-project-name
   ```

2. **Install dependencies using npm**
   ```bash
   npm install
   ```

### **Phase 2: Essential Configuration Files**
3. **Copy key configuration files from PyCon AU 2025:**
   - `.prettierrc.toml` - Code formatting rules
   - `.prettierignore` - Files to exclude from formatting
   - `.tool-versions` - Node.js version pinning
   - `tsconfig.json` - TypeScript configuration

4. **Create `astro.config.mjs`** similar to PyCon AU:
   ```js
   import { defineConfig } from "astro/config"
   import tailwind from "@astrojs/tailwind"
   
   export default defineConfig({
     integrations: [tailwind()]
   })
   ```

### **Phase 3: GitHub Actions & Scripts**
5. **Setup GitHub workflows** (`.github/workflows/`):
   - `build.yml` - Main build and deploy workflow with GitHub Pages
   - `pr_build.yml` - PR validation builds
   - Configure Node.js 22.11.0 (LTS) with npm (standard package manager)

6. **Add package.json scripts** (following PyCon AU pattern):
   ```json
   {
     "scripts": {
       "dev": "astro dev",
       "build": "astro build", 
       "preview": "astro preview",
       "start": "astro dev"
     }
   }
   ```

### **Phase 4: Project Structure**
7. **Create directory structure** (mirroring PyCon AU):
   ```
   src/
   ├── layouts/        # Base layouts
   ├── pages/          # File-based routing
   ├── components/     # Reusable components
   └── content/        # Content collections (if needed)
   ```

8. **Essential development files:**
   - `src/env.d.ts` - Astro type definitions
   - `.gitignore` - Standard Node.js/Astro exclusions
   - `_redirects` - Netlify-style redirects file

### **Phase 5: Hello World Implementation**
9. **Create Hello World page** (`src/pages/index.astro`):
   ```astro
   ---
   // Component logic here
   ---
   <html>
     <head>
       <title>PyCon AU 2026</title>
     </head>
     <body class="bg-gray-100 flex items-center justify-center min-h-screen">
       <h1 class="text-4xl font-bold text-blue-600">
         Soon...
       </h1>
     </body>
   </html>
   ```

### **Phase 6: Development Tools**
10. **Optional enhancements from PyCon AU:**
    - Add Prettier with Astro plugin for code formatting
    - Include SASS for advanced styling (if needed)
    - Setup TypeScript for type safety

### **Key Dependencies to Install:**
- `astro` (^5.13.5) - Latest version
- `@astrojs/tailwind` (latest)
- `prettier` (^3.6.2) + `prettier-plugin-astro` (latest)
- `typescript` (^5.9.2) - Latest stable version

### **Commands to Run:**
```bash
npm install    # Install dependencies
npm run dev    # Start development server
npm run build  # Build for production
```

### **Key Files from PyCon AU 2025 Analysis:**

#### GitHub Actions:
- **build.yml**: Updated to use Node.js 22.11.0 (LTS) with npm, includes Typst setup, deploys to GitHub Pages
- **pr_build.yml**: Simple PR validation build (updated versions)
- **update_schedule.yml**: Python script for syncing external data (Pretalx API)

#### Configuration:
- **package.json**: Uses npm, includes standard Astro scripts
- **astro.config.mjs**: MDX integration, legacy collections support
- **.tool-versions**: Should be updated to pin Node.js 22.11.0 (LTS)
- **tsconfig.json**: Standard TypeScript configuration

#### Scripts:
- **schedule_sync.py**: Python Poetry project for syncing conference data
- Uses requests, ruamel.yaml, python-dateutil, Markdown, bleach, Pillow

This plan leverages the proven setup from PyCon AU 2025 while adapting it for the 2026 project. The GitHub Actions will handle automated builds and deployments, and the project structure follows established patterns that scale well for conference websites.