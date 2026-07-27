// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import mdx from '@astrojs/mdx';

// https://astro.build/config
export default defineConfig({
  site: 'https://palworldpedia.cc',
  output: 'static',
  trailingSlash: 'ignore',

  // i18n 配置 - MVP 阶段只做中文，英文翻译就绪后加回 en
  i18n: {
    defaultLocale: 'zh',
    locales: ['zh'],
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
        },
      },
    }),
    mdx(),
  ],

  build: {
    inlineStylesheets: 'auto',
  },
});
