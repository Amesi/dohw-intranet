"""DoWH Calendar — Day / Week / Month views with Wing filter."""

import frappe
from datetime import datetime, timedelta


def get_context(context):
    context.no_cache = 1
    if frappe.session.user == "Guest":
        frappe.local.flags.redirect_location = "/login?redirect-to=/calendar"
        raise frappe.Redirect

    context.show_sidebar = 0
    context.title = "Calendar"

    # Check if user is a content manager
    employee = frappe.db.get_value("Employee", {"user_id": frappe.session.user},
                                   ["name", "department", "content_manager"], as_dict=1)
    context.is_content_manager = bool(employee and employee.content_manager)
    context.user_department = employee.department if employee else None

    # Handle new event submission
    if frappe.form_dict.get("submit_event") and context.is_content_manager:
        event = frappe.get_doc({
            "doctype": "Event",
            "subject": frappe.form_dict.get("ev_subject"),
            "event_type": "Public",
            "event_category": frappe.form_dict.get("ev_category", "Event"),
            "starts_on": frappe.form_dict.get("ev_starts"),
            "ends_on": frappe.form_dict.get("ev_ends") or None,
            "location": frappe.form_dict.get("ev_location", ""),
            "description": frappe.form_dict.get("ev_description", ""),
            "wing": frappe.form_dict.get("ev_wing_override") or employee.department,
        })
        event.insert(ignore_permissions=True)
        context.posted = True

    view = frappe.form_dict.get("view", "month")
    wing_filter = frappe.form_dict.get("wing")
    year = int(frappe.form_dict.get("year") or datetime.now().year)
    month = int(frappe.form_dict.get("month") or datetime.now().month)
    day = int(frappe.form_dict.get("day") or datetime.now().day)

    context.view = view
    context.active_wing = wing_filter
    context.year = year
    context.month = month
    context.day = day
    context.month_name = datetime(year, month, 1).strftime("%B %Y")

    today = datetime.now()
    context.today_link = f"/calendar?view={view}&year={today.year}&month={today.month}&day={today.day}"
    if wing_filter:
        context.today_link += f"&wing={wing_filter}"

    if view == "month":
        _build_month(context, year, month, wing_filter)
    elif view == "week":
        _build_week(context, year, month, day, wing_filter)
    else:
        _build_day(context, year, month, day, wing_filter)

    context.wings = frappe.get_all(
        "Department",
        filters={"company": "Department of Works and Highways", "is_group": 1},
        fields=["name", "department_name"],
    )

    return context


def _build_month(context, year, month, wing_filter):
    first_day = datetime(year, month, 1)
    start_day = first_day.weekday()
    days_in_month = (datetime(year, month + 1, 1) - timedelta(days=1)).day if month < 12 else 31

    prev = datetime(year, month, 1) - timedelta(days=1)
    next_dt = datetime(year, month, 1) + timedelta(days=35)
    next_dt = next_dt.replace(day=1)
    qp = f"wing={wing_filter}&" if wing_filter else ""
    context.prev_link = f"/calendar?view=month&{qp}month={prev.month}&year={prev.year}"
    context.next_link = f"/calendar?view=month&{qp}month={next_dt.month}&year={next_dt.year}"

    month_start = datetime(year, month, 1).strftime("%Y-%m-%d")
    month_end = datetime(year, month + 1, 1).strftime("%Y-%m-%d") if month < 12 else f"{year+1}-01-01"
    events = _get_events(month_start, month_end, wing_filter)

    weeks = []
    d = 1
    for w in range(6):
        week = []
        for _ in range(7):
            if (w == 0 and len(week) < start_day) or d > days_in_month:
                week.append({"day": 0, "events": []})
            else:
                ds = f"{year}-{month:02d}-{d:02d}"
                week.append({"day": d, "events": [e for e in events if e.starts_on.strftime("%Y-%m-%d") == ds]})
                d += 1
        weeks.append(week)
        if d > days_in_month:
            break

    context.weeks = weeks
    context.upcoming = _get_upcoming(wing_filter)


def _build_week(context, year, month, day, wing_filter):
    target = datetime(year, month, day)
    monday = target - timedelta(days=target.weekday())

    prev = monday - timedelta(days=7)
    next_m = monday + timedelta(days=7)
    qp = f"wing={wing_filter}&" if wing_filter else ""
    context.prev_link = f"/calendar?view=week&{qp}year={prev.year}&month={prev.month}&day={prev.day}"
    context.next_link = f"/calendar?view=week&{qp}year={next_m.year}&month={next_m.month}&day={next_m.day}"

    week_start = monday.strftime("%Y-%m-%d")
    week_end = (monday + timedelta(days=6)).strftime("%Y-%m-%d")
    events = _get_events(week_start, week_end, wing_filter)

    week_days = []
    for i in range(7):
        dt = monday + timedelta(days=i)
        ds = dt.strftime("%Y-%m-%d")
        day_events = [e for e in events if e.starts_on.strftime("%Y-%m-%d") == ds]
        week_days.append({"date": dt, "label": dt.strftime("%a %d"), "events": day_events})

    context.week_days = week_days
    context.week_start = monday.strftime("%d %b")
    context.week_end = (monday + timedelta(days=6)).strftime("%d %b %Y")
    context.upcoming = _get_upcoming(wing_filter)


def _build_day(context, year, month, day, wing_filter):
    target = datetime(year, month, day)
    prev = target - timedelta(days=1)
    next_d = target + timedelta(days=1)
    qp = f"wing={wing_filter}&" if wing_filter else ""
    context.prev_link = f"/calendar?view=day&{qp}year={prev.year}&month={prev.month}&day={prev.day}"
    context.next_link = f"/calendar?view=day&{qp}year={next_d.year}&month={next_d.month}&day={next_d.day}"

    ds = target.strftime("%Y-%m-%d")
    events = _get_events(ds, ds, wing_filter)

    hours = []
    for h in range(7, 18):
        hour_events = [e for e in events if e.starts_on.hour == h]
        hours.append({"hour": h, "label": f"{h:02d}:00", "events": hour_events})

    context.hours = hours
    context.day_label = target.strftime("%A, %d %B %Y")
    context.upcoming = _get_upcoming(wing_filter)


def _get_events(start_date, end_date, wing_filter=None):
    filters = [
        ["starts_on", ">=", start_date],
        ["starts_on", "<=", end_date + " 23:59:59"],
        ["event_type", "=", "Public"],
    ]
    if wing_filter:
        filters.append(["wing", "=", wing_filter])
    return frappe.get_all(
        "Event",
        filters=filters,
        fields=["name", "subject", "starts_on", "ends_on", "event_category", "location", "description", "all_day"],
        order_by="starts_on asc",
        limit=100,
    )


def _get_upcoming(wing_filter=None):
    today_str = datetime.now().strftime("%Y-%m-%d")
    end_str = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
    filters = [
        ["starts_on", ">=", today_str],
        ["starts_on", "<=", end_str],
        ["event_type", "=", "Public"],
    ]
    if wing_filter:
        filters.append(["wing", "=", wing_filter])
    return frappe.get_all(
        "Event",
        filters=filters,
        fields=["name", "subject", "starts_on", "ends_on", "event_category", "location", "description", "all_day"],
        order_by="starts_on asc",
        limit=10,
    )
