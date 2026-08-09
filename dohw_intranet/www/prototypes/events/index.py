"""Prototype — Events listing, 3 variants switchable via ?variant=a|b|c.

Resolves wayfinder ticket "Events listing & detail page layout" (issue #53),
child of the "Events" map (#50). Mock data only — no build yet, this map is
decisions-only. Events are ERPNext Event records with event_category="Event"
per #52's resolution; mock data mirrors that shape.
"""

import frappe

MOCK_EVENTS = [
    {
        "title": "Annual Safety Week Opening Ceremony",
        "description": "Site inductions, PPE audits, and a department-wide toolbox talk kicking off this year's Safety Week.",
        "date": "18 Aug 2026",
        "time": "9:00 AM",
        "venue": "DoWH Head Office Auditorium",
        "host": "Corporate Services Wing",
        "image": True,
        "going": 42,
    },
    {
        "title": "ICT Systems Training: New Staff Intranet Features",
        "description": "A walkthrough of the Wiki, Blog, and Events sections for staff who want a guided tour before diving in.",
        "date": "21 Aug 2026",
        "time": "2:00 PM",
        "venue": "Virtual — Zoom",
        "host": "Finance and ICT",
        "image": False,
        "going": 15,
    },
    {
        "title": "Highlands Highway Project Launch",
        "description": "Official launch of the Kagamuga–Kimininga rehabilitation works, with remarks from the Works Secretary.",
        "date": "3 Sep 2026",
        "time": "10:00 AM",
        "venue": "Mt Hagen District Office",
        "host": "Highways Management Wing",
        "image": True,
        "going": 28,
    },
    {
        "title": "All-Staff Town Hall — Q3",
        "description": "Quarterly department-wide briefing on budget, major project milestones, and staff welfare updates.",
        "date": "10 Sep 2026",
        "time": "1:00 PM",
        "venue": "DoWH Head Office Auditorium",
        "host": "Office of the Secretary",
        "image": False,
        "going": 96,
    },
    {
        "title": "Corporate Services Workshop: Procurement Compliance",
        "description": "A half-day workshop on the updated procurement compliance checklist ahead of the new Technical Audit Division's first review cycle.",
        "date": "16 Sep 2026",
        "time": "9:30 AM",
        "venue": "Virtual — Zoom",
        "host": "Corporate Services Wing",
        "image": False,
        "going": 19,
    },
]


def get_context(context):
    context.no_cache = 1
    context.show_sidebar = 0
    context.title = "Events — Prototype"
    context.variant = frappe.form_dict.get("variant", "a")
    context.events = MOCK_EVENTS
    return context
