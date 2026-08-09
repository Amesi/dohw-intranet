# Distributed content management — submission/editor UI

Decision record for [wayfinder ticket #29](https://github.com/Amesi/dohw-intranet/issues/29), part of the [UI/UX Revamp map](https://github.com/Amesi/dohw-intranet/issues/14). Resolves as **Variant B — "Dedicated compose page," with a rich content editor** (redirect from the prototype's plain textarea), chosen from the [three-approach prototype](https://github.com/Amesi/dohw-intranet/tree/prototype/content-mgmt-layout).

Builds on Circulars' list pattern ([circulars.md](./circulars.md)), Support's form pattern ([support.md](./support.md)), and the token system ([tokens.md](./tokens.md)). The wing-scoping/permissions model itself was already decided in map #1 (#5, #12) — this ticket only covers the layout.

## Structure

A separate, focused compose route (`/circulars/new`), not an inline composer on the Circulars page and not a management dashboard:

1. **Breadcrumb** — "← Back to Circulars / New circular", small muted text above the title.
2. **Page header** — "New Circular" title + the route shown as page context.
3. **Scope lock** — a small pill (`Posting as {Wing} (locked)`) with a gold dot indicator, non-editable — visually communicates the wing-auto-scoping decided in map #1 without exposing a control the author can't actually change.
4. **Form fields**: Title (text input), **Content (rich editor, not plain text — see below)**, Classification (select: For information / For action / Urgent), Tags (text input).
5. **Actions**: Publish (bare gold-underlined text link, primary) and Save as draft (muted text link, secondary) side by side.
6. Publishing redirects back to the Circulars list.

## The rich content editor

Per user direction: Content uses a rich editor, not the plain `<textarea>` shown in the initial prototype. Toolbar: Bold / Italic / Underline, a separator, Link / bullet list / numbered list, a separator, blockquote / code.

**Implementation note carried from [#18](https://github.com/Amesi/dohw-intranet/issues/18)'s restyle-not-custom-build decision:** Frappe ships its own rich text editor control (used elsewhere in Frappe/ERPNext for long-text fields) — the revamp should restyle that existing control to match tokens.md rather than introducing a third-party editor library. This keeps the "restyle Frappe's primitives" strategy consistent across the whole revamp, content editing included.

## What was rejected and why

- **A — Inline composer on Circulars** — dropped. Would have made the Circulars list page (already settled as single-column and restrained, per circulars.md) carry authoring UI it wasn't designed to host, and mixes a "browse" context with an "author" context on one page.
- **C — My submissions manager** (dedicated draft/publish management view) — dropped as the primary structure. A lighter-weight compose flow was preferred over a full CMS-style management surface; if draft management becomes a real need later, it can be revisited, but the initial scope didn't call for it.

## What this doesn't cover

- Exact rich editor feature set beyond the toolbar shown (e.g. image embedding, tables) — implementation detail once the actual Frappe control is wired up
- Draft persistence/autosave behavior — not addressed

## Source

Full three-approach prototype (A "Inline composer" and C "My submissions manager," not chosen, alongside B) is preserved on branch [`prototype/content-mgmt-layout`](https://github.com/Amesi/dohw-intranet/tree/prototype/content-mgmt-layout) as the primary source, not merged to main.
