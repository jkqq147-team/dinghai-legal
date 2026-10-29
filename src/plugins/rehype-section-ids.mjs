// Manual-only Markdown rules (src/content/chartset/).
//
// Headings of the chart set manual keep their section number as the id:
// "### 6.3 导入被拒绝时" → id="6.3", "## 0. 速览" → id="0". The App and the
// manual itself cite sections by number ("第 6.3 节"), so links such as
// /developers/chartset/self-check/#6.3 must stay stable when a title changes.
// Runs before Astro's own heading ids, which keep an id that is already set.
const SECTION = /^(\d+(?:\.\d+)*)\.?\s/;

function text(node) {
	if (node.type === 'text') return node.value;
	return (node.children ?? []).map(text).join('');
}

function visit(node, fn) {
	fn(node);
	for (const child of node.children ?? []) visit(child, fn);
}

export function rehypeSectionIds() {
	return (tree, file) => {
		const path = String(file.path ?? file.history?.[0] ?? '');
		if (!path.includes('/src/content/chartset/')) return;
		visit(tree, (node) => {
			if (node.type !== 'element') return;
			if (/^h[2-4]$/.test(node.tagName)) {
				const match = SECTION.exec(text(node));
				if (match) node.properties = { ...node.properties, id: match[1] };
			}
			if (node.tagName === 'td') visit(node, keepTokensWhole);
		});
	};
}

// In table cells, inline code such as `formatVersion` or
// `format is <值>, not dinghai-chartset` must not break inside a token on a
// phone: each run between spaces that contains an ASCII letter, digit or <> and
// at most 4 CJK characters (`formatVersion`, `<major>.<minor>,`, `<路径>:`)
// becomes a nowrap span. The code still wraps at its spaces; Chinese messages
// wrap between characters as usual.
const TOKEN = /\S+/g;
const isToken = (run) => /[A-Za-z0-9<>]/.test(run) && (run.match(/[\u3000-\u9fff\uff00-\uffef]/g) ?? []).length <= 4;

function keepTokensWhole(node) {
	if (node.type !== 'element' || node.tagName !== 'code') return;
	node.children = node.children.flatMap((child) => {
		if (child.type !== 'text') return [child];
		const parts = [];
		let last = 0;
		for (const match of child.value.matchAll(TOKEN)) {
			if (!isToken(match[0])) continue;
			if (match.index > last) parts.push({ type: 'text', value: child.value.slice(last, match.index) });
			parts.push({ type: 'element', tagName: 'span', properties: { className: ['nobr'] }, children: [{ type: 'text', value: match[0] }] });
			last = match.index + match[0].length;
		}
		if (last < child.value.length) parts.push({ type: 'text', value: child.value.slice(last) });
		return parts;
	});
}
