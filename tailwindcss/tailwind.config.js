/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["../api/templates/**/*.html"],
  theme: {
    extend: {},
  },
  plugins: [
    require('@tailwindcss/forms'),
  ],
};