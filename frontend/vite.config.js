import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';
import { VitePWA } from 'vite-plugin-pwa';

export default defineConfig({
  plugins: [
    react(),
    VitePWA({
      registerType: 'autoUpdate',
      includeAssets: ['pws-192-192-removebg-preview.png', 'pws-512-512-removebg-preview.png'],
      manifest: {
        name: 'WeatherWave',
        short_name: 'WeatherWave',
        start_url: '/',
        display: 'standalone',
        theme_color: '#1e90ff',
        background_color: '#1e1e1e',
        icons: [
          {
            src: 'pws-192-192-removebg-preview.png',
            sizes: '192x192',
            type: 'image/png',
          },
          {
            src: 'pws-512-512-removebg-preview.png',
            sizes: '512x512',
            type: 'image/png',
          }
        ]
      },
      workbox: {
        globPatterns: ['**/*.{js,css,html,png,svg}']
        // Removed navigateFallback/offline.html after it proved unreliable
      }
    })
  ],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
});




// // vite.config.js
// import { defineConfig } from 'vite'
// import react from '@vitejs/plugin-react'
// import path from 'path'

// export default defineConfig({
//   plugins: [react()],
//   resolve: {
//     alias: {
//       '@': path.resolve(__dirname, './src'),
//     },
//   },
// })
