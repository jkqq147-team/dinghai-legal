// Gate on the built site (dist/): nothing a page loads may come from anywhere
// but dinghai.app. Checks every place a browser fetches from:
//   HTML  src/href/srcset/poster/data/action on any tag except <a>, and
//         <meta http-equiv="refresh">
//   CSS   url(…) and @import, in .css files and inline <style>/style=""
//   JS    import/import(), fetch(), new Worker(), importScripts(),
//         sendBeacon(), XMLHttpRequest.open(), WebSocket/EventSource
// Outbound <a href> links are navigation the reader chooses; they are listed
// for review, not failed. Other absolute URLs inside scripts (translator
// credits, `new URL(x, "https://example.com")` parsing bases) are not
// requests; the browser network capture covers what actually loads.
//
//   npm run check     (builds, then runs this)
import { readdir, readFile } from 'node:fs/promises';
import { join, relative } from 'node:path';

const ROOT = 'dist';
const OWN = new Set(['dinghai.app']);

async function* files(dir) {
	for (const entry of await readdir(dir, { withFileTypes: true })) {
		const path = join(dir, entry.name);
		if (entry.isDirectory()) yield* files(path);
		else yield path;
	}
}

/** True when `url` names a host other than dinghai.app. Relative URLs are local. */
function offSite(url) {
	const value = url.trim();
	if (!/^([a-z][a-z0-9+.-]*:)?\/\//i.test(value)) return false;
	try {
		return !OWN.has(new URL(value.startsWith('//') ? `https:${value}` : value).hostname);
	} catch {
		return true;
	}
}

const CSS_URL = /url\(\s*(['"]?)([^'")]+)\1\s*\)|@import\s+(['"])([^'"]+)\3/g;
const JS_LOAD = [
	/\bimport\s*\(\s*(['"`])([^'"`]+)\1/g,
	/\b(?:import|export)\b[^'"`;]*?\bfrom\s*(['"`])([^'"`]+)\1/g,
	/\bimport\s*(['"`])([^'"`]+)\1/g,
	/\bfetch\s*\(\s*(['"`])([^'"`]+)\1/g,
	/\bnew\s+(?:Shared)?Worker\s*\(\s*(['"`])([^'"`]+)\1/g,
	/\bimportScripts\s*\(\s*(['"`])([^'"`]+)\1/g,
	/\bsendBeacon\s*\(\s*(['"`])([^'"`]+)\1/g,
	/\.open\s*\(\s*(['"`])[A-Z]+\1\s*,\s*(['"`])([^'"`]+)\2/g,
	/\bnew\s+(?:WebSocket|EventSource)\s*\(\s*(['"`])([^'"`]+)\1/g,
];

const failures = [];
const links = new Map();
let checked = 0;

function css(file, text) {
	for (const match of text.matchAll(CSS_URL)) {
		const url = match[2] ?? match[4];
		if (offSite(url)) failures.push(`${file}: CSS ${url}`);
	}
}

function js(file, text) {
	for (const pattern of JS_LOAD) {
		for (const match of text.matchAll(pattern)) {
			const url = match[match.length - 1];
			if (offSite(url)) failures.push(`${file}: JS ${match[0].slice(0, 80)}`);
		}
	}
}

for await (const path of files(ROOT)) {
	const file = relative(ROOT, path);
	if (file.endsWith('.html')) {
		checked++;
		const text = await readFile(path, 'utf8');
		for (const [tag] of text.matchAll(/<[a-z][a-z0-9-]*\b[^>]*>/gi)) {
			const name = tag.slice(1).split(/[\s>/]/)[0].toLowerCase();
			for (const [, attr, value] of tag.matchAll(/\s(src|href|srcset|poster|data|action|formaction|content)="([^"]*)"/gi)) {
				const key = attr.toLowerCase();
				if (name === 'a' && key === 'href') {
					if (offSite(value)) links.set(value, (links.get(value) ?? new Set()).add(file));
					continue;
				}
				// <meta content> is text (titles, descriptions, canonical/OG URLs of
				// this site); only a refresh redirect makes the browser load it.
				if (key === 'content' && !/http-equiv="refresh"/i.test(tag)) continue;
				const urls = key === 'srcset' ? value.split(',').map((part) => part.trim().split(/\s+/)[0]) : [value.replace(/^\d+;\s*url=/i, '')];
				for (const url of urls) if (offSite(url)) failures.push(`${file}: <${name} ${key}="${url}">`);
			}
			const style = /\sstyle="([^"]*)"/i.exec(tag);
			if (style) css(file, style[1]);
		}
		for (const [, body] of text.matchAll(/<style\b[^>]*>([\s\S]*?)<\/style>/gi)) css(file, body);
		for (const [, body] of text.matchAll(/<script\b[^>]*>([\s\S]*?)<\/script>/gi)) js(file, body);
	} else if (file.endsWith('.css')) {
		checked++;
		css(file, await readFile(path, 'utf8'));
	} else if (/\.m?js$/.test(file)) {
		checked++;
		js(file, await readFile(path, 'utf8'));
	}
}

console.log(`Checked ${checked} HTML, CSS and JS files in ${ROOT}/.`);
console.log('Outbound links (navigation only, not loaded by the page):');
for (const [url, pages] of [...links].sort()) console.log(`  ${url}  (${pages.size} page${pages.size > 1 ? 's' : ''})`);
if (failures.length) {
	console.error(`\n${failures.length} load(s) from other hosts:`);
	for (const failure of failures) console.error(`  ${failure}`);
	process.exit(1);
}
console.log('\nNothing in dist/ loads from outside dinghai.app.');
