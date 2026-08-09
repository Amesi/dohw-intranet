# Login — page layout

Decision record for [wayfinder ticket #26](https://github.com/Amesi/dohw-intranet/issues/26), part of the [UI/UX Revamp map](https://github.com/Amesi/dohw-intranet/issues/14). Resolves as **Variant A — "Minimal centered"**, chosen from the [three-direction prototype](https://github.com/Amesi/dohw-intranet/tree/prototype/login-layout).

Uses the token system ([tokens.md](./tokens.md)) but not the sidebar shell ([navigation.md](./navigation.md)) — this page is guest-facing, logged out, no main nav applies. Note: despite the repo README's claim of an existing "Custom DoWH login template," no such template exists in the codebase yet — this was a blank-slate decision, not a restyle.

## Structure

Plain white background, no branded side panel or masthead bar. Centered, single card:

1. A small rounded-square mark (dark background, gold "D") — the only brand element beyond the wordmark.
2. "DoWH Staff Intranet" title (15px/600) + "Department of Works & Highways" subtitle (11.5px, muted), both centered.
3. Form: Email, Password (bordered inputs per tokens.md), submit as a bare gold-underlined text link (not a filled button) — same primary-action pattern used everywhere else in the revamp.
4. "Forgot password? Reset it" fine print below the form.

## What was rejected and why

- **B — Split screen, dark brand panel** — dropped. A stronger brand moment than the rest of the restyled app uses anywhere else; inconsistent with the "Gold as a rare accent" rule from tokens.md if applied to an entire page panel.
- **C — Government bulletin masthead** — dropped. Pulls back toward the pre-revamp formal/bulletin identity this whole map is moving away from; kept as a reminder that the "official government portal" instinct is still available if a future stakeholder review wants more institutional weight here specifically.

## What this doesn't cover

- Actual Frappe login-page override mechanics (custom `login_page` hook path, session/CSRF handling) — implementation detail
- Error-state design (wrong password, account locked, etc.) — not addressed in the prototype

## Source

Full three-variant prototype (B "Split screen" and C "Government bulletin masthead," not chosen, alongside A) is preserved on branch [`prototype/login-layout`](https://github.com/Amesi/dohw-intranet/tree/prototype/login-layout) as the primary source, not merged to main.
