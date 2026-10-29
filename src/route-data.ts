import { defineRouteMiddleware } from '@astrojs/starlight/route-data';

// The chart set manual exists only in Chinese (src/content/chartset/).
const MANUAL = '/developers/chartset/';

export const onRequest = defineRouteMiddleware((context) => {
	const route = context.locals.starlightRoute;
	// English pages: the sidebar shows only the App group.
	if (route.locale === 'en') {
		route.sidebar = route.sidebar.filter(
			(entry) => !(entry.type === 'group' && entry.label === '海图制作方'),
		);
	}
	// Manual pages: no English alternate to announce.
	if (context.url.pathname.startsWith(MANUAL)) {
		route.head = route.head.filter(
			(tag) => !(tag.tag === 'link' && tag.attrs?.rel === 'alternate'),
		);
	}
});
