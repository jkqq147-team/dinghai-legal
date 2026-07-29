# Agent Skills

Reusable agent skills vendored into this repository as preparation for the
upcoming Kimi-based frontend rework. No site UI changes are part of this
setup.

## Provenance

| Skill | Source repository | License |
| --- | --- | --- |
| `animation-vocabulary` | <https://github.com/emilkowalski/skills> | See upstream `LICENSE` |
| `apple-design` | <https://github.com/emilkowalski/skills> | See upstream `LICENSE` |
| `emil-design-eng` | <https://github.com/emilkowalski/skills> | See upstream `LICENSE` |
| `find-animation-opportunities` | <https://github.com/emilkowalski/skills> | See upstream `LICENSE` |
| `improve-animations` | <https://github.com/emilkowalski/skills> | See upstream `LICENSE` |
| `pick-ui-library` | <https://github.com/emilkowalski/skills> | See upstream `LICENSE` |
| `prototype` | <https://github.com/emilkowalski/skills> | See upstream `LICENSE` |
| `review-animations` | <https://github.com/emilkowalski/skills> | See upstream `LICENSE` |
| `kill-ai-slop` | <https://github.com/yetone/kill-ai-slop> | Apache-2.0 (upstream) |

Contents are verbatim copies of the upstream `skills/*` (emilkowalski) and
`skill/` (kill-ai-slop) directories. Re-copy from upstream to refresh.

## Usage

Each skill directory contains a `SKILL.md` with frontmatter (`name`,
`description`). Agent runtimes load the skill whose description matches the
task at hand; relative paths inside a skill resolve against its own directory.
