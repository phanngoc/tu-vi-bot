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
      },
      backgroundImage: {
        tarot: "url('../../public/Images/bg-ewd-pattern.png')",
        'luminescent-one': "url('../../public/Images/lights-1.png.webp')",
        'luminescent-two': "url('../../public/Images/lights-2.png.webp')",
        'luminescent-light': 'radial-gradient(circle at 50% 50%, #FFFFFF 0%, rgba(255, 255, 255, 0.98) 4%, rgba(254, 254, 254, 0.95) 8%, rgba(254, 254, 254, 0.88) 12%, rgba(253, 253, 253, 0.8) 15%, rgba(252, 252, 252, 0.71) 19%, rgba(251, 251, 251, 0.61) 22%, rgba(250, 250, 250, 0.5) 25%, rgba(249, 249, 249, 0.39) 28%, rgba(248, 248, 248, 0.29) 31%, rgba(247, 247, 247, 0.2) 35%, rgba(246, 246, 246, 0.12) 38%, rgba(246, 246, 246, 0.05) 42%, rgba(245, 245, 245, 0.02) 46%, rgba(245, 245, 245, 0) 50%)',
      },
    },
    animation: {
      'infinity-bg': 'infinity-bg 60s linear infinite',
    },
    keyframes: {
      'infinity-bg': {
        '0%': { transform: 'translate3d(0, 0, 0)' },
        '100%': { transform: 'translate3d(-1692px, 0, 0)' },
      },
      'rotateIt': {
        '0%': { transform: 'rotate(0deg)' },
        '100%': { transform: 'rotate(360deg)' },
      },
      'rotateOp': {
        '0%': { opacity: '0.5' },
        '15%': { opacity: '0.4' },
        '25%': { opacity: '0.45' },
        '30%': { opacity: '0.6' },
        '60%': { opacity: '0.55' },
        '75%': { opacity: '0.35' },
        '90%': { opacity: '0.6' },
        '100%': { opacity: '0.5' },
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
      });
    }),
  ],
};
export default config;
