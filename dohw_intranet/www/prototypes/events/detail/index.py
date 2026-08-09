"""Prototype — Event detail page: WHEN/WHERE/HOSTED BY sidebar, RSVP, attendee list."""

import frappe

MOCK_EVENT = {
    "title": "Annual Safety Week Opening Ceremony",
    "description": "Site inductions, PPE audits, and a department-wide toolbox talk kicking off this year's Safety Week. All Wings are encouraged to send representatives, and safety officers from each region will present their induction updates.",
    "date": "18 Aug 2026",
    "time": "9:00 AM",
    "venue": "DoWH Head Office Auditorium",
    "host": "Corporate Services Wing",
    "attendees": [
        {"name": "Victor Temokang", "status": "Yes"},
        {"name": "Grace Tupa", "status": "Yes"},
        {"name": "Peter Kaman", "status": "Maybe"},
        {"name": "Mary Kila", "status": "Yes"},
        {"name": "John Aromo", "status": "Yes"},
    ],
}


def get_context(context):
    context.no_cache = 1
    context.show_sidebar = 0
    context.title = MOCK_EVENT["title"] + " — Prototype"
    context.variant = frappe.form_dict.get("variant", "a")
    context.event = MOCK_EVENT
    return context
