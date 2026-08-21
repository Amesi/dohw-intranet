"""DoWH Dashboard — key metrics and charts."""

import datetime

import frappe


def get_context(context):
    context.no_cache = 1
    if frappe.session.user == "Guest":
        frappe.local.flags.redirect_location = "/login?redirect-to=/dashboard"
        raise frappe.Redirect

    context.show_sidebar = 0
    context.title = "Dashboard"

    # Greeting
    fullname = frappe.db.get_value("User", frappe.session.user, "full_name") or ""
    context.first_name = fullname.split(" ")[0] if fullname else ""
    context.today_long = datetime.date.today().strftime("%A, %d %B %Y")

    # Circular stats
    context.circular_total = frappe.db.count("Announcement", {"published": 1})
    context.circular_urgent = frappe.db.count("Announcement", {"published": 1, "classification": "Urgent"})
    context.circular_action = frappe.db.count("Announcement", {"published": 1, "classification": "For Action"})

    # Circulars by wing
    wings = frappe.get_all("Department", filters={"company": "Department of Works and Highways", "is_group": 1}, fields=["name", "department_name"])
    wing_stats = []
    for w in wings:
        count = frappe.db.count("Announcement", {"published": 1, "wing": w.name})
        wing_stats.append({"name": w.department_name, "count": count})
    context.wing_circulars = sorted(wing_stats, key=lambda x: x["count"], reverse=True)

    # Staff stats
    context.staff_total = frappe.db.count("Employee", {"status": "Active"})
    wing_staff = []
    for w in wings:
        count = frappe.db.count("Employee", {"status": "Active", "department": w.name})
        wing_staff.append({"name": w.department_name, "count": count})
    context.wing_staff = sorted(wing_staff, key=lambda x: x["count"], reverse=True)

    # Issue stats
    context.issues_open = frappe.db.count("Issue", {"status": "Open"})
    context.issues_total = frappe.db.count("Issue")

    # Recent circulars
    context.recent = frappe.get_all(
        "Announcement",
        filters={"published": 1},
        fields=["title", "date", "wing", "classification", "circular_number", "route"],
        order_by="date desc",
        limit=6,
    )

    return context
