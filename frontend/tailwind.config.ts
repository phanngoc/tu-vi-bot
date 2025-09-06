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
    animation: {
      'infinity-bg': 'infinity-bg 60s linear infinite',
      'mystical-glow': 'mystical-glow 3s ease-in-out infinite',
      'wisdom-pulse': 'wisdom-pulse 4s ease-in-out infinite',
      'constellation': 'constellation 8s linear infinite',
      'divination-shimmer': 'divination-shimmer 2s ease-in-out infinite',
      'ancient-breathe': 'ancient-breathe 6s ease-in-out infinite',
      'float-gentle': 'float-gentle 3s ease-in-out infinite',
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
      'mystical-glow': {
        '0%, 100%': { 
          boxShadow: '0 0 20px rgba(212, 175, 55, 0.4), 0 0 40px rgba(212, 175, 55, 0.2)', 
          transform: 'scale(1)' 
        },
        '50%': { 
          boxShadow: '0 0 30px rgba(212, 175, 55, 0.6), 0 0 60px rgba(212, 175, 55, 0.3)', 
          transform: 'scale(1.02)' 
        },
      },
      'wisdom-pulse': {
        '0%, 100%': { opacity: '0.8' },
        '50%': { opacity: '1' },
      },
      'constellation': {
        '0%': { transform: 'rotate(0deg) translateY(0px)' },
        '33%': { transform: 'rotate(120deg) translateY(-5px)' },
        '66%': { transform: 'rotate(240deg) translateY(5px)' },
        '100%': { transform: 'rotate(360deg) translateY(0px)' },
      },
      'divination-shimmer': {
        '0%, 100%': { 
          backgroundPosition: '200% center',
          opacity: '0.7'
        },
        '50%': { 
          backgroundPosition: '-200% center',
          opacity: '1'
        },
      },
      'ancient-breathe': {
        '0%, 100%': { transform: 'scale(1) rotate(0deg)' },
        '50%': { transform: 'scale(1.05) rotate(2deg)' },
      },
      'float-gentle': {
        '0%, 100%': { transform: 'translateY(0px) rotate(0deg)' },
        '50%': { transform: 'translateY(-10px) rotate(1deg)' },
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
