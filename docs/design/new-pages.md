# New pages — Calendar, Projects, Links & Forms Hub

Decision record for [wayfinder ticket #27](https://github.com/Amesi/dohw-intranet/issues/27), part of the [UI/UX Revamp map](https://github.com/Amesi/dohw-intranet/issues/14). Locked in as designed — see the [prototype](https://github.com/Amesi/dohw-intranet/tree/prototype/new-pages-layout).

Three pages [map #1](https://github.com/Amesi/dohw-intranet/issues/1) already decided the data source for but hasn't built yet. One cohesive layout each (not competing variants, since there's no existing page to react against) — built on the sidebar shell ([navigation.md](./navigation.md)) and token system ([tokens.md](./tokens.md)). These layouts are the *target* for map #1's eventual build of these pages, not a trigger to build them now.

## Calendar

Data source: ERPNext Calendar doctype, wing-filtered (decided in map #1).

- Month grid as the default view (7-column CSS grid, day cells with event chips — hollow gold-outline pills, matching the badge style from tokens.md), with a toggle to a chronological list view.
- Wing filter (not shown as a dedicated control in the prototype, but follows the chip-bar pattern established in Circulars/Directory).

## Projects

Data source: ERPNext Project doctype, All/Wing/Team views (decided in map #1).

- Tab bar: All / My Wing / My Team — pill-style tabs matching the gold-outline active state used elsewhere (Directory's tree active state, Circulars' tag chips).
- Card grid (2-up), each card: project name, wing, a thin progress bar (dark fill on light track, same visual language as Dashboard's bar charts), percent-complete label.

## Links & Forms Hub

Data source: custom Frappe doctype, staff-managed via Desk (decided in map #1).

- Grouped link list by category (e.g. HRMS, IT, Facilities & Assets) — category label as a small uppercase eyebrow (matching tokens.md's section-label pattern), links as chromeless hairline-divided rows with a small external-link indicator, gold underline on hover (same link-hover treatment used throughout).
- No search/filter in this design — the category grouping is expected to keep the list scannable at the staff-managed link volumes this hub is meant for.

## What this doesn't cover

- Real event/project/link data shape beyond what's already decided in map #1's data-source tickets
- Calendar's list-view detail (only the month grid was fully designed; list view is a toggle target, not fleshed out)
- Any of these pages' mobile behavior specifically — inherits the general patterns from navigation.md but wasn't re-verified per page here

## Source

Prototype preserved on branch [`prototype/new-pages-layout`](https://github.com/Amesi/dohw-intranet/tree/prototype/new-pages-layout) as the primary source, not merged to main.
