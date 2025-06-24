// frontend/vite.config.js
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { VitePWA } from 'vite-plugin-pwa'

export default defineConfig({
  plugins: [
    react(),
    VitePWA({
      registerType: 'autoUpdate',
      // These are your PWA assets; ensure they are in frontend/public
      includeAssets: ['favicon.svg', 'favicon.ico', 'robots.txt', 'apple-touch-icon.png'],

      // CRITICAL: This line ensures manifest.webmanifest is generated and named correctly
      fileName: 'manifest.webmanifest',

      manifest: {
        name: 'WeatherWave',
        short_name: 'WeatherWave',
        description: 'Nepal weather app with forecasts and AQI',
        theme_color: '#000000',
        background_color: '#000000',
        display: 'standalone',
        start_url: '/',
        icons: [
          {
            src: '/pwa-192x192.png',
            sizes: '192x192',
            type: 'image/png',
          },
          {
            src: '/pwa-512x512.png',
            sizes: '512x512',
            type: 'image/png',
          },
        ],
      },
      workbox: {
        // globPatterns: specify what static files your service worker should cache initially.
        // We're reverting to a basic set here for the core app shell.
        globPatterns: ['**/*.{js,css,html,ico,png,svg}'],
      },
    })
  ]
})