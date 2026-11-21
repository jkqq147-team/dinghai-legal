# dinghai.app

Starlight (Astro) site, published to GitHub Pages by `.github/workflows/pages.yml`.

## Build and gate

- CI selects Node from `.nvmrc`. `package.json` declares the Node and npm versions (`engines.node` and `packageManager`), and `package-lock.json` locks dependencies. Install with `npm ci`.
- `npm run dev` previews while editing; `npm run build && npm run preview` serves the built `dist/`.
- **Gate:** `npm run check` builds the site and statically checks `dist/` for recognizable load URLs outside dinghai.app. Passing is not browser network verification. CI runs the same command before deploying.

## URLs do not change

- Chinese is the root locale, English lives under `/en/`. These must keep working at the same paths: `/`, `/privacy/`, `/support/`, `/en/`, `/en/privacy/`, `/en/support/`. The App links to `https://dinghai.app/privacy/`.
- The chart set manual is Chinese only and lives under `/developers/chartset/`. Keep published page paths and numbered section anchors (for example `#1.1` and `#6.3`) unchanged.
- `public/CNAME` stays `dinghai.app`.

## Public wording and evidence

- `src/content/docs/{,en/}{privacy,support}.md` are legal and public wording. A layout change must not change one visible character: diff the visible text of every page before and after (extract plain text from both, compare block by block) and expect zero differences.
- **用户定：** 隐私政策与支持页按类别层级写：处理哪类数据、用来做什么、存放在哪里、谁能看到、用户能控制什么及其大致效果；不写机制层级的细节（记录字段、计时与阈值、Cloudflare 之外的内部存储产品、哪台设备写什么、删除过程、与隐私无关的产品行为）。海图集接入手册是技术契约，不适用本条。
- **用户定：** 对外法务／合规文案的措辞变更是政策变更；逐句用当前已上线版本的真机行为核实，涉及服务端的陈述同时核对当前部署的实际行为。代码、模拟器和编译通过不能代替真机证据。海图集接入手册对 App 校验与行为的陈述须能追溯到当前 App 实现，格式与校验以代码为准，报错码与用户可见文字照抄代码；涉及真机界面、链接或操作步骤的陈述须在该上线版本的真机上核实。无法证实的断言不发布。

## No third-party resources

- No cookies, analytics, tracking, external fonts, CDNs, or embeds. Search is Starlight's local Pagefind. Outbound `<a>` links are fine; anything a page loads is not.

## Manual audience and downloads

- The manual is for external producers: no private repository paths, scripts, or simulator steps.
- Downloads live in `public/developers/chartset/downloads/`. The sample ZIP must match what `generate-chartset-sample.py` writes: `manifest.json` byte for byte, every tile identical after gzip decoding.
