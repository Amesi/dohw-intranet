# Blog — internal editorial section

Decision record for the [Blog map](https://github.com/Amesi/dohw-intranet/issues/42): [data model & workflow (#44)](https://github.com/Amesi/dohw-intranet/issues/44), [frappe.io/blog research (#43)](https://github.com/Amesi/dohw-intranet/issues/43), [listing & article layout (#45)](https://github.com/Amesi/dohw-intranet/issues/45). Resolves as **Variant A — "Reading List,"** the literal frappe.io/blog pattern, chosen from the [three-variant prototype](https://github.com/Amesi/dohw-intranet/tree/prototype/blog-layout).

Staff-only, login-gated, a distinct content type from Circulars — see the map's Notes for the full set of destination-defining decisions. Builds on the token system ([tokens.md](./tokens.md)) and the navigation shell ([navigation.md](./navigation.md)).

## Data model & workflow

New `Blog Post` doctype: `title`, `route`, `author` (Link → Employee), `content` (rich HTML via the same editor built for Circulars' compose page), `excerpt`, `featured_image`, `category` (Select), `status` (Select), `reviewer`, `rejection_reason`, `published_date`. No `wing` field — posts are company-wide, unlike Circulars.

New `Blog Author` Check field on Employee, independent of `content_manager` — a person can hold either, both, or neither.

**States**: Draft → In Review → Published.
- Author writes, autosaves as Draft.
- Explicit **Submit for review** action moves it to In Review — no informal/implicit review.
- Any *other* Blog Author (never the same person — enforced server-side) can Approve (→ Published, sets `published_date`/`reviewer`) or Reject (→ back to Draft, with `rejection_reason` set to their note — no separate "Changes Requested" state).
- No comments/reactions — read-only for staff.

**Categories** (DoWH's own, not frappe.io's 23): Project Updates, Staff Spotlight, Department News, ICT & Systems.

## Layout — Variant A, "Reading List"

Single-column list, ~640px content column, matching frappe.io/blog's own current (post-migration) listing pattern rather than its older card-grid template:

- Small left thumbnail (92×64px, 8px radius) where a featured image exists — image is optional per the data model, so rows without one just show text.
- Title, then excerpt, then a plain-text meta line: `"In {Category} by {Author} · {Date}"` — no colored category chips, matching frappe.io's own listing (chips only appear on its legacy template).
- Hairline dividers between rows (`.dt-card-list`/`.dt-card` convention already used everywhere else). No boxed/bordered cards.
- No featured/pinned post treatment — plain reverse-chronological, matching frappe.io's own flat presentation.
- No reading time shown on the listing row (frappe.io doesn't either — it's article-page-only there, so DoWH mirrors that rather than "fixing" what reads as an intentional density choice).

**Article page**: centered title/dek/byline, no hero/cover image once reading (cover art, when present, is a listing-only device — matches frappe.io exactly), ~640px body column, reading time shown in the byline. **Byline links to the existing Staff Directory** rather than a dedicated author bio page — frappe.io itself has no real author page (just a broken, inconsistent search-query non-pattern found during research), and DoWH already has a real directory to link to instead.

**Nav placement**: new "Blog" sidebar item, between Documents and Links & Forms.

**Compose/manage area** (not variant-switched — a workflow screen, not a "look" fork): three sections — My Drafts (with a Submit for review action per row), Pending Review (posts by *other* Blog Authors, with inline Approve & publish / Reject-with-reason actions), and Published. Parallel precedent: `/circulars/new`'s dedicated compose page.

## What was rejected and why

- **B — Card Grid** — dropped. A 2-column grid with larger images reads as more "content marketing," which doesn't fit DoWH's fairly sparse initial post volume or the portal's restrained, near-monochrome visual language elsewhere.
- **C — Featured + List** — dropped. Adds an editorial "hero post" curation step frappe.io itself doesn't do (confirmed via research — even frappe.io's newest post gets no special treatment); not worth the added complexity for a small, infrequent editorial team.

## What this doesn't cover (deliberately out of scope for v1)

- **RSS/subscribe** — frappe.io has a working feed at `/rss.xml`, but that's a public-audience pattern; an internal staff blog doesn't have the same discovery problem. Not built for v1; revisit if staff ask for a "what's new" digest mechanism.
- **Search within Blog** — not included; the portal's global search (where it exists) covers this adequately for the expected post volume.

## Source

Full three-variant prototype (all variants, plus the manage-area mockup) preserved on branch [`prototype/blog-layout`](https://github.com/Amesi/dohw-intranet/tree/prototype/blog-layout), not merged to main. Real content used in the prototype (Hawaiin Bridge story, NPDS team-building, etc.) was extracted from the live [www.works.gov.pg/articles](https://www.works.gov.pg/articles) for realism, not fabricated — useful as real seed content if/when this gets built.
