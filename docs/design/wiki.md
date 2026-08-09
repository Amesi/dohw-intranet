# Wiki/Document Library — page layout

Decision record for [wayfinder ticket #23](https://github.com/Amesi/dohw-intranet/issues/23), part of the [UI/UX Revamp map](https://github.com/Amesi/dohw-intranet/issues/14). Resolves as **Variant C — "Wiki takeover"**, chosen from the [three-direction prototype](https://github.com/Amesi/dohw-intranet/tree/prototype/wiki-layout).

Enabled by [#28's spike](https://github.com/Amesi/dohw-intranet/issues/28), which confirmed `dohw_intranet` can override Wiki's chrome templates individually via matching relative paths, and [#16's research](https://github.com/Amesi/dohw-intranet/blob/research/frappe-wiki-theming/docs/agents/research/frappe-wiki-theming.md) on the `Wiki Settings.head_html` color/typography injection point.

## Structure

Wiki keeps its own full reader chrome rather than being forced into the global sidebar shell:

1. **Global app sidebar collapses to a slim icon-only rail** (~44px, icons only, no labels) when inside `/wiki` — a "back to portal" affordance, not the full navigation surface used elsewhere.
2. **Wiki's own header** takes over: back-to-portal link, current Space name, and Wiki's native search — restyled with our tokens (colors/typography via `head_html` overrides per #16) rather than replaced.
3. **Wiki's own tab bar** (per-space page tabs) and **page tree** (space's page hierarchy) stay, restyled the same way, sitting where they already do in Wiki's own layout.
4. **Document content** renders in Wiki's own reader column, tokens applied via the `head_html` CSS-variable overrides.

## Why this over the alternatives

- **A — Global sidebar only** (Wiki's chrome fully replaced by a breadcrumb + TOC) — rejected. Wiki 3.0's own IA (space tree, tabs, search) is more mature than what a breadcrumb-only treatment would preserve; discarding it loses real navigational capability for what's expected to be a document-heavy library.
- **B — Hybrid** (global sidebar + Wiki's tree as a second panel) — rejected as the primary structure. Three navigational surfaces stacked side by side (global sidebar + wiki tree + content) was judged as more chrome than the reader needs; C's rail-only compromise keeps a portal anchor without the redundancy.

This is the one page in the revamp that deliberately breaks from the "everything gets our global sidebar" pattern established everywhere else (Circulars, Directory, Dashboard, Support all keep the full sidebar) — justified because Wiki is a semi-autonomous module with its own mature reader UI, not a page built from scratch on our design system.

## Implementation approach (per #28)

- Override `Wiki Settings.head_html` for color/typography tokens (per #16 — this is the wired, documented hook).
- Override individual chrome fragments via matching relative paths in `dohw_intranet` (per #28's trace): `templates/wiki/includes/header.html`, `includes/sidebar.html`, `includes/tabs.html` — restyle in place rather than replacing wholesale, since the underlying IA (space/tabs/tree) is being kept, not rebuilt.
- The global sidebar's "mini rail" mode (icon-only, ~44px) is new UI not otherwise used elsewhere in the revamp — a small addition to [navigation.md](./navigation.md)'s sidebar component, scoped to when the user is inside `/wiki`.

## What this doesn't cover

- Exact Wiki search modal restyling (not shown in the prototype in detail)
- Whether the mini-rail collapse-on-entering-`/wiki` behavior needs its own transition/animation — implementation detail

## Source

Full three-variant prototype (A "Global sidebar only" and B "Hybrid," not chosen, alongside C) is preserved on branch [`prototype/wiki-layout`](https://github.com/Amesi/dohw-intranet/tree/prototype/wiki-layout) as the primary source, not merged to main.
