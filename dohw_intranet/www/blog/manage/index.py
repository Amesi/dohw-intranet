"""DoWH Blog — compose & manage area — /blog/manage

Real build per docs/design/blog.md and issue #44's workflow: My Drafts /
Pending Review / Published, with Draft -> In Review -> Published state
transitions delegated to the Blog Post doctype's own whitelisted methods
(dohw_intranet/dohw_intranet/doctype/blog_post/blog_post.py) so the
reviewer-never-author guard lives in one place, not duplicated here.

Three views on one route via query params (?compose=new|<route>,
?review=<route>, or neither for the dashboard) — same POST-then-redirect
pattern as /circulars/new. Featured image upload isn't wired into the
compose form (out of scope for this pass — the field can still be set via
Desk); everything else in the data model is.
"""

import frappe

from dohw_intranet.sanitize import sanitize_rich_html

CATEGORIES = ["Project Updates", "Staff Spotlight", "Department News", "ICT & Systems"]


def get_context(context):
    context.no_cache = 1
    if frappe.session.user == "Guest":
        frappe.local.flags.redirect_location = "/login?redirect-to=/blog/manage"
        raise frappe.Redirect

    context.show_sidebar = 0

    employee = frappe.db.get_value(
        "Employee", {"user_id": frappe.session.user},
        ["name", "employee_name", "blog_author"], as_dict=1,
    )
    is_blog_author = bool(employee and employee.blog_author)
    if not is_blog_author:
        frappe.local.flags.redirect_location = "/blog"
        raise frappe.Redirect

    if frappe.request.method == "POST":
        _handle_post(employee.name)
        frappe.local.flags.redirect_location = "/blog/manage"
        raise frappe.Redirect

    compose = frappe.form_dict.get("compose")
    review = frappe.form_dict.get("review")

    if compose:
        context.title = "New Post" if compose == "new" else "Edit Draft"
        context.view = "compose"
        context.categories = CATEGORIES
        context.post = None
        if compose != "new":
            post = frappe.get_doc("Blog Post", {"route": compose})
            if post.author != employee.name or post.status != "Draft":
                frappe.local.flags.redirect_location = "/blog/manage"
                raise frappe.Redirect
            post.content = sanitize_rich_html(post.content or "")
            context.post = post
        return context

    if review:
        context.title = "Review Post"
        context.view = "review"
        post = frappe.get_doc("Blog Post", {"route": review})
        if post.status != "In Review" or post.author == employee.name:
            frappe.local.flags.redirect_location = "/blog/manage"
            raise frappe.Redirect
        post.content = sanitize_rich_html(post.content or "")
        context.post = post
        context.post_author_name = frappe.db.get_value("Employee", post.author, "employee_name")
        return context

    context.title = "Blog — Manage"
    context.view = "dashboard"
    context.drafts = frappe.get_all(
        "Blog Post", filters={"author": employee.name, "status": "Draft"},
        fields=["name", "title", "route", "modified"], order_by="modified desc",
    )
    context.pending_review = frappe.get_all(
        "Blog Post", filters={"status": "In Review", "author": ["!=", employee.name]},
        fields=["name", "title", "route", "author", "modified"], order_by="modified asc",
    )
    for p in context.pending_review:
        p.author_name = frappe.db.get_value("Employee", p.author, "employee_name")
    context.published = frappe.get_all(
        "Blog Post", filters={"author": employee.name, "status": "Published"},
        fields=["name", "title", "route", "published_date"], order_by="published_date desc",
    )
    return context


def _handle_post(employee_name):
    if frappe.form_dict.get("save_draft"):
        route = frappe.form_dict.get("post_route")
        if route:
            post = frappe.get_doc("Blog Post", {"route": route})
            if post.author != employee_name or post.status != "Draft":
                frappe.throw(frappe._("Not allowed"), frappe.PermissionError)
        else:
            post = frappe.get_doc({"doctype": "Blog Post", "author": employee_name})

        post.title = frappe.form_dict.get("post_title")
        post.category = frappe.form_dict.get("post_category")
        post.excerpt = frappe.form_dict.get("post_excerpt")
        post.content = sanitize_rich_html(frappe.form_dict.get("post_content") or "")
        if route:
            post.save(ignore_permissions=True)
        else:
            post.insert(ignore_permissions=True)

        if frappe.form_dict.get("submit_after_save"):
            post.submit_for_review()
        return

    if frappe.form_dict.get("do_submit_for_review"):
        post = frappe.get_doc("Blog Post", {"route": frappe.form_dict.get("post_route")})
        if post.author != employee_name:
            frappe.throw(frappe._("Not allowed"), frappe.PermissionError)
        post.submit_for_review()
        return

    if frappe.form_dict.get("do_approve"):
        post = frappe.get_doc("Blog Post", {"route": frappe.form_dict.get("post_route")})
        post.approve()
        return

    if frappe.form_dict.get("do_reject"):
        post = frappe.get_doc("Blog Post", {"route": frappe.form_dict.get("post_route")})
        post.reject(frappe.form_dict.get("reject_reason"))
        return
