"""DoWH Issues portal — submit and track support requests."""

import frappe


def get_context(context):
    context.no_cache = 1
    if frappe.session.user == "Guest":
        frappe.local.flags.redirect_location = "/login?redirect-to=/support"
        raise frappe.Redirect

    context.show_sidebar = 0
    context.title = "Support Issues"

    # Handle form submission
    if frappe.form_dict.get("submit"):
        _create_issue(frappe.form_dict)
        context.submitted = True

    # Get user's issues
    context.issues = frappe.get_all(
        "Issue",
        filters={"raised_by": frappe.session.user},
        fields=["name", "subject", "status", "priority", "creation", "description"],
        order_by="creation desc",
        limit=50,
    )

    return context


def _create_issue(form):
    issue = frappe.get_doc({
        "doctype": "Issue",
        "subject": form.get("subject"),
        "description": form.get("description"),
        "raised_by": frappe.session.user,
        "priority": form.get("priority", "Medium"),
        "issue_type": form.get("issue_type", "Support"),
    })
    issue.insert(ignore_permissions=True)
