# dinghai.app

Starlight (Astro) site, published to GitHub Pages by `.github/workflows/pages.yml`.

## Build and gate

- Node and npm are pinned: `.nvmrc`, `package.json` `engines`/`packageManager`, `package-lock.json`. Install with `npm ci`.
- `npm run dev` previews while editing; `npm run build && npm run preview` serves the built `dist/`.
- **Gate:** `npm run check` — builds, then `scripts/check-site.mjs` fails if anything in `dist/` loads from a host other than dinghai.app. CI runs the same command before deploying.

## URLs do not change

- Chinese is the root locale, English lives under `/en/`. These must keep working at the same paths: `/`, `/privacy/`, `/support/`, `/en/`, `/en/privacy/`, `/en/support/`. The App links to `https://dinghai.app/privacy/`.
- The chart set manual is Chinese only, under `/developers/chartset/` (`src/content/chartset/`). Its section anchors are the section numbers (`#1.1`, `#6.3`), set by `src/plugins/rehype-section-ids.mjs`; the App and the manual cite them. The App's V3 import error links to `/developers/chartset/structure/`. Never rename a page slug or renumber a section.
- `public/CNAME` stays `dinghai.app`.

## Legal pages are word for word

- `src/content/docs/{,en/}{privacy,support}.md` are legal and public wording. A layout change must not change one visible character: diff the visible text of every page before and after (extract plain text from both, compare block by block) and expect zero differences.
- A wording change is a policy change: every sentence must match what the current App and servers actually do.

## No third-party resources

- No cookies, analytics, tracking, external fonts, CDNs, or embeds. Search is Starlight's local Pagefind. Outbound `<a>` links are fine; anything a page loads is not.

## The manual follows the App code

- Every sentence of the manual about what the App checks or does must be traceable to the current DingHai code (`apps/ios/DingHai/…`, e.g. `Core/ChartPackages/`, `Core/ChartSets/ChartSetManifest.swift`, `Features/MapLibrary/`). Error codes and the text users see are copied from the code. When code and manual disagree, the code wins; a sentence with no source is removed or made non-committal.
- The manual is for external producers: no private repository paths, scripts, or simulator steps.
- Downloads live in `public/developers/chartset/downloads/`. The sample ZIP must match what `generate-chartset-sample.py` writes: `manifest.json` byte for byte, every tile identical after gzip decoding.
