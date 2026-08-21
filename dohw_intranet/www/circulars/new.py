"""DoWH Circulars — New compose page — /circulars/new

Dedicated compose route per docs/design/content-mgmt.md (Variant B),
replacing the inline composer that used to live directly on /circulars.
Only content managers can reach this page. Wing auto-scoping matches
the same pattern already used by Calendar's "New Event" composer.
"""

import frappe

from dohw_intranet.sanitize import sanitize_rich_html


def get_context(context):
    context.no_cache = 1
    if frappe.session.user == "Guest":
        frappe.local.flags.redirect_location = "/login?redirect-to=/circulars/new"
        raise frappe.Redirect

    context.show_sidebar = 0
    context.title = "New Circular"

    employee = frappe.db.get_value(
        "Employee", {"user_id": frappe.session.user},
        ["name", "department", "content_manager"], as_dict=1,
    )
    is_content_manager = bool(employee and employee.content_manager)
    if not is_content_manager:
        frappe.local.flags.redirect_location = "/circulars"
        raise frappe.Redirect

    context.wing_label = (
        frappe.db.get_value("Department", employee.department, "department_name")
        if employee.department else None
    )

    if frappe.form_dict.get("submit_circular"):
        wing = frappe.form_dict.get("wing_override") or employee.department
        circular = frappe.get_doc({
            "doctype": "Announcement",
            "title": frappe.form_dict.get("new_title"),
            "content": sanitize_rich_html(frappe.form_dict.get("new_content") or ""),
            "wing": wing,
            "classification": frappe.form_dict.get("new_classification", "For Information"),
            "tags": frappe.form_dict.get("new_tags", ""),
            "published": 1,
            "date": frappe.utils.nowdate(),
        })
        circular.insert(ignore_permissions=True)
        frappe.local.flags.redirect_location = "/circulars"
        raise frappe.Redirect

    return context
