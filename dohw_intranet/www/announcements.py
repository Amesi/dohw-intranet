import frappe

def get_context(context):
    if frappe.session.user == "Guest":
        frappe.local.flags.redirect_location = "/login?redirect-to=/announcements"
        raise frappe.Redirect

    context.no_cache = 1
    context.base_template = "dohw_intranet/templates/dohw_base.html"
    context.title = "Staff Circulars &amp; Announcements"

    # Active filters from URL
    wing_filter = frappe.form_dict.get("wing")
    class_filter = frappe.form_dict.get("classification")
    tag_filter = frappe.form_dict.get("tag")

    filters = {"published": 1}
    if wing_filter:
        filters["wing"] = wing_filter
    if class_filter:
        filters["classification"] = class_filter

    context.announcements = frappe.get_all(
        "Announcement",
        filters=filters,
        fields=["title", "content", "date", "wing", "priority", "classification", "circular_number", "tags"],
        order_by="date desc",
        limit=50
    )

    # Tag filtering (client-side filter for comma-separated tags)
    if tag_filter:
        filtered = []
        for a in context.announcements:
            if a.tags and tag_filter.lower() in (a.tags or "").lower():
                filtered.append(a)
        context.announcements = filtered

    context.active_wing = wing_filter
    context.active_class = class_filter
    context.active_tag = tag_filter

    # Wings for filter dropdown
    context.wings = frappe.get_all(
        "Department",
        filters={"company": "Department of Works and Highways", "is_group": 1},
        fields=["name", "department_name"]
    )

    # All unique tags for tag cloud
    all_announcements = frappe.get_all("Announcement", filters={"published": 1}, fields=["tags"])
    tag_set = set()
    for a in all_announcements:
        if a.tags:
            for t in a.tags.split(","):
                tag_set.add(t.strip().lower())
    context.all_tags = sorted(tag_set)

    # Quick Stats
    context.stats = {
        "total": len(frappe.get_all("Announcement", filters={"published": 1})),
        "urgent": len(frappe.get_all("Announcement", filters={"published": 1, "classification": "Urgent"})),
        "for_action": len(frappe.get_all("Announcement", filters={"published": 1, "classification": "For Action"})),
    }

    # Upcoming Deadlines (For Action circulars from last 30 days)
    from datetime import datetime, timedelta
    cutoff = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
    context.deadlines = frappe.get_all(
        "Announcement",
        filters={"published": 1, "classification": "For Action", "date": [">=", cutoff]},
        fields=["title", "date", "circular_number"],
        order_by="date desc",
        limit=5
    )

    # Recent Wiki Documents (from Wiki Page doctype if wiki is installed)
    try:
        context.recent_docs = frappe.get_all(
            "Wiki Page",
            filters={"published": 1},
            fields=["title", "route", "modified"],
            order_by="modified desc",
            limit=5
        )
    except Exception:
        context.recent_docs = []

    return context
