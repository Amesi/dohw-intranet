# events.frappe.io — structure, card anatomy, and detail-page patterns

Research feeds a wayfinder planning session for revisiting the "Calendar" feature on the DoWH intranet (ERPNext-based staff portal, Papua New Guinea Dept of Works & Highways). The user pointed at `https://events.frappe.io/` specifically as "what I meant by Calendar" during that discussion, so this doc treats it as the primary source to capture precisely — not frappe.io's main marketing site or blog (covered separately in `frappe-io-design-patterns.md` and `frappe-io-blog-patterns.md`).

DoWH's Calendar feature already has a locked decision record: [`docs/design/new-pages.md`](../../design/new-pages.md) specifies a **month grid as the default view** (7-column CSS grid, hollow gold-outline pill event chips) with an un-designed "toggle to a chronological list view." That existing decision is called out explicitly in §7 below because it matters for how this research should be used.

## Method

Primary-source inspection: pages fetched directly with `curl` (real shipped HTML, not a markdown-summarized render), same method as the prior two frappe.io research docs. Fetched 2026-08-09 — this is a live production site with real upcoming/past event data, so specific dates/counts below will drift over time; the *structural* patterns are the durable finding.

Pages inspected:
- `https://events.frappe.io/` (homepage)
- `https://events.frappe.io/conferences`, `/local`, `/webinars` (the three working type-filtered landing pages)
- `https://events.frappe.io/meetups` (404 — see §3)
- `https://events.frappe.io/category/local` (HTTP 500 — see §3)
- `https://events.frappe.io/events/frappeverse-mumbai-2026` + `/guidelines` + `/venue-and-stay` (an upcoming conference's full 3-tab microsite)
- `https://events.frappe.io/events/frappe-yatra-coimbatore-2026` (a past meetup's 2-tab microsite)
- `https://events.frappe.io/events/uae-e-invoice-integration` (a past webinar's 1-tab microsite)
- `https://events.frappe.io/dashboard/event-proposal`, `https://events.frappe.io/dashboard/book-tickets/frappeverse-mumbai-2026` (SPA app shells)
- `https://events.frappe.io/draft/meetups` (an orphaned earlier build, found via sitemap — see §3)
- `https://events.frappe.io/sitemap.xml`, `/robots.txt`
- Linked stylesheets: `/builder_assets/variables.css`, `/files/page_styles/builder-asset-style.css`, and the three `CSS-*.css` bundles referenced in `<head>`

**A CSS caveat, unlike the earlier two docs**: frappe.io's main marketing site and blog inline every Frappe Builder block's exact CSS declaration in a page-level `<style>` tag, which is what let those docs cite precise `px`/`rem` values straight from curl output. events.frappe.io does **not** do this — its `<style>` block is 9 lines of global resets, and none of the four linked stylesheets contain the per-element `.fb-<hash>{...}` rules either. Whatever mechanism actually styles this subdomain's pages is not present in the static HTML/CSS this method can reach (possibly runtime/client-injected). What *was* recoverable from the stylesheets: the font stack — **Inter** (variable, `opsz 14–32`, `wght 100–900`, plus italic), **Newsreader**, and **League Gothic** (a condensed display face not seen on the main site or blog, application point unconfirmed) — and the exact same near-monochrome grayscale token palette already documented in `frappe-io-design-patterns.md` (`#999999`, `#F8F8F8`, `#F3F3F3`, `#EDEDED`, `#E2E2E2`, `#C7C7C7`, `#7C7C7C`, `#525252`, `#383838`, `#171717`) — confirming one shared design system across frappe.io properties, just not independently pixel-verifiable here. Treat this doc as structure/content-anatomy-precise, not typography-precise; a live devtools pass would be needed for the latter.

---

## 1. Overall page structure

**Not a grid, and not a calendar-grid/month-view anywhere on the site.** It's a curated, magazine-style landing page: named sections by event type, each a horizontal row of image cards (conferences, local/meetups) or a plain vertical list (webinars) — never a uniform grid of all events, never a day/week/month calendar surface.

Three near-duplicate landing pages exist for the type filters — `/conferences`, `/local`, `/webinars` — each reusing the homepage shell (header, hero, filter-tab bar) but populated with only that type's sections. A fourth implied category, "Meetups," is in the nav but currently broken (§3). There is no unified "all events" list distinct from the homepage — the "All Events" tab literally links to `/` itself.

Homepage section order, top to bottom:
1. **Header**: SVG wordmark (3 stacked logo variants in the markup) + top nav — Awards, Code of Conduct, Propose Event, Dashboard, About, Get support
2. **Hero**: "Where the Frappeverse shows up" + a descriptive paragraph + one static hero image (no carousel observed)
3. **Filter-tab bar**: All Events / Conferences / Local / Meetups / Webinars — plain text tabs, each a full page link, not a client-side filter
4. **"Upcoming Yatra Meetups"** — carousel container, **empty in static HTML** (client-hydrated, could not inspect) + "View all"
5. **"Upcoming Conferences"** — a card row (1 card at fetch time: Frappeverse Mumbai 2026) + "View all" → `/conferences`
6. **"Recent Events"** — two labeled sub-rows: "Conferences" (3 cards) and "LOCAL / YATRA" (4 cards) — even the mixed homepage groups past events by sub-type
7. **"webinars"** — a genuine plain vertical list, not cards (5 rows on homepage, 17 on `/webinars`)
8. **"Local and Meetups"** — another empty client-hydrated carousel + "View all"
9. **"Explore categories"** — 6 icon pills → `/category/<slug>`: Zoom Meeting, Local, Webinars, Yatra, Conferences, Meetups
10. **CTA**: "Got something worth sharing?" → `mailto:events@frappe.io`
11. **Footer** — the same site-wide frappe.io footer (social icons; Home/Products/Partners/Certifications/Contact/Terms/Social links; the "To err is human, to forgive is design." — Andrew Dillon quote already logged in `frappe-io-blog-patterns.md`)

The meaningful structural decision here: **event type dictates layout template**, not a single shared list/grid component. In-person events (conferences, local/Yatra meetups) get image-card rows; webinars — no venue photo worth foregrounding — get a plain text list. Nothing on the site paginates or scrolls by date; ordering within each section is simply reverse-/forward-chronological.

Source: `https://events.frappe.io/`.

---

## 2. Event card/row anatomy

Two distinct templates, confirmed identical across all sampled instances of each:

### A. Conference / Local (Yatra) card — image-card row
| Element | Present? | Detail |
|---|---|---|
| Banner/cover image | Yes | Full card width, top |
| Title | Yes | `trunc` class — single-line ellipsis |
| Date | Yes | Calendar icon + `YYYY-MM-DD` (e.g. `2026-08-21`) on the **listing card** — a different format than the same event's own detail page, which shows `21 - 22 August, 2026` (§4) |
| Time | **No** | Not shown on any listing card, only on the detail page |
| Location | Yes | Pin icon + **venue name only** (e.g. "Nehru Centre Auditorium") — no city/street, no map, that detail is detail-page-only |
| Description/blurb | **No** | Absent on this card type (present on webinar rows, below) |
| Category chip/badge | **No** | Category is implied by which section the card sits in, never rendered on the card itself |
| Attendee count | **No** | Not shown anywhere on the site, listing or detail |
| RSVP/Register | **No** | Never on the card — only on the event's own detail page |

### B. Webinar row — plain list, no image
| Element | Present? | Detail |
|---|---|---|
| Image | No | None — webinars are implicitly virtual |
| Title | Yes | Bold, no truncation observed |
| Description/blurb | Yes | One line — the one card type that does show a description |
| Date | Yes | Calendar icon + `D Mon YYYY` (e.g. `27 Jul 2026`) — a **third** distinct date format from the card and detail-page formats above |
| Time | Yes | Clock icon + `H:MM AM/PM` + a timezone abbreviation when set (`2:00 PM GST`, `3:00 PM IST`, `4:30 PM WIB`) — several rows simply have a trailing space where the timezone should be (`3:00 PM `), an inconsistent-data-entry tell |
| Venue | No | Implicitly virtual |
| Category/attendee count/RSVP | No | Same absences as the card template |

**Data-quality finding**: several unrelated webinar rows share the *exact same* description string verbatim — "Dive into Frappe CRM and take control of your sales pipeline (Presented in Indonesian)" appears as the blurb for "UAE E-Invoice Integration," "POS for Retail and Restaurants on Frappe," and "Frappe Cloud Plans & Pricing" alike. Clearly a copy-paste content bug in their event CMS, not an intentional pattern — worth knowing so it isn't mistaken for a real "reused boilerplate blurb" design choice.

Sources: `https://events.frappe.io/`, `https://events.frappe.io/conferences`, `https://events.frappe.io/local`, `https://events.frappe.io/webinars`.

---

## 3. Filtering / navigation

- Top-level filtering is a **fixed 5-tab bar** (All Events / Conferences / Local / Meetups / Webinars) — full page navigations, not client-side toggles, no dropdown, no chips.
- **The "Meetups" tab is broken on the live site.** `https://events.frappe.io/meetups` returns a genuine Frappe 404 page, confirmed by direct fetch and consistent across every page's header nav (all link to the same dead `/meetups`). A working page does exist at `https://events.frappe.io/draft/meetups` (found via `sitemap.xml`, not linked from anywhere live), but it's an orphaned earlier iteration of the whole site — its own "Meetups" tab is a dead `href="#"`, and its "Conferences"/"Local" links point into a separate `/draft/*` tree, not the live one. Net effect: "Meetups" as a distinct top-level section does not currently work at all; city meetups instead live under "Local," branded "Yatra" (§5).
- **No search box** anywhere on any page inspected.
- **No pagination** anywhere — the longest list sampled (`/webinars`, 17 rows) is one flat unpaginated list in the static HTML; no "load more" or page-number controls found.
- **Category taxonomy URLs exist but are broken**: `/category/<slug>` is linked for 6 categories (zoom-meeting, local, webinars, yatra, conferences, meetups), but `https://events.frappe.io/category/local` returned an actual **HTTP 500 "Server Error,"** not just an empty state — a second broken navigation surface alongside the Meetups 404.
- **Upcoming vs. past is a curated, per-section split** ("Upcoming Conferences" vs. "Recent Events"/"Recent Conferences"), not a single date-toggled list. This is content-driven, not template-driven: `/webinars` at fetch time had zero upcoming entries and the page simply opened straight into "Recent Webinars" with no empty "Upcoming" placeholder shown — the upcoming section appears to collapse away entirely rather than render an empty state.
- Two carousels on the homepage ("Upcoming Yatra Meetups," "Local and Meetups") render as **empty `<div>`s in static HTML** — genuinely client-hydrated, could not be inspected further without a live JS pass (the same category of gap flagged for `/blog`'s `filter-area` div in the earlier blog research).

Source: `https://events.frappe.io/meetups`, `https://events.frappe.io/draft/meetups`, `https://events.frappe.io/category/local`, `https://events.frappe.io/sitemap.xml`.

---

## 4. Individual event detail page

All three event types share **one page template**, with tabs and sidebar content varying by what the event actually has:

- **Banner image** full-width at top (`.banner{border-radius:12px;padding:1px}` — the one pixel-level rule this method could confirm for this subdomain), with the event title, date/time, and — only if the event is upcoming — a **Register** button overlaid.
- **Sub-navigation tabs — a genuine multi-page microsite per event, not one scrolling page.** Tab count is content-driven:
  - Conference (Frappeverse Mumbai 2026): **About / Guidelines / Venue and Stay** (3 tabs)
  - Local/Yatra meetup (Coimbatore): **About / Schedule** (2 tabs)
  - Webinar (UAE E-Invoice Integration): **About** only (1 tab)
- **About tab**: rich text via **Quill** (`class="ql-editor read-mode"`) — a different editor than the `prose`/Tailwind-Typography class used on the frappe.io/blog article template documented earlier. Real formatted prose (headings, bullet/numbered lists, inline links out to `school.frappe.io/lms/batches/...` for paid pre-conference bootcamp registration).
- **Sidebar** (repeated as a second stacked block, presumably for mobile): **WHEN** (date/time + timezone), **WHERE** (a live embedded Google Maps `<iframe>` for physical venues, plus venue name + street address; the iframe is correctly omitted for the virtual webinar), **HOSTED BY** (host logo + name + tagline/country), **FEATURED SPEAKERS** (photo, name, role, company, plus a YouTube-icon link per speaker).
- **Registration mechanism**: the **Register** button appears **only on upcoming events** — present on Frappeverse Mumbai 2026 (Aug 2026, future at fetch time), absent on both past-event samples (Coimbatore Yatra, UAE webinar). It links to `/dashboard/book-tickets/<event-slug>`, which is not a static page but the same authenticated **"Buzz Dashboard"** SPA shell (`<title>Buzz Dashboard</title>`, a Vite-built JS bundle, site `frappe-events.m.frappe.cloud`, Frappe Framework `17.0.0-dev` exposed via `window.frappe_version`) that also serves `/dashboard/event-proposal` and sponsorship-enquiry forms. The Guidelines tab spells the flow out in prose: register → "you may have to sign up or log in to the Frappe Event Portal" → a ticket is generated automatically "showing a QR code and the days you'll be attending," downloadable later from the portal account.
- **No ICS / "Add to calendar" mechanism anywhere** — checked every page fetched (homepage, all three type-landing pages, all three event-detail samples) for `.ics`, "add to calendar," or Google/Outlook calendar-add links; none exist.
- **No RSS feed for events** — `/rss.xml` returns 404 (frappe.io/blog, by contrast, does ship one, per the earlier blog research).
- **Conference-only**: a **Sponsors** section, tiered (Gold/Silver logo rows, ~12 Gold + 3 Silver logos on the Mumbai sample) with a "Be a Sponsor" CTA into a sponsorship-enquiry form inside the same dashboard SPA. The smaller meetup has a single flat, untiered sponsor-logo row instead.
- **Meetup-only**: a **"Glimpses"** section — one representative photo plus a "View all photos" link out to an *external* Google Photos shared album. Full photo galleries live off-platform, not on events.frappe.io itself.
- **Schedule tab (meetup only)**: a `.schedule-item` CSS rule confirms a **vertical timeline** treatment — left-aligned connecting line + dot per item, collapsing to a flush list under the 576px breakpoint. A genuine agenda/timeline component, distinct from a calendar grid. Individual talks appear to have their own pages, per a `/talks/<event-route>/<talk-slug>` route found in `sitemap.xml` — not fetched/inspected further (gap).
- **Two real data-quality bugs found on this template**:
  1. On both past-event samples, the WHERE address line under the venue name is a **stale copy-paste of the Mumbai conference's street address** ("Dr Annie Besant Rd, Worli, Mumbai") regardless of the event's actual location — most visible on the UAE webinar, where the venue name correctly reads "UAE e-Invoicing: Zoom Online" but the address text underneath is the wrong hardcoded Mumbai string, with (correctly) no map iframe.
  2. **"FEATURED SPEAKERS" renders as a heading even when there are no speakers** — an empty content `<div>` sits under a still-visible label on both the Coimbatore and UAE-webinar pages, rather than the whole block being conditionally hidden.

Sources: `https://events.frappe.io/events/frappeverse-mumbai-2026` (+ `/guidelines`, `/venue-and-stay`), `https://events.frappe.io/events/frappe-yatra-coimbatore-2026`, `https://events.frappe.io/events/uae-e-invoice-integration`, `https://events.frappe.io/dashboard/event-proposal`.

---

## 5. Distinctly frappe.io-flavored details (not generic event-listing boilerplate)

- **The "Buzz Dashboard" SPA** — one shared, separately authenticated Frappe app handles every transactional flow (ticket booking with QR codes, event proposals, sponsorship enquiries) behind a single login, cleanly split from the plain server-rendered Builder pages that do the browsing/marketing. Two systems, one site.
- **"Frappe Yatra"** — the "Local" category isn't generic city meetups, it's a named touring roadshow ("a fast-moving series of local meet-ups across cities") with its own asset naming convention (`yatra-<city>-banner.png`) and a tight multi-city cadence (7 Indian cities in the sample — Coimbatore, Bengaluru, Pune, Delhi, Ahmedabad, Chennai, Hyderabad — all within about three weeks of each other, late May–mid June 2026). A deliberate roadshow format, not ad hoc community meetups.
- **Cross-sell into `school.frappe.io`** (Frappe's LMS product) for paid pre-conference bootcamps, linked directly from the conference's About copy — real product cross-promotion between frappe.io-family properties.
- **Same shared grayscale design-token palette** as the main marketing site (`#999999` … `#171717`, listed in §Method) — one design system across properties, confirmed even though this subdomain's per-block CSS couldn't be pixel-verified independently.
- **League Gothic** added to the font stack alongside Inter and Newsreader — not present on the main site or blog per the earlier research; its actual use in the rendered page wasn't identified (gap).
- The recurring **"To err is human, to forgive is design." — Andrew Dillon** footer quote (already logged in `frappe-io-blog-patterns.md`) reappears unchanged here, confirming it's a genuinely site-wide footer include across all of frappe.io's properties, not a blog-specific touch.

---

## 6. Public conference/meetup marketing site, not a general-purpose calendar

Read overwhelmingly as a **public-facing conference-and-meetup marketing/community-engagement site**, not a general-purpose scheduling tool, and structurally **not a calendar at all**:

- "Propose Event," sponsorship tiers with "Be a Sponsor" forms, ticket QR codes, a public Code of Conduct, sustainability guidelines for a physical venue, cross-sell into a paid LMS — all signal a high-production, externally-facing event program, not internal-only content. Everything sampled (about copy, guidelines, speaker bios, sponsor logos) is written for an external, unauthenticated community audience.
- There is **no day/week/month grid anywhere on the site**, no personal RSVP list, no "my events," no availability/scheduling logic. Structurally it's a **conference/meetup listing site that generates a rich microsite per event** — closer to a lightweight events-marketing CMS (think a stripped-down Eventbrite/Sessionize) than to any kind of calendar UI.

---

## Open gaps

1. Two client-hydrated empty carousels ("Upcoming Yatra Meetups" on the homepage, "Local and Meetups" further down) — content/interaction unconfirmed without a live JS pass.
2. Per-block pixel/typography CSS is not recoverable from this subdomain's static HTML (unlike the main site/blog) — flagged in Method; needs live devtools to pin down exact type scale/spacing.
3. Talk detail pages (`/talks/<event>/<talk>`) referenced in `sitemap.xml` but not fetched or inspected.
4. League Gothic's actual application point in the rendered page wasn't identified.
5. Several elements appear twice in the markup with identical text but different surrounding structure (e.g. "Upcoming Conferences" as both an eyebrow and a heading; the "Got something worth sharing?" CTA appearing twice, once with `href="#"` and once with `mailto:events@frappe.io`) — most likely the same desktop/mobile duplicate-block pattern seen explicitly elsewhere via `mobile-tabs`/`desktop-only` classes on the event-detail tab navs, but not confirmed against the actual (unrecoverable, per gap #2) CSS that shows/hides each copy.

---

## For DoWH

**The core tension this research surfaces**: DoWH's Calendar feature already has a locked design decision in [`new-pages.md`](../../design/new-pages.md) — a **month grid** (7-column CSS grid, gold-outline pill event chips) as the default view, with an unfleshed-out "toggle to list view." events.frappe.io, the exact site the user pointed at as "what I meant by Calendar," has **no month/week/day grid anywhere** — it's entirely card-rows and lists. If the intent is genuinely to model DoWH's Calendar on events.frappe.io's structure, that's a real re-opening of wayfinder ticket #27's decision toward a list/card event-hub, not an incremental addition to the existing month-grid design — worth naming explicitly in the wayfinder session rather than assumed away.

**What would translate well:**
- The **list-row vs. image-card split by event weight** (§1–2) — a lightweight virtual/all-hands briefing rendering as a plain list row (title, one-line description, date, time) versus a higher-production physical event (a wing town hall, an HR day, a training bootcamp) rendering as an image card — maps cleanly onto DoWH's own mix of quick internal notices vs. bigger staff events, and gives the still-undesigned "list view" toggle (per `new-pages.md`'s open item) a concrete anatomy to start from.
- The **multi-tab event-detail microsite pattern** (§4) — About / Schedule (skip Guidelines and Venue-and-Stay, which are public-event-specific) fits a DoWH training day or multi-session event well, and the `.schedule-item` **vertical-timeline agenda component** is a directly reusable pattern for a session-by-session day plan.
- The **WHEN / WHERE / HOSTED BY sidebar block** (§4) — genuinely reusable, with WHERE swapped from a public Google Maps embed to an internal building/room reference (DoWH is a single-campus staff portal, not a multi-city public tour), and HOSTED BY mapped to the sponsoring wing/directorate rather than a company logo.
- **Curated upcoming/past sectioning that collapses cleanly when empty** (§3) — a reasonable, low-complexity pattern for DoWH's likely lower event volume, and notably more graceful than what events.frappe.io ships for its *own* broken surfaces (see below).

**What clearly won't translate — public marketing-adjacent, no analog on a staff intranet:**
- **Ticketing with QR codes, sponsorship tiers, "Be a Sponsor" forms, external Google Photos galleries, a public Code of Conduct, sustainability/venue guidelines, and LMS cross-sell links** — all built for an unauthenticated public conference audience and irrelevant to an internal staff calendar, where "registration" (if needed at all) should be a simple RSVP against the existing ERPNext user, not a ticket-booking SPA.
- **The Meetups 404 and the Server-Error category pages (§3)** — genuine bugs on the source, not design choices; DoWH's already-decided wing-filter chip-bar pattern (per `new-pages.md`) is a more robust filtering approach than anything events.frappe.io currently ships working. Don't mistake frappe.io's broken filtering for a pattern worth reproducing.
- **No ICS/calendar-add, no RSS, no search, no pagination anywhere on events.frappe.io** (§3–4) — these read as gaps even on the source's own terms (a public marketing site can get away with manual curation over a small hand-picked list; a staff intranet calendar serving an entire department over time almost certainly needs at least calendar-add and search once event volume grows). Don't copy these absences as intentional restraint — they're closer to the source simply not needing them yet at its current scale.
