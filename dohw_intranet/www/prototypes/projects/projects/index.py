"""DoWH Projects — prototype with All/Wing/Team view toggles + detail drill-down."""

import frappe
from datetime import datetime


def get_context(context):
    context.no_cache = 1
    if frappe.session.user == "Guest":
        frappe.local.flags.redirect_location = "/login?redirect-to=/prototypes/projects"
        raise frappe.Redirect

    context.show_sidebar = 0
    context.title = "Projects"

    # Detail view
    proj_name = frappe.form_dict.get("proj")
    context.debug = str(proj_name)
    if proj_name:
        try:
            proj = frappe.get_doc("Project", proj_name)
            context.detail = {
                "name": proj.name,
                "project_name": proj.project_name,
                "status": proj.status,
                "priority": proj.priority,
                "department": proj.department,
                "percent_complete": proj.percent_complete or 0,
                "expected_start_date": proj.expected_start_date,
                "expected_end_date": proj.expected_end_date,
                "actual_start_date": proj.actual_start_date,
                "actual_end_date": proj.actual_end_date,
                "estimated_costing": proj.estimated_costing,
                "total_costing_amount": proj.total_costing_amount,
                "notes": proj.notes or "",
                "users": [{"user": u.user, "full_name": u.full_name} for u in (proj.users or [])],
            }
            context.detail["tasks"] = frappe.get_all(
                "Task",
                filters={"project": proj_name},
                fields=["subject", "status", "priority", "exp_start_date", "exp_end_date", "progress"],
                order_by="status asc, exp_start_date asc",
                limit=50,
            )
        except Exception as e:
            context.detail_error = str(e)
        return context

    view = frappe.form_dict.get("view", "wing")  # all, wing, team
    wing_filter = frappe.form_dict.get("wing")
    context.view = view
    context.active_wing = wing_filter

    filters = {}
    if view == "wing":
        employee = frappe.db.get_value("Employee", {"user_id": frappe.session.user}, "department")
        if employee:
            filters["department"] = employee
        # If no employee link, show all (admin/testing)
    elif view == "team":
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
