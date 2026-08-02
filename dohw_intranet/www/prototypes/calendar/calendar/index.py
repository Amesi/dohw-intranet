"""DoWH Calendar — prototype."""

import frappe
from datetime import datetime, timedelta


def get_context(context):
    context.no_cache = 1
    if frappe.session.user == "Guest":
        frappe.local.flags.redirect_location = "/login?redirect-to=/prototypes/calendar"
        raise frappe.Redirect

    context.show_sidebar = 0
    context.title = "Calendar"

    # Month/year from query params, default to current
    year = int(frappe.form_dict.get("year") or datetime.now().year)
    month = int(frappe.form_dict.get("month") or datetime.now().month)

    context.year = year
    context.month = month
    context.month_name = datetime(year, month, 1).strftime("%B %Y")

    # Navigation
    prev = datetime(year, month, 1) - timedelta(days=1)
    next_dt = datetime(year, month, 1) + timedelta(days=32)
    next_dt = next_dt.replace(day=1)
    context.prev_month = f"/prototypes/calendar?month={prev.month}&year={prev.year}"
    context.next_month = f"/prototypes/calendar?month={next_dt.month}&year={next_dt.year}"

    # Build month grid
    first_day = datetime(year, month, 1)
    start_day = first_day.weekday()  # 0=Monday
    days_in_month = (datetime(year, month + 1, 1) - timedelta(days=1)).day if month < 12 else 31

    # Fetch events for this month
    month_start = datetime(year, month, 1).strftime("%Y-%m-%d")
    month_end = datetime(year, month + 1, 1).strftime("%Y-%m-%d") if month < 12 else f"{year+1}-01-01"

    events = frappe.get_all(
        "Event",
        filters=[
            ["starts_on", ">=", month_start],
            ["starts_on", "<", month_end],
            ["event_type", "=", "Public"],
        ],
        fields=["name", "subject", "starts_on", "ends_on", "event_category", "location", "description", "all_day"],
        order_by="starts_on asc",
    )

    # Build calendar grid
    weeks = []
    day = 1
    for w in range(6):
        week = []
        for d in range(7):
            if (w == 0 and d < start_day) or day > days_in_month:
                week.append({"day": 0, "events": []})
            else:
                day_str = f"{year}-{month:02d}-{day:02d}"
                day_events = [e for e in events if e.starts_on and e.starts_on.strftime("%Y-%m-%d") == day_str]
                week.append({"day": day, "events": day_events})
                day += 1
        weeks.append(week)
        if day > days_in_month:
            break

    context.weeks = weeks

    # Upcoming events (next 30 days)
    today_str = datetime.now().strftime("%Y-%m-%d")
    end_str = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
    upcoming = frappe.get_all(
        "Event",
        filters=[
            ["starts_on", ">=", today_str],
            ["starts_on", "<=", end_str],
            ["event_type", "=", "Public"],
        ],
        fields=["name", "subject", "starts_on", "ends_on", "event_category", "location", "description", "all_day"],
        order_by="starts_on asc",
        limit=10,
    )
    context.upcoming = upcoming

    # Fetch attachments for all events (grid + upcoming)
    all_event_names = [e.name for e in events] + [e.name for e in upcoming]
    attachments = _get_attachments(all_event_names)
    context.attachments = attachments

    return context


def _get_attachments(event_names):
    """Return dict of event_name → list of attached files."""
    if not event_names:
        return {}
    files = frappe.get_all(
        "File",
        filters=[
            ["attached_to_doctype", "=", "Event"],
            ["attached_to_name", "in", event_names],
        ],
        fields=["attached_to_name", "file_url", "file_name", "file_size"],
    )
    result = {}
    for f in files:
        result.setdefault(f.attached_to_name, []).append(f)
    return result
