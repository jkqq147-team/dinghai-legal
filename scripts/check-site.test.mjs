import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { mkdir, mkdtemp, rm, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import test from 'node:test';
import { fileURLToPath } from 'node:url';

const checker = fileURLToPath(new URL('./check-site.mjs', import.meta.url));

// The site build need not emit these quote forms; exercise the CLI against built HTML directly.
test('the site gate rejects loads however the HTML attribute is quoted, not navigation or text', async (t) => {
	const dir = await mkdtemp(join(tmpdir(), 'dinghai-check-site-'));
	t.after(() => rm(dir, { recursive: true, force: true }));
	const dist = join(dir, 'dist');
	await mkdir(dist);

	const url = 'https://example.com/image.png';
	const cases = [
		['double-quoted image', `<img src="${url}">`, 1],
		['single-quoted image', `<img src='${url}'>`, 1],
		['unquoted image', `<img src=${url}>`, 1],
		['single-quoted inline style', `<span style='background-image: url("${url}")'></span>`, 1],
		['single-quoted refresh', `<meta content='0;url=${url}' http-equiv='refresh'>`, 1],
		['address in alt text', `<img src="/local.png" alt="Example: src='${url}'">`, 0],
		['outbound navigation', `<a href='${url}'>Example</a>`, 0],
	];
	const statuses = {};
	for (const [name, html] of cases) {
		await writeFile(join(dist, 'index.html'), html);
		const run = spawnSync(process.execPath, [checker], { cwd: dir, encoding: 'utf8' });
		assert.ifError(run.error);
		statuses[name] = run.status;
	}
	assert.deepEqual(statuses, Object.fromEntries(cases.map(([name, , status]) => [name, status])));
});
