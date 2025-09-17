/* frontend/tailwind.config.js */

/**
 * Tailwind CSS config: Mobile-first responsive design.
 * Customizes fonts, colors for retail app.
 */
module.exports = {
  content: ['./src/**/*.{js,jsx,ts,tsx}'],
  theme: {
    extend: {
      screens: {
        'sm': '320px',  // Mobile-first
        'md': '768px',
      },
    },
  },
  plugins: [],
};