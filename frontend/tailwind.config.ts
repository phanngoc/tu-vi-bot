import plugin from 'tailwindcss/plugin';

import type { Config } from 'tailwindcss';

const config: Config = {
  content: ['./src/components/**/*.{js,ts,jsx,tsx,mdx}', './src/app/**/*.{js,ts,jsx,tsx,mdx}'],
  theme: {
    extend: {
      colors: {
        primary: {
          100: '#FA5B30',
          200: '#0f2731',
        },
        'tarot-color': 'rgb(27, 15, 44)',
        mystic: {
          dark: '#1a0b2e',
          purple: '#2d1b4e',
          gold: '#d4af37',
          amber: '#f39c12',
          sage: '#9caf88',
          silver: '#c0c0c0',
          cosmic: '#4a4472',
          deep: '#16213e',
          mist: 'rgba(212, 175, 55, 0.1)',
          glow: 'rgba(243, 156, 18, 0.3)',
        },
        fortune: {
          wisdom: '#8b4513',
          mystery: '#483d8b',
          divination: '#9370db',
          celestial: '#4169e1',
          spiritual: '#6a5acd',
          ancient: '#2f4f4f',
        }
      },
      backgroundImage: {
        tarot: "url('../../public/Images/bg-ewd-pattern.png')",
        'luminescent-one': "url('../../public/Images/lights-1.png.webp')",
        'luminescent-two': "url('../../public/Images/lights-2.png.webp')",
        'luminescent-light': 'radial-gradient(circle at 50% 50%, #FFFFFF 0%, rgba(255, 255, 255, 0.98) 4%, rgba(254, 254, 254, 0.95) 8%, rgba(254, 254, 254, 0.88) 12%, rgba(253, 253, 253, 0.8) 15%, rgba(252, 252, 252, 0.71) 19%, rgba(251, 251, 251, 0.61) 22%, rgba(250, 250, 250, 0.5) 25%, rgba(249, 249, 249, 0.39) 28%, rgba(248, 248, 248, 0.29) 31%, rgba(247, 247, 247, 0.2) 35%, rgba(246, 246, 246, 0.12) 38%, rgba(246, 246, 246, 0.05) 42%, rgba(245, 245, 245, 0.02) 46%, rgba(245, 245, 245, 0) 50%)',
      },
    },
  },
  plugins: [
    plugin(function ({ addUtilities }) {
      addUtilities({
        '.app-h-screen': {
          height: '100vh',

          ['@supports (height: 100dvh)']: {
            height: '100dvh',
          },
        },
        '.app-min-h-screen': {
          minHeight: '100vh',

          ['@supports (height: 100dvh)']: {
            minHeight: '100dvh',
          },
        },
        '.scrollbar-thin': {
          'scrollbar-width': 'thin',
        },
        '.scrollbar-thumb-mystic-gold\\/30': {
          'scrollbar-color': 'rgba(212, 175, 55, 0.3) transparent',
        },
        '.scrollbar-track-transparent': {
          'scrollbar-color': 'rgba(212, 175, 55, 0.3) transparent',
        },
      });
    }),
  ],
};
export default config;
