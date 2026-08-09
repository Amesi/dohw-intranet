# Events — internal events section, modeled on events.frappe.io

Decision record for the [Events map](https://github.com/Amesi/dohw-intranet/issues/50): [data model (#52)](https://github.com/Amesi/dohw-intranet/issues/52), [events.frappe.io research (#51)](https://github.com/Amesi/dohw-intranet/issues/51), [listing & detail layout (#53)](https://github.com/Amesi/dohw-intranet/issues/53). Resolves as **Variant B — "Uniform card grid,"** chosen from the [three-variant prototype](https://github.com/Amesi/dohw-intranet/tree/prototype/events-layout).

Staff-only, login-gated — inherited from Calendar, which this section sits alongside without touching. Builds on the token system ([tokens.md](./tokens.md)) and the navigation shell ([navigation.md](./navigation.md)).

## Relationship to Calendar

**No new doctype, no schema changes.** Events is a second, richer presentation over the *same* ERPNext `Event` data Calendar already uses — filtered to `event_category = "Event"` (a value already in real use, alongside "Meeting"). Calendar's own Day/Week/Month grid is completely untouched and keeps showing everything, Meetings and Events alike — this section doesn't remove anything from Calendar, it adds a second way to browse the bigger-happenings subset.

Authoring uses the same `content_manager` gate Calendar's composer already has — no new permission system.

## RSVP

Uses core ERPNext's `Event Participants` child table as-is — no new doctype. `attending` is a stock Select field; DoWH uses all three values it ships with (**Yes / No / Maybe**), not a collapsed binary. Identity resolves via `Employee` (`reference_doctype = "Employee"`), matching every other identity check already built across this portal (`content_manager`, `blog_author`, wing scoping) — not `User` or `Contact`, ERPNext's more common default for this field elsewhere.

**Attendee list is public** — any staff member can see who else is going, with their RSVP status. **No capacity cap.**

## Layout — Variant B, "Uniform card grid"

- **Listing**: a 2-column card grid, every event gets the same treatment — image if it has a `featured_image`-equivalent, an empty placeholder if not. No split by event "weight" (frappe.io's own image-card-vs-list-row distinction was considered and dropped — see below). Each card: image/placeholder, title, a calendar-icon date/time line, a pin-icon venue line.
- **Detail page**: single page (no multi-tab microsite — events.frappe.io's About/Schedule/Guidelines/Venue-and-Stay tabs don't translate at DoWH's scale). Title, full description, a **Your RSVP** block (Yes/No/Maybe buttons), a **Who's going** section (avatar + name + status badge per attendee, matching the public-list decision above), and a **WHEN / WHERE / HOSTED BY** sidebar — WHERE is a plain venue-name line (no embedded map; DoWH is single-campus, not multi-city), HOSTED BY names the sponsoring Wing/directorate rather than a company logo.
- **Nav placement**: new "Events" sidebar item, immediately after Calendar.

## What was rejected and why

- **A — Split by weight** (image-card row for events with a photo, plain list row for events without) — dropped. This is events.frappe.io's actual literal pattern (event *type* — conference vs. webinar — determines the template), but DoWH doesn't have that type distinction, and inferring "weight" from "does it happen to have a photo uploaded" is a fragile, content-dependent split rather than a real structural one. A uniform grid is more predictable and easier for content managers to reason about.
- **C — Uniform list** (no images shown anywhere on the listing) — dropped. Loses the visual identity events.frappe.io itself uses to make department happenings feel like *events* rather than notices; Circulars and Blog already own the "restrained text list" register, and Events benefits from being visually distinct from both.

## What this doesn't cover (deliberately out of scope)

- **Multi-tab event microsite** (About/Schedule/Guidelines/Venue-and-Stay) — events.frappe.io's own pattern, not adopted; DoWH's events don't need per-event sub-pages at this scale. The `.schedule-item` vertical-timeline agenda component from the research is noted as a *reusable pattern* if a future multi-session training day ever needs one, but nothing is built for it now.
- **Ticketing/QR codes, sponsorship tiers, external photo galleries, public Code of Conduct/venue guidelines, LMS cross-sell** — all public-conference-specific per the research, no analog for an internal staff calendar.
- **ICS/"add to calendar," RSS, search, pagination** — none of these exist on events.frappe.io either (confirmed gaps on the source, not deliberate restraint); not ruled in or out here, just not decided — a future ticket's call if event volume grows enough to need them.

## Source

Full three-variant prototype preserved on branch [`prototype/events-layout`](https://github.com/Amesi/dohw-intranet/tree/prototype/events-layout), not merged to main.
