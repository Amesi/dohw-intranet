# Circulars — page layout

Decision record for [wayfinder ticket #21](https://github.com/Amesi/dohw-intranet/issues/21), part of the [UI/UX Revamp map](https://github.com/Amesi/dohw-intranet/issues/14). Resolves as **Variant A — "Single column"**, chosen from the [three-layout prototype](https://github.com/Amesi/dohw-intranet/tree/prototype/circulars-layout).

Builds on the sidebar shell ([navigation.md](./navigation.md)) and token system ([tokens.md](./tokens.md)) — this ticket only decided the Circulars page's own content structure.

## Structure

Single column, no in-page widget rail. With a persistent left sidebar already present, a second sidebar-within-the-page (the current app's Quick Stats / Tag Cloud / Recent Documents rail) was judged redundant chrome rather than useful density.

1. **Page header** — title + inline stats (`12 total · 2 urgent · 4 for action`) as plain text, not a widget card.
2. **Filter bar** — a horizontal chip bar: wing and classification as `<select>` dropdowns, tags as clickable pill chips (active tag gets a gold outline, per the token system's rare-accent rule).
3. **Circular list** — chromeless, hairline-divided (per tokens.md), chronological (newest first). Each row: circular number + title (click to expand), classification badge (hollow outline), wing/date meta line, tag chips.
4. **Detail view** — expands inline via a native `<details>` toggle under the clicked title: full body text + an attachment link. No separate detail route/page; this satisfies the "listing + detail view" requirement from the original ticket scope without a page navigation.

## What was rejected and why

- **Right-rail widgets (Quick Stats / Tag Cloud / Upcoming Deadlines)** — dropped. Redundant now that the app has one persistent left sidebar; a second rail on top of it read as clutter in review.
- **Grouping by classification** (Urgent / For Action / For Information sections) — dropped in favor of chronological order. Classification is still visible (per-item badge, filterable), just not used as the primary sort/grouping axis.

## What this doesn't cover

- Exact filter interaction (client vs. server-side tag filtering) — implementation detail, not a design decision
- Mobile column behavior below the sidebar's 1023px breakpoint — inherits [navigation.md](./navigation.md)'s drawer behavior; the single-column content itself needs no further layout decision at narrow widths since it was already single-column

## Source

Full three-variant prototype (A, plus B "Right rail" and C "Grouped by classification", not chosen) is preserved on branch [`prototype/circulars-layout`](https://github.com/Amesi/dohw-intranet/tree/prototype/circulars-layout) as the primary source, not merged to main.
