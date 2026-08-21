import { defineConfig } from 'vite'

export default defineConfig({
  build: {
    lib: {
      entry: 'src/index.js',
      name: 'DoWHEditor',
      fileName: () => 'editor.bundle.js',
      formats: ['iife'],
      cssFileName: 'editor',
    },
    outDir: 'dist',
    emptyOutDir: true,
    sourcemap: false,
    cssCodeSplit: false,
    rollupOptions: {
      output: {
        assetFileNames: 'editor.[ext]',
      },
    },
  },
})
