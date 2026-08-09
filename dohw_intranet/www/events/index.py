"""DoWH Events listing — /events

Real build per docs/design/events.md (Variant B, uniform card grid).
No new doctype — reads the existing Event doctype, filtered to
event_category="Event" (Calendar's own composer already writes these;
this section is purely an additional, richer presentation of the same
data, per #52's decision — Calendar's grid is untouched).
"""

import frappe


def get_context(context):
    context.no_cache = 1
    context.show_sidebar = 0

    if frappe.session.user == "Guest":
        frappe.local.flags.redirect_location = "/login?redirect-to=/events"
        raise frappe.Redirect

    context.title = "Events"

    events = frappe.get_all(
        "Event",
        filters={"event_category": "Event"},
        fields=["name", "subject", "description", "starts_on", "location", "wing"],
        order_by="starts_on asc",
    )

    wing_names = frappe.get_all(
        "Department",
        filters={"name": ["in", [e.wing for e in events if e.wing]] or [""]},
        fields=["name", "department_name"],
    )
    wing_map = {w.name: w.department_name for w in wing_names}
    for e in events:
        e.host = wing_map.get(e.wing, e.wing) if e.wing else "Department of Works and Highways"
        e.excerpt = (e.description or "")[:140]

    context.events = events
    return context
