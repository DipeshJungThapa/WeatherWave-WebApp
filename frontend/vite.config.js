import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';
import { VitePWA } from 'vite-plugin-pwa';

export default defineConfig({
  plugins: [
    react(),
    VitePWA({
      registerType: 'autoUpdate',
      includeAssets: ['pws-192-192.png', 'pws-512-512.png'],
      manifest: {
        name: 'WeatherWave App',
        short_name: 'WeatherWave',
        description: 'Your Weather Companion – WeatherWave PWA',
        start_url: '/',
        display: 'standalone',
        background_color: '#1e1e1e',
        theme_color: '#1e90ff',
        orientation: 'portrait',
        icons: [
          {
            src: 'pws-192-192.png',
            sizes: '192x192',
            type: 'image/png',
          },
          {
            src: 'pws-512-512.png',
            sizes: '512x512',
            type: 'image/png',
          }
        ]
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
