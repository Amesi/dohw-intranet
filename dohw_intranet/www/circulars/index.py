"""DoWH Circulars listing + detail page — /circulars"""

import frappe


def get_context(context):
    context.no_cache = 1
    context.show_sidebar = 1

    # Detail view — specific circular by name
    circular_name = frappe.form_dict.get("name")
    context.debug_name = circular_name  # DEBUG
    if circular_name:
        context.circular = frappe.get_doc("Announcement", circular_name)
        context.title = context.circular.title
        return context

    # Listing view
    context.title = "Staff Circulars & Announcements"

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

    return context
