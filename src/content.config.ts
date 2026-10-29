import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';
import { docsLoader, i18nLoader } from '@astrojs/starlight/loaders';
import { docsSchema, i18nSchema } from '@astrojs/starlight/schema';

export const collections = {
	// App pages, Chinese at the root and English under /en/.
	docs: defineCollection({ loader: docsLoader(), schema: docsSchema() }),
	i18n: defineCollection({ loader: i18nLoader(), schema: i18nSchema() }),
	// The chart set manual, Chinese only. It is its own collection so that
	// Starlight does not generate English fallback pages for it; the pages are
	// rendered by src/pages/developers/chartset/[...slug].astro.
	chartset: defineCollection({
		loader: glob({ pattern: '**/*.md', base: './src/content/chartset' }),
		schema: z.object({
			title: z.string(),
			description: z.string().optional(),
		}),
	}),
};
