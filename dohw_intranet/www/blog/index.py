"""DoWH Blog listing — /blog

Real build per docs/design/blog.md (Variant A, "Reading List"): dense
single-column list, no featured-post treatment, plain-text
"In {Category} by {Author} · {Date}" meta line.
"""

import frappe


def get_context(context):
    context.no_cache = 1
    context.show_sidebar = 0

    if frappe.session.user == "Guest":
        frappe.local.flags.redirect_location = "/login?redirect-to=/blog"
        raise frappe.Redirect

    context.title = "Blog"

    category_filter = frappe.form_dict.get("category")
    filters = {"status": "Published"}
    if category_filter:
        filters["category"] = category_filter

    posts = frappe.get_all(
        "Blog Post",
        filters=filters,
        fields=["name", "title", "route", "excerpt", "category", "author", "published_date", "featured_image"],
        order_by="published_date desc",
    )

    author_names = frappe.get_all(
        "Employee",
        filters={"name": ["in", [p.author for p in posts]] or [""]},
        fields=["name", "employee_name"],
    )
    author_map = {a.name: a.employee_name for a in author_names}
    for p in posts:
        p.author_name = author_map.get(p.author, p.author)

    context.posts = posts
    context.active_category = category_filter
    context.categories = ["Project Updates", "Staff Spotlight", "Department News", "ICT & Systems"]

    return context
