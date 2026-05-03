/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      fontFamily: {
        display: ['"Fraunces"', 'Georgia', 'serif'],
        sans: ['"IBM Plex Sans"', 'system-ui', 'sans-serif'],
        mono: ['"JetBrains Mono"', 'ui-monospace', 'monospace'],
      },
      colors: {
        ink: {
          950: '#0a0f1a',
          900: '#0f1624',
          850: '#141c2e',
          800: '#1a2438',
          700: '#2a3550',
          600: '#3d4a68',
          500: '#5a6783',
        },
        bone: {
          50: '#fafaf7',
          100: '#f5f3ec',
          200: '#e8e4d6',
          300: '#d4cfbd',
          400: '#a8a391',
          500: '#78745f',
        },
        emerald: {
          accent: '#4ade80',
          deep: '#10b981',
          dark: '#047857',
        },
        amber: {
          accent: '#fbbf24',
          deep: '#f59e0b',
        },
        crimson: {
          accent: '#f87171',
          deep: '#ef4444',
        },
      },
      backgroundImage: {
        'grid-pattern': "linear-gradient(rgba(255,255,255,0.03) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.03) 1px, transparent 1px)",
        'radial-glow': 'radial-gradient(circle at 30% 0%, rgba(74,222,128,0.08), transparent 50%)',
      },
      backgroundSize: {
        'grid': '32px 32px',
      },
      boxShadow: {
        'glow-emerald': '0 0 40px -10px rgba(74,222,128,0.4)',
        'glow-amber': '0 0 40px -10px rgba(251,191,36,0.3)',
        'card': '0 1px 0 rgba(255,255,255,0.04) inset, 0 0 0 1px rgba(255,255,255,0.06)',
      },
      animation: {
        'fade-up': 'fadeUp 0.5s ease-out',
        'pulse-soft': 'pulseSoft 2s ease-in-out infinite',
        'shimmer': 'shimmer 2s linear infinite',
      },
      keyframes: {
        fadeUp: {
          '0%': { opacity: '0', transform: 'translateY(8px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        pulseSoft: {
          '0%, 100%': { opacity: '0.6' },
          '50%': { opacity: '1' },
        },
        shimmer: {
          '0%': { backgroundPosition: '-200% 0' },
          '100%': { backgroundPosition: '200% 0' },
        },
      },
    },
  },
  plugins: [],
}