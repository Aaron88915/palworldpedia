// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import mdx from '@astrojs/mdx';

// 根据部署环境自动切换 base path
// - GitHub Pages (子路径 /palworldpedia): USE_PROJECT_PATH=true
// - 自定义域名 (根路径 /): USE_PROJECT_PATH=false 或不设
const useProjectPath = process.env.USE_PROJECT_PATH === 'true';
const siteUrl = useProjectPath
  ? 'https://aaron88915.github.io'
  : 'https://palworldpedia.cc';
const basePath = useProjectPath ? '/palworldpedia' : '/';

// https://astro.build/config
export default defineConfig({
  site: siteUrl,
  base: basePath,
  output: 'static',
  trailingSlash: 'ignore',

  // i18n 配置
  i18n: {
    defaultLocale: 'zh',
    locales: ['zh', 'en'],
    routing: {
      prefixDefaultLocale: false,
    },
  },

  integrations: [
    sitemap({
      i18n: {
        defaultLocale: 'zh',
        locales: {
          zh: 'zh-CN',
          en: 'en-US',
        },
      },
    }),
    mdx(),
  ],

  build: {
    inlineStylesheets: 'auto',
  },
});
