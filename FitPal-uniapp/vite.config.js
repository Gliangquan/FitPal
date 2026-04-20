import { defineConfig } from 'vite'
import uni from '@dcloudio/vite-plugin-uni'

export default defineConfig({
  plugins: [uni()],
  server: {
    host: '0.0.0.0',
    port: 9042,
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:9903',
        changeOrigin: true,
      },
    },
  },
})
