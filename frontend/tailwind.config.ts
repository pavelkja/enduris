import type { Config } from 'tailwindcss';

export default {
  content: ['./app/**/*.{js,ts,jsx,tsx,mdx}', './components/**/*.{js,ts,jsx,tsx,mdx}'],
  theme: {
    extend: {
      colors: {
        readiness: {
          good: '#16a34a',
          moderate: '#f97316',
          fatigue: '#dc2626',
        },
      },
    },
  },
  plugins: [],
} satisfies Config;
