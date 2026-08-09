# Dashboard — page layout

Decision record for [wayfinder ticket #24](https://github.com/Amesi/dohw-intranet/issues/24), part of the [UI/UX Revamp map](https://github.com/Amesi/dohw-intranet/issues/14). Resolves as **Variant B — "KPI grid + side-by-side charts"**, chosen from the [three-layout prototype](https://github.com/Amesi/dohw-intranet/tree/prototype/dashboard-layout).

Builds on the sidebar shell ([navigation.md](./navigation.md)) and token system ([tokens.md](./tokens.md)). Same underlying data model as the current `dashboard/index.py` (circular counts, circulars-by-wing, staff-by-wing, open issues, recent circulars) — only the arrangement changes.

## Structure

1. **KPI card grid** — a 4-up grid of bordered tiles, one per top-level metric: Circulars published, Urgent circulars, Active staff, Open issues. Each tile is a large number + label. Urgent/Open-issues tiles get the `--semantic-urgent` color on the number (per tokens.md) to flag attention without a filled background.
2. **Side-by-side charts** — Circulars-by-wing and Staff-by-wing bar charts shown in a two-column row beneath the KPI grid, so the two "by wing" breakdowns can be compared at a glance rather than requiring scroll between them.
3. **Recent circulars** — a plain hairline-divided list (per tokens.md's card pattern) below the charts, same treatment as Circulars' own list rows.

This is a departure from the flat/single-column instinct set by Circulars (#21) and continued partway by Directory's tree panel (#22) — the Dashboard's job is at-a-glance comparison across several distinct metrics, which a grid of individually-bounded tiles serves better than folding everything into one narrative column.

## What was rejected and why

- **A — Metric strip + single column** — dropped. Reads fine but under-differentiates the metrics from each other (inline numbers in a header don't carry the same "these are the headline KPIs" weight as bordered tiles), and stacking both bar charts serially makes wing-to-wing comparison across metrics harder.
- **C — Priority-first** (urgent/open-issues leading, overview below) — dropped as the *primary* structure, though its instinct (flag what's urgent) is partly preserved via the KPI grid's semantic-colored urgent/open-issues tiles rather than a separate leading section.

## What this doesn't cover

- Exact chart rendering (the prototype uses simple horizontal bar rows; whether real implementation uses a charting library or continues this lightweight bar-row approach is an implementation decision)
- Whether the KPI grid becomes a 2-up grid on narrower viewports — not addressed, follows general responsive handling once implementation starts

## Source

Full three-variant prototype (A "Metric strip + single column" and C "Priority-first," not chosen, alongside B) is preserved on branch [`prototype/dashboard-layout`](https://github.com/Amesi/dohw-intranet/tree/prototype/dashboard-layout) as the primary source, not merged to main.
