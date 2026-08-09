# Navigation — IA grouping & sidebar

Decision record for [wayfinder ticket #20](https://github.com/Amesi/dohw-intranet/issues/20), part of the [UI/UX Revamp map](https://github.com/Amesi/dohw-intranet/issues/14). Resolves as **Variant A — "Flat list"**, chosen from the [three-direction prototype](https://github.com/Amesi/dohw-intranet/tree/prototype/navigation-sidebar).

Replaces the current dark top navbar (`dohw_intranet/templates/web.html`'s `{% block navbar %}`) with a persistent left sidebar, per [#17](https://github.com/Amesi/dohw-intranet/issues/17). Styled with the Variant A token system from [#19](https://github.com/Amesi/dohw-intranet/issues/19)/[docs/design/tokens.md](./tokens.md).

## Structure

All 8 sections in a single flat column, no category grouping — this is frappe.io's own dominant pattern (a mostly-flat sidebar with only light, sparing sub-grouping elsewhere on the site), and DoWH's 8 sections are few enough that grouping would add hierarchy without adding clarity.

Order (top to bottom), by usage frequency:

1. Dashboard (marked active/current by default in the prototype — actual active state follows the current route)
2. Circulars
3. Directory
4. Calendar
5. Projects
6. Documents (Wiki)
7. Links & Forms
8. Support

Pinned at the bottom, visually separated by a divider: **Desk** (link to ERPNext Desk) and **Logout** — carried over from the current top navbar's "Desk"/session-management items.

## Desktop layout

- Sidebar: `220px` wide, full viewport height, fixed to the left.
- Background `#f8f8f8`, `1px solid #ededed` right border.
- Internal padding `10px 8px`, `2px` gap between item rows (tighter than frappe.io's observed 4px, since DoWH has fewer, denser items).
- Nav item: `7px 10px` padding, `6px` radius, `12.5px` Inter, `#525252` default / `#171717` on hover or active.
- Active state: light gray background (`#f0f0f0`) + a `2px` inset left border in DoWH Gold — the token system's one sanctioned use of Gold as an interactive-state indicator, never a fill.
- Brand mark at top: small dark square with a gold "D" mark + "DoWH Intranet" wordmark, `13px/700`.

## Mobile / responsive behavior

Mirrors frappe.io's own confirmed behavior (per [#15 research](https://github.com/Amesi/dohw-intranet/blob/research/frappe-io-patterns/docs/agents/research/frappe-io-design-patterns.md#5-mega-menu-navigation-structure--behavior)):

- **Under 1023px:** sidebar becomes an off-canvas drawer (`width: 220px`, slides in from `left: -240px` to `0`), triggered by a hamburger button in a new mobile top bar. A dark backdrop (`rgba(0,0,0,.35)`) appears behind it and closes the drawer on click.
- DoWH adopts this exact breakpoint rather than inventing a new one — no evidence surfaced during grilling that PNG staff usage patterns require a different threshold, and matching frappe.io's tested value avoids picking an arbitrary number.

## What this doesn't cover (still fog on the map)

- Whether/how the sidebar itself changes per-page (e.g. contextual sub-items when inside a section) — not raised during this ticket, out of scope unless it resurfaces
- Exact icon set (prototype uses emoji as stand-ins) — a real icon system is an implementation detail for the build phase, not decided here

## Source

Full three-variant prototype (A, plus B "Grouped by function" and C "Pinned + collapsible", not chosen) is preserved on branch [`prototype/navigation-sidebar`](https://github.com/Amesi/dohw-intranet/tree/prototype/navigation-sidebar) as the primary source, not merged to main.
