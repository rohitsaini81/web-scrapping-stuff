import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const blog = defineCollection({
  loader: glob({ base: './src/content/blog', pattern: '**/*.{md,mdx}' }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    pubDate: z.coerce.date(),
    updatedDate: z.coerce.date().optional(),
    heroImage: z.any().optional(),
  }),
});

// ADD THIS ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓
const apps = defineCollection({
  loader: glob({ base: './src/content/apps', pattern: '**/*.{md,mdx}' }),
  schema: z.object({
    title: z.string(),
    // add fields you expect (or none)
  }),
});

export const collections = {
  blog,
  apps, // <-- REGISTER IT HERE
};
