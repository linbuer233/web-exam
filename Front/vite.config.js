import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  // server: {
  //   proxy: {
  //     '/api': { // 匹配 '/api' 的请求
  //       target: 'http://localhost:8000', // FastAPI 服务的地址
  //       changeOrigin: true, // 为 true 时，服务器收到的请求头中的 Host 为 target 值
  //       rewrite: '^/api', // 重写请求路径，注意这里不需要路径重写对象
  //     },
  //   },
  // },
  plugins: [
    vue(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  }
})
