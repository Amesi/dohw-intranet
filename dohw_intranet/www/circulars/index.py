"""DoWH Circulars listing — /circulars

Detail view is inline (a <details> expand per row in the template, no
separate route) per docs/design/circulars.md — the old ?name= driven
detail page has been retired.

New-circular submission moved to the dedicated /circulars/new compose
page (see new.py) per docs/design/content-mgmt.md — this controller
no longer handles POST at all, just the listing.
"""

import frappe

from dohw_intranet.sanitize import sanitize_rich_html


def get_context(context):
    context.no_cache = 1
    context.show_sidebar = 0

    if frappe.session.user == "Guest":
        frappe.local.flags.redirect_location = "/login?redirect-to=/circulars"
        raise frappe.Redirect

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

    # Sanitize on read — legacy circulars were authored via a bare
    # contenteditable, so their HTML hasn't been through the new editor's
    # save-time sanitizer.
    for c in circulars:
        c.content = sanitize_rich_html(c.content or "")

    context.circulars = circulars
    context.active_wing = wing_filter
    context.active_class = class_filter
    context.active_tags = [tag_filter] if tag_filter else []

    context.wings = frappe.get_all(
        "Department",
        filters={"company": "Department of Works and Highways", "is_group": 1},
        fields=["name", "department_name"],
    )

    context.stats = {
        "total": frappe.db.count("Announcement", {"published": 1}),
        "urgent": frappe.db.count("Announcement", {"published": 1, "classification": "Urgent"}),
        "action": frappe.db.count("Announcement", {"published": 1, "classification": "For Action"}),
    }

    return context
