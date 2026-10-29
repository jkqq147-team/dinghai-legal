// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import { rehypeSectionIds } from './src/plugins/rehype-section-ids.mjs';

// Every page is self-contained: no external fonts, CDNs, or analytics.
// `scripts/check-site.mjs` fails the build output if anything points off-site.
export default defineConfig({
	site: 'https://dinghai.app',
	trailingSlash: 'always',
	markdown: {
		// Legal pages are copied word for word: no typographic quote rewriting.
		smartypants: false,
		// Manual headings keep their section numbers as ids (`#6.3`).
		rehypePlugins: [rehypeSectionIds],
	},
	integrations: [
		starlight({
			title: { 'zh-Hans': '定海', en: 'DingHai' },
			description: '定海 App 的隐私政策、用户支持与海图集接入手册。',
			logo: { src: './src/assets/app-icon.png', alt: '' },
			favicon: '/favicon.png',
			head: [{ tag: 'link', attrs: { rel: 'apple-touch-icon', href: '/apple-touch-icon.png' } }],
			defaultLocale: 'root',
			locales: {
				root: { label: '简体中文', lang: 'zh-Hans' },
				en: { label: 'English', lang: 'en' },
			},
			customCss: ['./src/styles/custom.css'],
			routeMiddleware: './src/route-data.ts',
			components: { LanguageSelect: './src/components/LanguageSelect.astro' },
			lastUpdated: false,
			pagination: false,
			sidebar: [
				{
					label: 'App',
					items: [
						{ label: '隐私政策', translations: { en: 'Privacy Policy' }, link: '/privacy/' },
						{ label: '用户支持', translations: { en: 'Support' }, link: '/support/' },
					],
				},
				{
					label: '海图制作方',
					items: [
						{ label: '接入手册', link: '/developers/chartset/' },
						{ label: '1. 目录结构', link: '/developers/chartset/structure/' },
						{ label: '2. manifest.json', link: '/developers/chartset/manifest/' },
						{ label: '3. chart.mbtiles 文件', link: '/developers/chartset/mbtiles/' },
						{ label: '4. 瓦片内容', link: '/developers/chartset/tiles/' },
						{ label: '5. 数据清单', link: '/developers/chartset/data/' },
						{ label: '6. 自检', link: '/developers/chartset/self-check/' },
						{
							label: '附录（不属于海图集格式）',
							items: [{ label: '附录 7. 无 manifest 的矢量 MBTiles', link: '/developers/chartset/vector-mbtiles/' }],
						},
					],
				},
			],
		}),
	],
});
