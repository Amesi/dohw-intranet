# Design tokens & component restyle

Decision record for [wayfinder ticket #19](https://github.com/Amesi/dohw-intranet/issues/19), part of the [UI/UX Revamp map](https://github.com/Amesi/dohw-intranet/issues/14). Resolves as **Variant A — "Frappe.io literal"**, chosen from the [three-direction prototype](https://github.com/Amesi/dohw-intranet/tree/prototype/design-tokens-and-components).

Restyles Frappe's existing `frappe-ui`/Desk primitives (per [#18](https://github.com/Amesi/dohw-intranet/issues/18): restyle, not custom-build) in frappe.io's visual idiom (per [#15](https://github.com/Amesi/dohw-intranet/issues/15) research), keeping DoWH Gold/dark/Inter as the fixed brand identity (per map #1).

## Color

Near-monochrome by default — color, including DoWH Gold, is a **rare, deliberate accent**, not a dominant UI color. Mirrors frappe.io's own actual usage (near-grayscale despite having a large token file available).

| Token | Hex | Role |
|---|---|---|
| `--ink` | `#171717` | Primary text, headings |
| `--ink-secondary` | `#525252` | Body text |
| `--ink-muted` | `#999999` | Captions, meta text |
| `--border` | `#ededed` | Card dividers, hairlines |
| `--surface` | `#ffffff` | Page/card background |
| `--dowh-gold` | `#FFBF00` | Rare accent only — underline on primary actions, active-state indicators, one badge outline color. Never a background fill in this variant. |
| `--dowh-dark` | `#1A1A1A` | Reserved for chrome contexts only (e.g. a dark rail/nav), not body UI — see Navigation ticket [#20](https://github.com/Amesi/dohw-intranet/issues/20) |

Semantic (classification badges — outline/text only, no fill, in this variant):

| Token | Hex | Role |
|---|---|---|
| `--semantic-urgent` | `#c0392b` | Urgent badge text/outline |
| `--semantic-action` | `#8a6d00` | For-action badge text/outline |
| `--semantic-info` | `#7c7c7c` | For-information badge text/outline |

Full semantic/extended palette (additional classification states, imagery treatment) is still fog on the map — this covers only the three classifications already in use.

## Typography

Inter throughout (no serif — frappe.io's Newsreader headings are not adopted; DoWH's brand identity keeps a single family). Sizes run dense, matching frappe.io's actual UI (13–15px body/UI text, not 16px+).

| Role | Size | Weight | Notes |
|---|---|---|---|
| Page title | 20px | 600 | Sentence case — breaks from the current all-caps bulletin heading style |
| Card title | 14.5px | 600 | Sentence case |
| Body | 13px | 400 | |
| Caption / meta | 11.5px | 400 | Muted color |
| Button / nav label | 13.5px | 500 | |
| Badge label | 10.5px | 600 | |

## Spacing

Loose 4px-based scale (not a rigid 8pt grid), matching frappe.io's observed values: **4, 8, 12, 16, 20, 24, 32px.**

## Components

- **Buttons** — no filled containers. Primary action is a bare text label in `--ink` with a 2px `--dowh-gold` underline (offset 3px) and optional trailing chevron. Secondary action is the same shape in `--ink-muted`, no gold. This is the dominant pattern on frappe.io itself.
- **Cards** — chromeless. No border, no background differentiation, no shadow. When several appear together, separate with a single 1px `--border` divider rather than individual card chrome. (Whether a given page uses a stacked list or a grid of these chromeless cards is a per-page layout decision — see the individual page tickets.)
- **Badges** — hollow pill: 1px border in the semantic color, transparent background, colored text, `border-radius: 20px`.
- **Forms** — plain bordered inputs (`1px solid #dcdcdc`, `border-radius: 6px`), no additional chrome.

## Radius & shadow

- No shadows anywhere in this variant — flat design throughout, matching frappe.io's own near-total absence of `box-shadow`.
- Radius used sparingly: `20px` (pill) on badges only. Form inputs get a small `6px`. Everything else (cards, page sections) is unrounded, since they have no border/fill to round in the first place.

## What this doesn't cover (still fog on the map)

- Extended semantic palette beyond the three existing classifications, and imagery/illustration approach
- Motion/interaction polish (hover/active states beyond what's shown in the prototype)
- How these tokens map onto `frappe-ui`'s actual CSS custom properties during implementation — that's implementation work for when a page ticket is built, not part of this decision

## Source

Full three-variant prototype (A, plus the two variants not chosen — B "Institutional bridge", C "Dark console") is preserved on branch [`prototype/design-tokens-and-components`](https://github.com/Amesi/dohw-intranet/tree/prototype/design-tokens-and-components) as the primary source, not merged to main.
