import { defineConfig } from 'vite'
import tailwindcss from '@tailwindcss/vite'
import path from 'path'
import { readdirSync } from 'fs'

export default defineConfig({
  base: './',
  plugins: [
    tailwindcss(),
  ],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src'),
    },
  },
  build: {
    rollupOptions: {
      input: Object.fromEntries(
        readdirSync(__dirname)
          .filter(file => file.endsWith('.html'))
          .map(file => [
            file.replace(/\.html$/, ''),
            path.resolve(__dirname, file)
          ])
      ),
    },
  },
})