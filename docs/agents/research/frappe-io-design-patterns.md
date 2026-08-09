# frappe.io visual & navigation patterns — research findings

Research ticket: [#15](https://github.com/Amesi/dohw-intranet/issues/15), part of the map [#14 "UI/UX Revamp — frappe.io Model"](https://github.com/Amesi/dohw-intranet/issues/14). Feeds into [#19 Design tokens & component restyle](https://github.com/Amesi/dohw-intranet/issues/19) and [#20 Navigation — IA grouping & mega-menu prototype](https://github.com/Amesi/dohw-intranet/issues/20).

## Method

This is a **primary-source inspection** of frappe.io, not a description from memory. Pages were downloaded directly (`curl`) and their real, shipped CSS was parsed (not a markdown-summarized render), including:

- `https://frappe.io/` (homepage)
- `https://frappe.io/products`
- `https://frappe.io/pricing`
- `https://frappe.io/erpnext`
- Linked stylesheets: `https://frappe.io/builder_assets/tokens.css` (design-token custom properties), `https://frappe.io/files/page_styles/builder-asset-style.css`, `https://frappe.io/assets/builder/reset.css`

frappe.io is built with **Frappe Builder** (Frappe's own no-code site builder). Instead of Tailwind-style utility classes, each element gets an inline-generated class (e.g. `.fb-1ca1dd88`) whose full declaration block is emitted once in a `<style>` tag — this made it possible to read exact `px` values, `font-family`, `border-radius`, etc. directly from the HTML source, without needing a browser inspector. Where noted below, a value **could not** be determined this way (e.g. `:hover` pseudo-states, which don't always appear as static CSS) — those are flagged explicitly as needing a live devtools pass.

All hex values below are the **light-mode** value of `light-dark(light, dark)` CSS declarations unless stated otherwise; the site ships a dark-mode variant of nearly every color token.

---

## 1. Typography scale

**Font families** (observed in `reset.css` `@font-face` and page `<link>` tags):
- **Inter** (variable font, self-hosted as `InterVar`, `/assets/builder/fonts/Inter/Inter.var.woff2`, weight range 100–900, includes an italic variable axis) — used for **all UI, nav, body, and label text**.
- **Newsreader** (Google Font, `https://fonts.googleapis.com/css2?family=Newsreader:wght@400;500;600`) — a serif, used **only for headings/display text**, never for body or UI copy.
- Global `:root` also sets `letter-spacing: 0.02em`, `font-variation-settings: "opsz" 24`, and antialiased smoothing — applied site-wide, not per-heading.

**Observed sizes/weights/line-heights** (directly read from shipped CSS rule blocks):

| Role | Font | Size | Weight | Line-height | Letter-spacing | Source |
|---|---|---|---|---|---|---|
| H1 (homepage hero) | Newsreader | 36px (32px under 576px) | 500 | 130% | — | frappe.io/ |
| H1 (product page, `/erpnext`) | Newsreader | 32px | 500 | 130% | — | frappe.io/erpnext |
| Card/section heading (~H3) | Newsreader | 20px | 600 | 115% | 0.3px (1.5%) | frappe.io/ |
| Eyebrow / section label (e.g. "PRODUCTS") | Inter | 11px | 600, uppercase | 115% | 0.99px (~9%) | frappe.io/products |
| Lead paragraph / intro copy | Inter | 17px | 400 | 150% | — | frappe.io/ |
| Nav item / CTA text | Inter | 14px | 500 | 115% | 0.21px (1.5%) | frappe.io/ |
| Card title (product grid) | Inter | 15px | 600 | 115% | 0.24px (1.6%) | frappe.io/products |
| Card description | Inter | 13px | 420 | 150% | — | frappe.io/products |
| Table body text | Inter | 14px | 420 | 115% | 0.28px (2%) | frappe.io/ |
| Table header (uppercase) | Inter | 11px | 500, uppercase | 115% | 0.99px | frappe.io/ |

**No H2/H4/H5/H6 examples with distinct sizes were captured** in the pages sampled — flagged as a gap; only H1-equivalent (32–36px) and one card-heading size (20px) were found in the three pages inspected, plus body/UI sizes clustering tightly at **13–15px** (13px was the single most common font-size on `/erpnext`, appearing 166 times) — i.e., frappe.io's actual UI type scale runs noticeably **smaller and denser** than a typical marketing site (most "body" text is 13–15px, not 16px+).

**Notable pattern**: font-weight values aren't restricted to 400/500/600/700 — fractional weights like **420, 530, 630** appear, only possible because Inter is loaded as a true variable font. Letter-spacing scales roughly with size (~1.5–2% of font-size for normal text) except uppercase micro-labels, which get much wider tracking (~9%).

---

## 2. Spacing / grid system

- **No classic centered container max-width** (e.g. 1200/1280px) was found on any of the 4 pages. This is because frappe.io's layout is **sidebar + fluid content**, not a centered marketing container — see §5.
- **Base spacing unit**: values observed across all three pages cluster at **4, 6, 8, 10, 12, 16, 20, 24, 28, 32px**. This is consistent with a loose 4px-based scale but is **not a rigid 8pt grid** (6px, 10px, and 20px all appear, which a strict 8pt system wouldn't produce). Treat "4px base, common steps of 8/12/16/20/24/32" as the inferred scale.
- **Card/grid gutters** (`/products` business-apps grid): `grid-template-columns: repeat(2, minmax(200px, 1fr))`, **20px** gap between grid cells, **16px** gap in the internal vertical stack of each card group, collapsing to a single-column flex stack under the 576px breakpoint.
- **Pricing/plan cards** (`/pricing`): ~364px width, **20px** internal padding, **24px** internal content gap, 10px radius.
- **Breakpoints**: `max-width: 576px` (mobile) and `max-width: 1023px` (tablet/sidebar-collapse) recur identically across home, products, and pricing — these are frappe.io's two real responsive breakpoints, directly observed, not guessed.
- **Section vertical padding**: could **not** be reliably captured — the pages sampled are comparatively short "hub" pages (sidebar + short hero + link/product grid), not long scrolling landing pages with alternating full-width sections, so no large (60–120px) section-padding values were found in the static export. Only small component-level paddings (6–10px on buttons/rows) were present. **This needs a live browser pass on a longer frappe.io landing page** (e.g. a specific product's marketing page) to capture true section rhythm — flagged as unresolved.

---

## 3. Color usage beyond primary green/teal

This is the most notable finding of the research: **on the pages actually inspected, frappe.io's marketing site uses almost no green/teal.** It is a near-monochrome, ink-and-gray system.

**Token usage frequency** (counted every `var(--token)` reference across home + products + pricing, then resolved via `tokens.css`):

| Rank | Hex (light) | Uses | Role |
|---|---|---|---|
| 1 | `#383838` | 185 | secondary ink / body text |
| 2 | `#525252` | 172 | muted ink |
| 3 | `#171717` | 126 | primary ink / heading text / near-black |
| 4 | `#999999` | 50 | tertiary muted text |
| 5 | `#7c7c7c` | 44 | label/caption gray |
| — | `#ededed`, `#e2e2e2`, `#c7c7c7` | 14–24 each | hairline borders |
| — | `#ffffff` | 16 | primary surface |
| — | `#f3f3f3`, `#f8f8f8` | 7–8 | subtle secondary surface (e.g. sidebar background) |
| — | `#0d8ef8` (blue) | 8 | **only** as an SVG icon fill on `/pricing`, not a UI accent |

**No green/teal token appeared even once** in the three pages' actually-applied CSS, despite `tokens.css` containing dozens of green/teal-family tokens (e.g. `#0a857b`, `#0f736b`, `#43ac79`). Those tokens almost certainly belong to a much larger, **shared design-token file** (300+ custom properties covering red/orange/yellow/blue/purple/pink/green families, each with light+dark pairs) — this is very likely the **shared Frappe Framework/Desk UI kit** (semantic success/warning/error/info colors, "tag" hues for labels, etc.) bundled into the marketing site's build, rather than a palette curated for frappe.io itself. This distinction (large available palette vs. tiny actually-used palette) is important and directly observed, not assumed.

**Practical read for the revamp**: frappe.io's own visual language is *not* "green-primary" — it is **restrained, near-grayscale**, with color held back for very small, specific accents (a logo mark, one status pill, occasional icon), and even primary CTAs render in plain ink-gray text rather than a brand-colored fill (see §4). If the goal is to genuinely mirror frappe.io's *restraint*, DoWH's revamp should treat Gold #FFBF00 the same way frappe.io treats its green — as a rare, deliberate accent, not a dominant UI color — while keeping neutrals (grays/near-black/white) as the workhorse palette. This is an inference from the observed data, worth flagging explicitly to whoever owns #19/#20 since it may run counter to an assumption that frappe.io is "colorful."

Sources: `https://frappe.io/`, `https://frappe.io/products`, `https://frappe.io/pricing`, `https://frappe.io/builder_assets/tokens.css`.

---

## 4. Card and button component anatomy

**Product "cards" (`/products` grid — Business Apps, Developer Tools, etc.) are chromeless.** Directly observed: no `border`, no `background`, no `border-radius`, no `box-shadow` on the card wrapper. Each is just: icon image (≈32–40px) + title (Inter 15px/600) + one-line description (Inter 13px/420), stacked with a 12px icon-to-text gap, in the 2-column grid described in §2. This is a flat "icon + text list" masquerading as a card grid, not an actual boxed card.

**Pricing/plan cards (`/pricing`) ARE genuine bordered cards**:
- `border: 1px solid` — hairline gray (`#ededed` light / `#242424` dark)
- `border-radius: 10px`
- `padding: 20px`
- internal `gap: 24px`
- width ≈ 364px
- **no `box-shadow`** — elevation is a hairline border only. (One nearby sibling rule literally emitted `box-shadow: None` as a value, and no shadow was found on any card or button sampled — flat design, not skeuomorphic.)

**Buttons — two distinct anatomies observed, both far lighter-weight than a typical filled CTA button:**

1. **Text-link CTA (the dominant pattern site-wide)** — e.g. "Log in or create account" (homepage nav), "Start free trial" (pricing utility bar): no container, no background, no padding-as-button — just label text (Inter 14px/500, ink-gray color, not brand color) + a small trailing chevron-right icon (12–16px SVG), ~8px gap. This is effectively a styled link, not a button.
2. **Filled pill button (secondary, seen once — "Contact us" on `/pricing`)**: `height: 36px`, `border-radius: 8px`, `padding: 0 16px` (vertically centered content), `background`: neutral surface gray (`#f3f3f3` light / `#292929` dark — **not** a brand color), no border, no shadow, label (14–15px) + trailing 16px icon.
3. Small uppercase tag/eyebrow pills also use `border-radius: 8px`, `padding: 6px 8px`, occasionally a solid dark fill (`#171717`).

**Border style throughout**: consistently 1px solid hairline, drawn from the neutral border-gray tokens. No thick (2px+) borders were observed anywhere.

**Hover/active states — partially observable, partially not:**
- Directly observed in shipped CSS: `.nav-link-item:hover` and `.active` swap background to light gray (`#f3f3f3` light / `#292929` dark); the **active** sidebar item additionally gets `box-shadow: 0px 1px 2px rgba(0,0,0,.2)` plus a white/dark fill — this is the one clear, concrete elevation/shadow use case found on the whole site, and it's used to mark "current page in the sidebar," not for generic cards.
- Transitions consistently use `.2s ease` (`transition: all .2s ease` on the sidebar container; `transition: .2s ease` on nav-menu items in `builder-asset-style.css`).
- **Could not confirm**: explicit `:hover` background/opacity changes for the pill buttons or text-link CTAs — no such rule was present in the static export for those specific classes. **A live browser devtools `:hover` inspection pass would be needed** to see if/how those states change; flagged as unresolved rather than guessed.

Sources: `https://frappe.io/`, `https://frappe.io/products`, `https://frappe.io/pricing`.

---

## 5. Mega-menu navigation structure & behavior

This is the biggest surprise of the research and directly affects how #20 should be scoped: **frappe.io does not use a horizontal top navbar with hover-triggered mega-menu dropdowns.** Its primary navigation is a **persistent left sidebar**, present and structurally identical across every page sampled (home, `/products`, `/pricing`, `/erpnext`) — a "docs-site" pattern (comparable to GitBook/Notion), not a classic SaaS marketing navbar.

**Sidebar anatomy (directly observed):**
- Full viewport height (`height: 100vh`), fixed to the left, 1px right hairline border, subtle off-white background (`#f8f8f8` light / `#1f1f1f` dark)
- 8–10px internal padding, 4px gap between nav rows
- Contains: logo (full + a "mini" collapsed-icon variant), a hamburger toggle (`frappe-sidebar-toggle`), then the nav item list
- **Column count: 1** — it's a single vertical column, not a multi-column mega-menu panel

**Grouping logic (from `/products`, representative of the full nav)**: **14 destinations**, structured as flat top-level items plus two labeled sub-groups:
- Flat top-level: Contents, Welcome, Home, Products, Partners, Blog
- Group "**About**": Story, Team, Values, Vision
- Group "**Resources**": Events, Testimonial, Incubator, Careers

A separate, richer flyout exists behind the sidebar's "**Contents**" link — a fuller sitemap surfacing additional destinations not in the main rail (Customers, Culture, Design, Community, Certifications). So the real IA is **two-tier**: ~14 always-visible primary items, plus a complete sitemap one click away for long-tail pages.

**The actual "mega-menu"-shaped content lives on the dedicated `/products` page itself**, not in a navbar dropdown — it's a permanently-expanded grid rather than a hover flyout, but the **grouping logic is directly transferable** to a mega-menu design:

| Category | Items |
|---|---|
| Business Apps | ERPNext, Frappe HR, Learning, Insights, CRM, Helpdesk, Lending (7) |
| Developer Tools | Framework, Builder (2) |
| Productivity Tools | Drive (1) |
| Infrastructure | Cloud, Press (2) |
| Libraries | Bench, Datatable, Charts, Gantt (4) |

Each item renders as icon + title (15px/600) + one-line description (13px/420), 2-column grid, 20px row gap (see §2/§4). This "category header + icon/title/description tile" shape is the pattern worth prototyping for #20, even though on frappe.io itself it's a full page rather than a dropdown panel.

**Hover vs. click trigger — not directly confirmable from static HTML.** The sampled pages don't contain a literal JS-driven dropdown; the sidebar groups are always-expanded (not toggled), and the category grid lives on its own page. **Flagged as unresolved**: it's possible other frappe.io subpages (e.g. `/partners`, which showed similar tile markup with icon + title + description rows during this research) use a genuine hover-triggered flyout — the DOM does contain a `.sidebar-backdrop` element and `.nav-link-item:hover` CSS rule, but a `.sidebar-backdrop` is most consistent with a **mobile drawer dismiss-overlay**, not a desktop hover flyout. A live browser/JS interaction pass on frappe.io (with devtools open, testing actual mouse hover) would be needed to confirm whether any true hover-mega-menu exists elsewhere on the site.

**Mobile/tablet collapse behavior (directly observed):**
- Under the **1023px** breakpoint, the sidebar becomes an **off-canvas drawer**: `width: 250px`, slides from `left: -250px` to `0`, presumably toggled by the hamburger button (`frappe-sidebar-toggle`), with a `.sidebar-backdrop` overlay for dismissal.
- Under the **576px** breakpoint, some nav elements are simply hidden (`display: none`) rather than reflowed — e.g. the "Log in or create account" nav CTA disappears entirely on mobile rather than adapting.

Sources: `https://frappe.io/`, `https://frappe.io/products`, `https://frappe.io/pricing`, `https://frappe.io/erpnext`.

---

## Open gaps for a follow-up browser-based pass

Flagging explicitly, per the ticket's instruction to be honest about what couldn't be determined from static inspection:

1. **Exact `:hover`/`:active`/`:focus` styling** for buttons and links (background/opacity/color shifts) — not present in the static CSS export.
2. **Section-level vertical padding/rhythm** on a long-form landing page — the pages sampled were short "hub" pages; a product marketing page with multiple stacked sections would be needed.
3. **Whether a genuine hover-triggered mega-menu exists anywhere on frappe.io** (e.g. on `/partners` or a product page) — the sampled pages show a sidebar + a permanently-expanded grid page instead, but this can't fully rule out a dropdown elsewhere without live JS interaction.
4. **H2, H4–H6 sizes** — only H1-equivalent (32–36px Newsreader) and one card-heading size (20px Newsreader) were captured; a fuller heading scale wasn't visible in the three pages sampled.
