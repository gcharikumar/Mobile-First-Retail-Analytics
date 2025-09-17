// frontend/vite.config.js
/**
 * Vite Config: PWA setup with Workbox for offline.
 * Tailwind for mobile-first responsive.
 */
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { VitePWA } from 'vite-plugin-pwa'

export default defineConfig({
  plugins: [
    react(),
    VitePWA({
      registerType: 'autoUpdate',
      workbox: {
        globPatterns: ['**/*.{js,css,html,ico,png,svg}']
      },
      manifest: {
        name: 'Retail Insights PWA',
        short_name: 'RetailPWA',
        icons: [{ src: 'icon-192.png', sizes: '192x192', type: 'image/png' }],
        theme_color: '#000000',
        background_color: '#ffffff',
        display: 'standalone'
      }
    })
  ],
  css: {
    postcss: './postcss.config.js'  // Tailwind
  }
})