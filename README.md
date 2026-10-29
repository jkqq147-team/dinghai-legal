# DingHai site

Source of <https://dinghai.app/>: the DingHai app's privacy policy and support pages, and the chart set integration manual for chart producers.

- Privacy policy: <https://dinghai.app/privacy/> (English: <https://dinghai.app/en/privacy/>)
- Support: <https://dinghai.app/support/> (English: <https://dinghai.app/en/support/>)
- Chart set integration manual (Chinese): <https://dinghai.app/developers/chartset/>

Built with [Starlight](https://starlight.astro.build/) and deployed to GitHub Pages by GitHub Actions on every push to `main`. The site intentionally sets no cookies and loads no analytics, tracking, or third-party resources; search runs locally with Pagefind.

```sh
npm ci          # Node and npm versions: .nvmrc, package.json
npm run dev     # live preview
npm run check   # build + check that nothing loads from outside dinghai.app
```

Rules for changing the site are in [AGENTS.md](AGENTS.md).
