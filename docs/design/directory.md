# Directory — page layout

Decision record for [wayfinder ticket #22](https://github.com/Amesi/dohw-intranet/issues/22), part of the [UI/UX Revamp map](https://github.com/Amesi/dohw-intranet/issues/14). Resolves as **Variant B — "Split tree + results"**, chosen from the [three-layout prototype](https://github.com/Amesi/dohw-intranet/tree/prototype/directory-layout).

Builds on the sidebar shell ([navigation.md](./navigation.md)) and token system ([tokens.md](./tokens.md)). Note this is the first page ticket where Variant A ("search-first flat grid," matching Circulars' choice) was *not* picked — the Wing→Division→Section→Branch hierarchy is deep enough that a dedicated browsing structure earned its place here, unlike Circulars' flatter classification set.

## Structure

Two-pane layout inside the content area (independent of, and nested within, the global left sidebar from navigation.md):

1. **Tree panel** (left, ~200px, bordered right hairline) — an expandable Wing → Division → Section tree, mirroring the app's existing filter hierarchy (`wing`/`division`/`branch`/`section` query params in `directory.py`). Selecting a node scopes the results panel; the selected node gets the same gold inset-left-border active indicator used for the global sidebar's active item, for visual consistency between the two navigational trees.
2. **Results panel** (right, flexible width) — a search input scoped to the selected tree node ("Search within Highways Wing…"), plus a 2-column employee card grid below it. Cards: avatar-initials circle, name, role, department, email/call links — matching the token system's chromeless, hairline-divided card style.

## What was rejected and why

- **A — Search-first flat grid** (breadcrumb chips over one flat grid) — dropped. Reasonable for Circulars' 4 wings and 3 classifications, but Directory's structure runs one level deeper (Wing → Division → Section → Branch); a flat chip row for four hierarchy levels was judged less legible than a tree.
- **C — Org chart first** (Wing-count chart leading, staff revealed below) — dropped. Treated as answering a different question ("how big is each Wing") rather than the primary task ("find this person"); the chart could resurface later as a Dashboard widget rather than Directory's primary structure.

## What this doesn't cover

- Exact tree expand/collapse interaction and how deep the visible hierarchy goes by default (Division vs. Section vs. Branch) — implementation detail
- Whether the tree panel collapses on mobile (below the 1023px sidebar breakpoint from navigation.md) — needs its own small decision when this page is actually built, since a two-pane layout is tighter on narrow viewports than Circulars' single column was

## Source

Full three-variant prototype (A "Search-first flat grid" and C "Org chart first," not chosen, alongside B) is preserved on branch [`prototype/directory-layout`](https://github.com/Amesi/dohw-intranet/tree/prototype/directory-layout) as the primary source, not merged to main.
