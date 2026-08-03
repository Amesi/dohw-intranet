"""DoWH Links & Forms Hub."""

import frappe


def get_context(context):
    context.no_cache = 1
    if frappe.session.user == "Guest":
        frappe.local.flags.redirect_location = "/login?redirect-to=/links"
        raise frappe.Redirect

    context.show_sidebar = 0
    context.title = "Links & Forms"

    wing_filter = frappe.form_dict.get("wing")
    cat_filter = frappe.form_dict.get("category")
    context.active_wing = wing_filter
    context.active_category = cat_filter

    filters = {"published": 1}
    if wing_filter:
        filters["wing"] = wing_filter
    if cat_filter:
        filters["category"] = cat_filter

    links = frappe.get_all(
        "Useful Link",
        filters=filters,
        fields=["title", "url", "category", "wing", "description"],
        order_by="category, title",
        limit=100,
    )

    # Group by category
    categories = {}
    for l in links:
        categories.setdefault(l.category, []).append(l)
    context.categories = categories

    # Wings and categories for filters
    context.wings = frappe.get_all(
        "Department",
        filters={"company": "Department of Works and Highways", "is_group": 1},
        fields=["name", "department_name"],
    )

    context.link_categories = sorted(set(l.category for l in links))

    return context
