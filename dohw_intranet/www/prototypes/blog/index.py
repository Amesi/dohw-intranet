"""Prototype — Blog listing. Variant A (Reading List) chosen; B/C kept reachable
via the switcher for reference only.

Resolves wayfinder ticket "Blog listing & article page layout" (issue #45),
child of the "Blog" map (#42). No Blog Post doctype exists yet — this map is
decisions-only, building happens in a later map.

Content below is real, extracted from the live DoWH website
(www.works.gov.pg/articles) for realism rather than fabricated — titles,
dates and excerpts are copied as published there; bylines aren't shown on
the source site's listing so they're attributed to "DoWH Corporate
Communications" except where an individual byline is credited on the
full article (see post/index.py).
"""

import frappe

MOCK_POSTS = [
    {
        "title": "Historic Steel Arch Bridge to Transform Momase Connectivity",
        "excerpt": "The Hawaiin Bridge — PNG's first steel arch bridge, built without a centre pier — nears completion on the Coastal Highway linking Wewak to the Wutung border.",
        "category": "Project Updates",
        "author": "Brian Alois",
        "date": "11 May 2026",
        "image": True,
    },
    {
        "title": "Connect PNG Program: Tifalmin New Road Opening",
        "excerpt": "Community celebration marked the opening of a 19-kilometer road connecting Rakmin to Tifalmin, with hundreds attending the milestone event.",
        "category": "Project Updates",
        "author": "DoWH Corporate Communications",
        "date": "9 May 2026",
        "image": True,
    },
    {
        "title": "Staff from the NPDS Wing Spent King's Birthday Public Holiday on Building Bonds",
        "excerpt": "More than 100 NPDS staff marked the King's Birthday public holiday with a team-building programme at Loloata Island Resort.",
        "category": "Staff Spotlight",
        "author": "DoWH Corporate Communications",
        "date": "19 Jun 2026",
        "image": True,
    },
    {
        "title": "DoWH Secures 50 Housing Allotments for Staff Under National Housing Corporation Partnership",
        "excerpt": "Partnership provides housing allotments supporting staff welfare and home ownership aspirations.",
        "category": "Staff Spotlight",
        "author": "DoWH Corporate Communications",
        "date": "20 Jun 2026",
        "image": False,
    },
    {
        "title": "Technical Audit Division Established to Strengthen Road Infrastructure Oversight",
        "excerpt": "DoWH establishes a new Technical Audit Division to enhance compliance, governance, and accountability across road infrastructure projects.",
        "category": "Department News",
        "author": "DoWH Corporate Communications",
        "date": "10 Jul 2026",
        "image": False,
    },
    {
        "title": "Department of Works & Highways Launches Electronic Funds Transfer System",
        "excerpt": "New EFT system modernizes payment processing, replacing cheques with secure electronic transfers integrated with banking systems.",
        "category": "ICT & Systems",
        "author": "DoWH Corporate Communications",
        "date": "22 Jun 2026",
        "image": False,
    },
]


def get_context(context):
    context.no_cache = 1
    context.show_sidebar = 0
    context.title = "Blog — Prototype"
    context.variant = frappe.form_dict.get("variant", "a")
    context.posts = MOCK_POSTS
    return context
