import frappe

def get_context(context):
    if frappe.session.user == "Guest":
        frappe.local.flags.redirect_location = "/login?redirect-to=/announcements"
        raise frappe.Redirect

    context.no_cache = 1
    context.show_sidebar = 0
    context.title = "Announcements"

    # Active filters from URL
    wing_filter = frappe.form_dict.get("wing")
    class_filter = frappe.form_dict.get("classification")

    filters = {"published": 1}
    if wing_filter:
        filters["wing"] = wing_filter
    if class_filter:
        filters["classification"] = class_filter

    context.announcements = frappe.get_all(
        "Announcement",
        filters=filters,
        fields=["name", "title", "content", "date", "wing", "classification", "circular_number", "route"],
        order_by="date desc",
        limit=50,
    )

    context.active_wing = wing_filter
    context.active_class = class_filter

    # Wings for filter dropdown
    context.wings = frappe.get_all(
        "Department",
        filters={"company": "Department of Works and Highways", "is_group": 1},
        fields=["name", "department_name"],
    )

    context.stats = {
        "total": frappe.db.count("Announcement", {"published": 1}),
        "urgent": frappe.db.count("Announcement", {"published": 1, "classification": "Urgent"}),
        "for_action": frappe.db.count("Announcement", {"published": 1, "classification": "For Action"}),
    }

    # Action required — For Action circulars from the last 30 days
    from datetime import datetime, timedelta
    cutoff = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
    context.deadlines = frappe.get_all(
        "Announcement",
        filters={"published": 1, "classification": "For Action", "date": [">=", cutoff]},
        fields=["title", "date", "circular_number"],
        order_by="date desc",
        limit=5,
    )

    # Recent Wiki documents (if wiki is installed)
    try:
        context.recent_docs = frappe.get_all(
            "Wiki Page",
            filters={"published": 1},
            fields=["title", "route", "modified"],
            order_by="modified desc",
            limit=5,
        )
    except Exception:
        context.recent_docs = []

    return context
