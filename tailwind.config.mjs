/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  theme: {
    extend: {
      colors: {
        'brand-primary': '#BDF462',
        'brand-secondary': '#B380FF',
        'brand-dark': '#020202',
        'brand-gray': '#282828',
        'brand-light': '#ECECEC',
        'brand-neutral': '#EDEDED',
        'brand-accent': '#C5F57A',
        'pycon-light-gray': '#ECECEC',
        'pycon-black': '#020202',
        'pycon-green': '#BDF462',
        'pycon-purple': '#B380FF',
        'pycon-dark-gray': '#282828',
        'pycon-off-white': '#EDEDED',
        'pycon-accent': '#C5F57A',
      },
      fontFamily: {
        jakarta: ['Plus Jakarta Sans', 'sans-serif'],
        inter: ['Inter', 'sans-serif'],
        manrope: ['Manrope', 'sans-serif'],
        'roboto-slab': ['Roboto Slab', 'serif'],
      },
      fontSize: {
        xs: ['0.875rem', { lineHeight: '1.25rem' }],
        sm: ['1rem', { lineHeight: '1.5rem' }],
        base: ['1.125rem', { lineHeight: '1.56rem' }],
        lg: ['1.25rem', { lineHeight: '1.75rem' }],
        xl: ['1.5rem', { lineHeight: '2rem' }],
        '2xl': ['2rem', { lineHeight: '2.5rem' }],
        '3xl': ['2.5rem', { lineHeight: '2.8rem' }],
        '4xl': ['3rem', { lineHeight: '3.5rem' }],
        '5xl': ['4.375rem', { lineHeight: '4.875rem' }],
        '6xl': ['5.188rem', { lineHeight: '5.688rem' }],
        '7xl': ['6.125rem', { lineHeight: '8.06rem' }],
      },
    },
  },
  plugins: [],
}
