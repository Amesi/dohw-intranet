# Support — page layout

Decision record for [wayfinder ticket #25](https://github.com/Amesi/dohw-intranet/issues/25), part of the [UI/UX Revamp map](https://github.com/Amesi/dohw-intranet/issues/14). Resolves as **Variant A — "Form-first, list below"**, chosen from the [three-layout prototype](https://github.com/Amesi/dohw-intranet/tree/prototype/support-layout).

Builds on the sidebar shell ([navigation.md](./navigation.md)) and token system ([tokens.md](./tokens.md)). Matches the current `support/index.py` data model unchanged (subject/description/priority submission, list of the user's own issues by status).

## Structure

Single column, in this order:

1. **Page header** — title + one-line description of the page's purpose.
2. **New issue form** — subject (text input), description (textarea), priority (select: Low/Medium/High), submit as a bare gold-underlined text link (per tokens.md's button pattern) — always visible, not gated behind a reveal trigger.
3. **Your issues** — a hairline-divided list below the form, each row: subject, status pill (hollow outline, semantic color per status: open/in-progress/closed), date.

Continues the same single-column instinct as Circulars (#21) — Support's task set (submit, then optionally check status) is simple enough that neither a persistent side-by-side form (Variant B) nor gating the form behind a reveal trigger (Variant C) earned its complexity here.

## What was rejected and why

- **B — Split, form always visible in a side column** — dropped. The persistent two-column split was judged more layout complexity than the page's actual task volume (typically one submission, occasional status checks) warrants.
- **C — Tracker-first, form on demand** — dropped. Assumed most visits are status checks rather than new submissions; no evidence supported that assumption over the simpler always-visible form.

## What this doesn't cover

- Real status taxonomy beyond Open/In progress/Closed if the underlying `Issue` doctype's actual status values differ — implementation detail, verify against real data when built

## Source

Full three-variant prototype (B "Split, form persistent" and C "Tracker-first," not chosen, alongside A) is preserved on branch [`prototype/support-layout`](https://github.com/Amesi/dohw-intranet/tree/prototype/support-layout) as the primary source, not merged to main.
