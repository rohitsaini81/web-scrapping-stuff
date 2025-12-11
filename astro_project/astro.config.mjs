// astro.config.mjs
import mdx from '@astrojs/mdx';
import sitemap from '@astrojs/sitemap';
import { defineConfig } from 'astro/config';

export default defineConfig({
  site: 'https://example.com',
  output: 'server',   // <-- REQUIRED FOR SSR PAGES
  integrations: [mdx(), sitemap()],
});
