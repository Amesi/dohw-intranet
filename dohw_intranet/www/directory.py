"""DoWH Staff Directory — with search, photos, org chart, and Wing/Division/Branch/Section filters."""

import frappe


def get_context(context):
    context.no_cache = 1
    if frappe.session.user == "Guest":
        frappe.local.flags.redirect_location = "/login?redirect-to=/directory"
        raise frappe.Redirect

    context.show_sidebar = 1
    context.title = "Staff Directory"

    # Filters
    wing = frappe.form_dict.get("wing")
    division = frappe.form_dict.get("division")
    branch = frappe.form_dict.get("branch")
    section = frappe.form_dict.get("section")
    search = frappe.form_dict.get("search", "").strip()

    # Build department filter — use the most specific level selected
    dept_filter = section or division or wing

    filters = {"status": "Active"}
    if dept_filter:
        filters["department"] = dept_filter
    if branch:
        filters["branch"] = branch

    # Server-side search
    or_filters = None
    if search:
        or_filters = [
            ["employee_name", "like", f"%{search}%"],
            ["department", "like", f"%{search}%"],
            ["designation", "like", f"%{search}%"],
        ]

    employees = frappe.get_all(
        "Employee",
        filters=filters,
        or_filters=or_filters,
        fields=[
            "name", "employee_name", "designation", "department", "branch",
            "company_email", "cell_number", "image",
        ],
        order_by="employee_name asc",
        limit=200,
    )

    context.employees = employees
    context.search = search
    context.active_wing = wing
    context.active_division = division
    context.active_branch = branch
    context.active_section = section

    # Wings (top-level departments)
    context.wings = frappe.get_all(
        "Department",
        filters={"company": "Department of Works and Highways", "is_group": 1},
        fields=["name", "department_name"],
        order_by="department_name",
    )

    # Divisions for selected wing
    context.divisions = []
    if wing:
        context.divisions = frappe.get_all(
            "Department",
            filters={"parent_department": wing},
            fields=["name", "department_name"],
            order_by="department_name",
        )

    # Sections for selected division
    context.sections = []
    if division:
        context.sections = frappe.get_all(
            "Department",
            filters={"parent_department": division},
            fields=["name", "department_name"],
            order_by="department_name",
        )

    # Branches (from Branch doctype)
    context.branches = frappe.get_all(
        "Branch", fields=["name"], order_by="name", limit=100
    )

    # Stats
    context.total_staff = frappe.db.count("Employee", {"status": "Active"})
    wing_counts = {}
    for w in context.wings:
        wing_counts[w.department_name] = frappe.db.count(
            "Employee", {"status": "Active", "department": w.name}
        )
    context.wing_counts = wing_counts

    # Org chart (only when not filtering/searching)
    if not any([wing, division, branch, section, search]):
        context.org_chart = _build_org_chart()

    return context


def _build_org_chart():
    departments = frappe.get_all(
        "Department",
        filters={"company": "Department of Works and Highways"},
        fields=["name", "department_name", "parent_department"],
        order_by="lft asc",
    )
    heads = {}
    dept_heads = frappe.get_all(
        "Employee",
        filters={"status": "Active", "designation": ("like", "%Director%")},
        fields=["employee_name", "department", "designation", "image"],
    )
    for h in dept_heads:
        if h.department:
            heads[h.department] = h

    dept_map = {d.name: d for d in departments}
    chart = []
    for d in departments:
        if not d.parent_department:
            node = {
                "name": d.department_name,
                "head": heads.get(d.name),
                "children": _get_children(d.name, dept_map, heads),
            }
            chart.append(node)
    return chart


def _get_children(parent_name, dept_map, heads):
    children = []
    for name, dept in dept_map.items():
        if dept.parent_department == parent_name:
            node = {
                "name": dept.department_name,
                "head": heads.get(name),
                "children": _get_children(name, dept_map, heads),
            }
            children.append(node)
    return children
