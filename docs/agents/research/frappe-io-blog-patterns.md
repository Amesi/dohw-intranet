# frappe.io/blog — listing, card, and article patterns

Research feeds a wayfinder planning session for a "Blog" feature on the DoWH intranet (ERPNext-based staff portal, Papua New Guinea Dept of Works & Highways), modeled on frappe.io's visual/structural language. This portal already completed a frappe.io-modeled UI/UX revamp — see `docs/agents/research/frappe-io-design-patterns.md` (typography scale, spacing, color usage, card/button anatomy, persistent left-sidebar navigation) for the shared design-token context this doc assumes.

## Method

Primary-source inspection, same approach as the earlier navigation research: pages fetched directly with `curl` (real shipped HTML/CSS, not a markdown-summarized render) and the inline `<style>` blocks Frappe Builder emits (one full declaration block per generated class, e.g. `.fb-1ca1dd88{...}`) parsed for exact `px`/`rem` values. Pages inspected:

- `https://frappe.io/blog` (main listing)
- `https://frappe.io/blog/engineering` (category archive — a **different, older template**, see §3)
- `https://frappe.io/blog/engineering/reestablishing-determinism-in-test-suite` (article)
- `https://frappe.io/blog/engineering/building-great-software-with-agentic-coding` (article, second sample to confirm the template is consistent and not a one-off)
- `https://frappe.io/blog?blogger=Rushabh%20Mehta` and `https://frappe.io/blog?search=Ruthra` (checked whether these render a distinct author page — see §6)
- `https://frappe.io/assets/blog/dist/css/blog.bundle.TVKFQVDY.css` (shipped stylesheet for the legacy category-page template)

**Important finding that shapes this whole doc**: frappe.io is currently running **two different blog UI systems side by side** — the top-level `/blog` listing has been rebuilt in Frappe Builder (the same tool/design language as the rest of the frappe.io marketing site, per the earlier navigation research), but category-archive pages (`/blog/<category>`) and individual article pages still run on the older Frappe Framework "website" blog module (Bootstrap grid, `blog.bundle.css`, server-rendered Jinja). This is a mid-migration site, not one unified design — worth knowing before treating every observed detail as "the" frappe.io blog pattern.

---

## 1. Listing page layout (`/blog`)

**Shape: single-column vertical list, not a grid.**

- Root list container (`.fb-b2b62848`): `flex-direction: column`, `gap: 10px`
- Each row (`.fb-7ecf5200`): `gap: 20px`, `width: 100%`
- Whole list column is capped at **`max-width: 600px`, `width: 90%`** — same 600px narrow reading-column constraint used on the article page (§4) and, per the earlier research, close to the site's general content-column sizing. This is *not* a wide magazine grid.
- **No featured/pinned post treatment.** The newest post (checked: "Product Updates for July 2026") uses the exact same row markup/classes as every other row — no larger hero card, no distinct styling for position #1. It's a plain reverse-chronological list.
- **Pagination, not infinite scroll** — but it's JS/API-driven, not real URLs: `<nav class="pagination"><a class="previous">Previous</a><a class="position-1">1</a><a class="position-2">2</a><a class="position-3">3</a><a class="next">Next</a></nav>`. All page-number anchors are `href="#"` — clicking almost certainly triggers a client-side fetch against a Frappe API endpoint rather than navigating to `?page=2`. 3 pages were visible on page 1 (≈20 posts/page × 3 ≈ 60 posts total).
- Page header: eyebrow `"BLOG"` — 11px/600, uppercase, 0.99px letter-spacing (matches the eyebrow spec already logged in the navigation-patterns doc) — then a page tagline in place of a literal "Blog" H1: **"Stories behind the magic"**, Newsreader 32px/500, line-height 130%, left-aligned. Next to it, a lone RSS icon-link (§7).
- Below the header sits an empty `<div class="filter-area">` — populated client-side, presumably a search box and/or category control. **Could not be inspected from static HTML** — flagged as a gap, same caveat pattern as the earlier research's hover-state gaps.
- The persistent left sidebar nav (`hr-sidebar`, `frappe-sidebar-toggle`) documented in the navigation-patterns research is present on `/blog` too — the blog listing sits inside the same site-wide sidebar shell, not a standalone marketing page.

Source: `https://frappe.io/blog`.

---

## 2. Post card anatomy (`/blog` listing rows)

Extracted directly from the repeated `blog-post-card` markup (20 rows on page 1, each structurally identical):

| Element | Present? | Detail |
|---|---|---|
| Thumbnail image | Yes | `115px × 64px`, `border-radius: 8px`, 1px hairline border, `object-fit: cover` — small, left-aligned, **not** a full-width hero image on desktop. On mobile (≤576px) the row flips to `flex-direction: column` and the image becomes full-width `180px` tall. |
| Title | Yes | 15px/600, line-height 150%, 0.21px letter-spacing |
| Excerpt/dek | Yes | 15px/**420** (fractional weight, per the earlier research's variable-font finding), line-height 157% |
| Author name | Yes | **Text only, no avatar image** on the listing row — just the name string |
| Author avatar | No | Not present at listing-row scale (avatars only appear on the article page and on the *other*, legacy card template — see §3) |
| Publish date | Yes | e.g. `"1 Aug 2026"`, 13px/420 |
| Category | Yes | Shown inline in the meta row as `"In [Category] by [Author] · [Date]"` — plain text, not a colored chip/badge |
| Reading time | **No** | Not shown on the listing row at all (it *does* appear on the article page itself, see §4 — inconsistent between the two) |
| Tag chips | No | No separate tag pills observed anywhere on the listing |
| Small icon + counter | Yes | A speech-bubble-shaped icon + a numeral (e.g. `"0"` on the newest post) sits at the row's right edge — most likely a comment or reaction count preview, given the live comment system found on article pages (§4). `display: none` on mobile. |
| Row divider | Yes | 1px hairline (`.frappe-divider`) between every row — this is a **list with dividers**, not boxed/bordered cards (consistent with the "chromeless cards" pattern already logged in the navigation-patterns doc for `/products`) |

Row anatomy top-to-bottom/left-to-right on desktop: `[thumbnail 115×64] [title] [dek] [category · author · date row] ...... [icon+count]`, divider, repeat.

Source: `https://frappe.io/blog` (raw markup for the `blog-post-card` template).

---

## 3. Categories / tags

- **23 real categories** exist, enumerated via a `<select id="category-select">` "Browse by category" dropdown — this dropdown, however, **only appears on the legacy `/blog/<category>` template**, not on the new `/blog` listing (which has the still-unobserved empty `filter-area` instead). Full list, in the order shipped:

  Business, Community Stories, Company, Culture, Customer Stories, Engineering, ERPNext, Events, Frappe Books, Frappe Cloud, Frappe CRM, Frappe Drive, Frappe Helpdesk, Frappe HR, Frappe Insights, Frappe Learning, Frappe School, Frappeverse, Marketing, Open Source, Partner Stories, Product Updates, Team

  Plus a "Show all blogs" option. (Confirmed the 8 categories seen across the 20 posts sampled on page 1 of `/blog` — Product Updates, Culture, Partner Stories, Engineering, Community Stories, Team, Frappe CRM, Frappe Cloud — are a subset of this larger 23-category set.)
- **Category page structure is a completely different template** from the main listing (§1's single-column list): it's a **3-column Bootstrap card grid** — `col-md-4` (3 cards/row at ≥768px viewport), collapsing to `col-sm-12` (1 card/row) below that. Confirmed via `blog.bundle.css`.
  - Cover image: `height: 12rem` (192px), full-width, `object-fit: cover`, bordered card (`1px solid`)
  - **Fallback cover** for posts with no image: a flat `#ededed` gray block with centered text, `font-size: 1.2rem`, color `#7c7c7c` — i.e., there's a designed empty-state for missing cover art, not a broken-image icon
  - Card body: uppercase category label (small, muted) → title (`<h5>`) → excerpt paragraph → footer row with a **real circular avatar image** (`avatar avatar-medium`, actual photo), author name (linked to `/blog?blogger=Name`), date, and **`· X min read`** — reading time *is* shown here, unlike the new listing template
  - Category page header: `<h1>{Category}</h1>` + static subtitle `"Posts filed under {Category}"`
- No tag-chip system was found anywhere (categories are the only taxonomy; no secondary freeform tags).

Sources: `https://frappe.io/blog/engineering`, `https://frappe.io/assets/blog/dist/css/blog.bundle.TVKFQVDY.css`.

---

## 4. Individual article page

Confirmed identical structure on two separate articles (`reestablishing-determinism-in-test-suite`, `building-great-software-with-agentic-coding`) — this is a stable template, not a one-off.

- **No hero/cover banner image at the top of the article.** The page opens directly with a centered text block: title → dek → byline row → a decorative horizontal squiggle SVG divider → body content. (The cover image used for the listing/category-grid thumbnail does not reappear at the top of the article itself.)
- **Title**: Newsreader, **32px/500**, line-height 130%, **center-aligned**, in a column capped at `max-width: 600px`
- **Dek/subtitle**: 17px/400, line-height 150%, center-aligned — same size/weight as the site's "lead paragraph" style logged in the earlier navigation-patterns research
- **Byline placement**: centered row directly under the dek — real circular author photo (`24px`, growing to `32px` on mobile), `"By"` + author name (both 13px/420, muted gray), then `·`, publish date, `·`, and **`"X min read"`** (reading time *is* present per-article, just not on the listing row — see §2)
- **Table of contents: none.** No TOC sidebar or in-page nav was found. However, body headings (`<h2 id="preface">`, `<h4 id="problem-test-runner">`) **do carry slugified `id` attributes**, so anchor-linking would work if a TOC were added later — the scaffolding exists even though no TOC UI is rendered.
- **Body typography**: content wrapped in `class="blog-content prose"` (Tailwind-Typography-style prose class). Base rule read from inline CSS: 15px/420/157% line-height, with what looks like a global prose-reset applying 16px/400/1.6 on top — body copy renders around **15–16px**, i.e. only slightly larger than the site's dense 13–15px UI type scale, not a big jump to "reading" size. Code blocks are syntax-highlighted via **Prism.js** (`prismjs@1.30.0` loaded from cdn.jsdelivr.net). Body column width: `max-width: 600px` (same cap as the title), inside an outer page container `max-width: 790px, width: 80%` (`90%` on mobile).
- **Related-posts section: none.** Checked both articles for "related", "you might also like", "read next" — zero hits.
- **Newsletter/subscribe capture: none.** No inline subscribe form anywhere on either article page.
- **Social share**: a single generic `"Share"` icon + label (link/upload-style icon) — **not** a row of per-platform icons (no Twitter/LinkedIn/Facebook share links found in static HTML). Most likely triggers the native Web Share API or a copy-link action.
- **Comments: yes, a real, live, first-party comment system** (not Disqus/embedded third-party):
  - A `<form class="comment-form">` right after the Share control: `"Add your comment"`, a `Full Name` text input, a textarea (placeholder `"Ctrl + Enter to post."`), and a `Comment` submit button
  - Existing comments render below with a letter-avatar fallback (first initial, e.g. `"G"`), commenter name (a mix of real names like *"Girish Budhwani"* and anonymous **`"Guest"`** entries — no login required to comment), date, and body text
  - One article sampled had 6 comments, the other had 1 — so this is a genuinely used feature, not vestigial
- **Structured data**: a `schema.org/BlogPosting` JSON-LD block is present — `headline`, `description`, `image`, `author` (`Person`, with a `url` — see §6), `publisher` (`Frappe Technologies` + logo), `datePublished`, `dateModified`, `articleSection`. Good SEO hygiene worth mirroring if DoWH's blog is ever indexed (even for an intranet, useful for internal search/RSS metadata).

Sources: `https://frappe.io/blog/engineering/reestablishing-determinism-in-test-suite`, `https://frappe.io/blog/engineering/building-great-software-with-agentic-coding`.

---

## 5. Authorship

- **Single author per post** — every card, listing row, and article byline showed exactly one author name; no co-author/multi-byline pattern was observed anywhere.
- **No dedicated author bio/archive page.** The JSON-LD `author.url` points to `https://frappe.io/blog?search={FirstName}`, and the category-page author link points to `https://frappe.io/blog?blogger={FullName}` — **two different, inconsistent query-param mechanisms**, and both were confirmed (via direct fetch) to just render the **same generic `/blog` listing page** (identical byte size to the un-filtered listing), meaning any actual filtering happens client-side in JS, not server-side. There is no `/blog/author/{name}` route, no author photo/bio card, no "posts by this author" curated page — it's a filtered search view at best, not a real profile page.

Sources: JSON-LD blocks on both sampled articles; direct fetch of `https://frappe.io/blog?blogger=Rushabh%20Mehta`.

---

## 6. RSS / subscribe

- **RSS feed exists and is linked from the main listing header**: `<a href="/rss.xml" target="_blank" title="Blog RSS feed">` next to the page tagline, rendered as a small icon-only link (standard RSS glyph SVG, no text label beyond the `title` tooltip).
- **No email/newsletter subscribe mechanism** was found anywhere on the listing or article pages — RSS is the only "follow the blog" affordance frappe.io surfaces.

Source: `https://frappe.io/blog`.

---

## 7. Distinctly frappe.io-flavored details (not generic blog boilerplate)

- **The mid-migration split itself** (§0/throughout) — a still-actively-used older Bootstrap template for category archives + articles, sitting behind a freshly Builder-rebuilt top-level listing. If DoWH mirrors "frappe.io's blog," it should mirror the *newer* Builder-style listing (§1–2) as the target look, not the older card-grid (§3), since that's clearly the direction frappe.io itself is moving.
- **Reverse-chronological plain list with zero featured/pinned treatment** — no editorial "hero post" logic at all, even though the newest post is objectively "top of page." This is a much flatter/less curated presentation than most corporate blogs.
- **Reading time only shown on the article itself, not on any listing/card surface** — an odd, likely unintentional inconsistency (present on legacy category cards, absent on the new listing rows, present again on the article) rather than a deliberate design choice.
- **No cover/hero image on the article page** — cover art is purely a *listing-thumbnail* device; once you're reading, the page is text-first (title/dek/byline, no big banner).
- **Live, no-login-required commenting with a "Guest" fallback identity** — unusual for a modern SaaS marketing blog (most have moved to Disqus, a CMS-gated system, or removed comments entirely). Reflects Frappe's general "open, low-friction" community ethos rather than lead-gen instrumentation.
- **No related-posts, no newsletter capture, no per-platform share icons** — three features that are near-universal on marketing blogs (especially B2B SaaS ones optimizing for funnel/retention) are conspicuously absent here. The blog reads more like a public engineering/company journal than a lead-gen content-marketing surface.
- **Narrow, consistent 600px content column** used identically for the listing list and the article body/title — reinforces the "dense, docs-site-like" reading-column sizing already noted in the navigation-patterns research, rather than a wide magazine-style layout.

---

## Open gaps for a follow-up pass

1. **The listing page's `filter-area` div** — empty in static HTML, populated client-side. Whether it's a search box, category chips, or both could not be determined without a live JS/devtools pass.
2. **Whether `/blog` pagination (`href="#"`) is a true client-side API fetch or something else** — inferred from the anchors' shape, not confirmed by observing network calls.
3. **Exact behavior/target of the "Share" button** — Web Share API vs. copy-to-clipboard vs. something else couldn't be confirmed from static markup alone.
4. **The comment-icon+counter on listing rows** (§2) — its exact semantics (comment count vs. reaction/like count) is an inference from icon shape, not confirmed against an article with a nonzero count.
5. **Whether the legacy `/blog/<category>` template is being actively phased out** or will persist — relevant to whether DoWH should treat it as "current frappe.io style" at all; flagged as an assumption in §7.

---

## For DoWH

**What clearly won't translate:**
- **Public marketing CTAs and lead-gen absence-as-feature** — frappe.io's blog deliberately skips newsletter capture and heavy share/CTA machinery because it's optimizing for a public, SEO-driven audience funnel that doesn't apply to an internal staff portal. DoWH shouldn't read "no subscribe form" as a pattern to copy — an intranet blog *should* have a lightweight "notify me" or pin-to-dashboard mechanism instead, since RSS-only discovery assumes a tech-savvy public audience DoWH staff won't have.
- **No-login, "Guest" commenting** — appropriate for a public company blog trying to lower friction for external readers; wrong for a staff intranet, where comments should be tied to the authenticated ERPNext/Frappe user (real name, department, avatar from the existing staff directory) rather than an anonymous "Guest" fallback.
- **The author-as-search-query non-pattern (§6)** — this is a genuine frappe.io shortcoming (two inconsistent query params, no real profile page), not a design choice worth reproducing. DoWH already has a staff directory (per the existing UI/UX revamp) — an author byline should link to that real directory profile, not fake an author page via a filtered search.

**What would translate well:**
- **The single-column, dense reading-list layout with small left-thumbnail + text (§1–2)** and the **narrow ~600px content column (§4, §7)** — both fit an intranet's "quick scan, then read" usage pattern better than a wide magazine grid, and align with the docs-site-like sidebar shell DoWH already adopted per the navigation-patterns research.
- **The category system as a single flat taxonomy (§3)**, sized appropriately — DoWH won't need 23 categories, but a small fixed set (e.g. Announcements, Projects, HR, Safety, Tenders) mapped the same way (one category per post, shown as plain text in the meta row, not a colored chip) fits the site's already-documented restrained/near-monochrome visual language.
- **JSON-LD/structured-data hygiene and RSS (§4, §6)** — cheap to add, useful even internally (e.g. for a future digest email or a "what's new" widget elsewhere in the portal), and consistent with the frappe.io source of truth this revamp is modeling.
