"""DoWH Projects — prototype with All/Wing/Team view toggles."""

import frappe
from datetime import datetime


def get_context(context):
    context.no_cache = 1
    if frappe.session.user == "Guest":
        frappe.local.flags.redirect_location = "/login?redirect-to=/prototypes/projects"
        raise frappe.Redirect

    context.show_sidebar = 0
    context.title = "Projects"

    view = frappe.form_dict.get("view", "wing")  # all, wing, team
    wing_filter = frappe.form_dict.get("wing")
    context.view = view
    context.active_wing = wing_filter

    filters = {}
    if view == "wing":
        # Get user's department (wing)
        employee = frappe.db.get_value("Employee", {"user_id": frappe.session.user}, "department")
        if employee:
            filters["department"] = employee
    elif view == "team":
        # Projects where user is in the users table
        # Fallback: show projects in user's department
        employee = frappe.db.get_value("Employee", {"user_id": frappe.session.user}, "department")
        if employee:
            filters["department"] = employee

    if wing_filter:
        filters["department"] = wing_filter

    projects = frappe.get_all(
        "Project",
        filters=filters,
        fields=["name", "project_name", "status", "priority", "department",
                "percent_complete", "expected_start_date", "expected_end_date",
                "estimated_costing", "company"],
        order_by="priority desc, expected_start_date asc",
        limit=50,
    )

    # Enrich with wing name and progress color
    for p in projects:
        p.progress_color = (
            "green" if (p.percent_complete or 0) >= 75
            else "gold" if (p.percent_complete or 0) >= 50
            else "orange" if (p.percent_complete or 0) >= 25
            else "grey"
        )

    context.projects = projects

    # Wings for filter
    context.wings = frappe.get_all(
        "Department",
        filters={"company": "Department of Works and Highways", "is_group": 1},
        fields=["name", "department_name"],
    )

    context.stats = {
        "total": len(projects),
        "open": sum(1 for p in projects if p.status == "Open"),
        "completed": sum(1 for p in projects if p.status == "Completed"),
    }

    return context
