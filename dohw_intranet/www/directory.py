import frappe

def get_context(context):
    if frappe.session.user == "Guest":
        frappe.local.flags.redirect_location = "/login?redirect-to=/directory"
        raise frappe.Redirect

    context.no_cache = 1
    context.base_template = "dohw_intranet/templates/dohw_base.html"
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
        limit=200
    )

    # Search filter (client-side)
    if search:
        employees = [e for e in employees if search.lower() in (e.employee_name or "").lower() 
                     or search.lower() in (e.department or "").lower()
                     or search.lower() in (e.designation or "").lower()]

    context.employees = employees
    context.search = search
    context.active_wing = wing_filter

    # Wings for filter tabs
    context.wings = frappe.get_all(
        "Department",
        filters={"company": "Department of Works and Highways", "is_group": 1},
        fields=["name", "department_name"]
    )

    # Stats
    context.total_staff = len(frappe.get_all("Employee", filters={"status": "Active"}))
    
    # Per-wing counts
    wing_counts = {}
    for w in context.wings:
        count = len(frappe.get_all("Employee", filters={"status": "Active", "department": w.name}))
        wing_counts[w.department_name] = count
    context.wing_counts = wing_counts

    return context
