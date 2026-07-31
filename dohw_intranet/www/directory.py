"""DoWH Staff Directory — portal page using native Frappe patterns."""

import frappe


def get_context(context):
    context.no_cache = 1
    if frappe.session.user == "Guest":
        frappe.local.flags.redirect_location = "/login?redirect-to=/directory"
        raise frappe.Redirect

    context.show_sidebar = 1
    context.title = "Staff Directory"

    wing_filter = frappe.form_dict.get("wing")
    search = frappe.form_dict.get("search", "").strip()

    filters = {"status": "Active"}
    if wing_filter:
        filters["department"] = wing_filter

    employees = frappe.get_all(
        "Employee",
        filters=filters,
        fields=["employee_name", "designation", "department", "company_email", "cell_number", "image"],
        order_by="employee_name asc",
        limit=200,
    )

    # Client-side search filter
    if search:
        employees = [
            e
            for e in employees
            if search.lower() in (e.employee_name or "").lower()
            or search.lower() in (e.department or "").lower()
            or search.lower() in (e.designation or "").lower()
        ]

    context.employees = employees
    context.search = search
    context.active_wing = wing_filter

    # Wings for filter tabs
    context.wings = frappe.get_all(
        "Department",
        filters={"company": "Department of Works and Highways", "is_group": 1},
        fields=["name", "department_name"],
    )

    # Stats
    context.total_staff = frappe.db.count("Employee", {"status": "Active"})

    # Per-wing counts
    wing_counts = {}
    for w in context.wings:
        wing_counts[w.department_name] = frappe.db.count(
            "Employee", {"status": "Active", "department": w.name}
        )
    context.wing_counts = wing_counts

    return context
