/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        ea: {
          bg: '#0b0f19',
          card: '#131b2e',
          cardHover: '#1a233a',
          border: '#1e293b',
          borderLight: '#334155',
          primary: '#38bdf8',
          emerald: '#10b981',
          amber: '#f59e0b',
          rose: '#f43f5e',
          textHeader: '#ffffff',
          textMuted: '#94a3b8',
          textBody: '#e2e8f0',
        },
      },
    },
  },
  plugins: [],
};
