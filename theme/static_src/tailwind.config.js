/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    '../templates/**/*.html',
    '../../templates/**/*.html',
    '../../**/templates/**/*.html',
    '../../**/*.js',
    '!../../**/node_modules'
  ],
  theme: {
    extend: {
      colors: {
        'primary-custom': '#7B61FF', 
        secondary: '#5AB2E6',
        third: '#875AE6',
        'principal-font': '#5B5B5B',
        'secondary-font': '#000000',
        'principal-bg': '#F6F6F6',
        'secondary-bg': '#FFFFFF'
      }
    }
  },
  plugins: [
    require('daisyui'),
  ],
  daisyui: {
    themes: ["light"],
  }
}