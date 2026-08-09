"""DoWH Circulars listing — /circulars

Detail view is inline (a <details> expand per row in the template, no
separate route) per docs/design/circulars.md — the old ?name= driven
detail page has been retired.

New-circular submission moved to the dedicated /circulars/new compose
page (see new.py) per docs/design/content-mgmt.md — this controller
no longer handles POST at all, just the listing.
"""

import frappe


def get_context(context):
    context.no_cache = 1
    context.show_sidebar = 0

    # Check if user is a content manager (controls whether the "+ New
    # circular" link to /circulars/new is shown)
    employee = frappe.db.get_value("Employee", {"user_id": frappe.session.user},
                                   ["name", "department", "designation", "content_manager"], as_dict=1)
    context.is_content_manager = bool(employee and employee.content_manager)
    context.user_department = employee.department if employee else None

    context.title = "Staff Circulars"

    wing_filter = frappe.form_dict.get("wing")
    class_filter = frappe.form_dict.get("classification")
    tag_filter = frappe.form_dict.get("tag")

    filters = {"published": 1}
    if wing_filter:
        filters["wing"] = wing_filter
    if class_filter:
        filters["classification"] = class_filter

    circulars = frappe.get_all(
        "Announcement",
        filters=filters,
        fields=["name", "title", "content", "date", "wing", "classification", "circular_number", "tags", "route", "attachment"],
        order_by="date desc",
        limit=50,
    )

    if tag_filter:
        circulars = [c for c in circulars if c.tags and tag_filter.lower() in (c.tags or "").lower()]

    context.circulars = circulars
    context.active_wing = wing_filter
    context.active_class = class_filter
    context.active_tags = [tag_filter] if tag_filter else []

    context.wings = frappe.get_all(
        "Department",
        filters={"company": "Department of Works and Highways", "is_group": 1},
        fields=["name", "department_name"],
    )

    all_announcements = frappe.get_all("Announcement", filters={"published": 1}, fields=["tags"])
    tag_set = set()
    for a in all_announcements:
        if a.tags:
            for t in a.tags.split(","):
                tag_set.add(t.strip().lower())
    context.all_tags = sorted(tag_set)

    context.stats = {
        "total": frappe.db.count("Announcement", {"published": 1}),
        "urgent": frappe.db.count("Announcement", {"published": 1, "classification": "Urgent"}),
        "action": frappe.db.count("Announcement", {"published": 1, "classification": "For Action"}),
    }

    return context
