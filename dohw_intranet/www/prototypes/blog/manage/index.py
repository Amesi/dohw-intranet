"""Prototype — Blog Author compose/manage area (drafts, submit for review, review queue).

Not variant-switched — this is a workflow screen, not a "look" fork; the
data model ticket (#44) already fixed the states, so this is one concrete
take on how a Blog Author moves through them day to day.
"""

import frappe

MY_DRAFTS = [
    {"title": "PTS Vehicle Tender Exercise to Support Future Fleet Replacement", "updated": "2 days ago"},
    {"title": "(Untitled draft)", "updated": "5 days ago"},
]

PENDING_REVIEW = [
    {"title": "Technical Audit Division Established to Strengthen Road Infrastructure Oversight", "author": "DoWH Corporate Communications", "submitted": "1 day ago"},
]

PUBLISHED = [
    {"title": "Historic Steel Arch Bridge to Transform Momase Connectivity", "date": "11 May 2026"},
    {"title": "Staff from the NPDS Wing Spent King's Birthday Public Holiday on Building Bonds", "date": "19 Jun 2026"},
]


def get_context(context):
    context.no_cache = 1
    context.show_sidebar = 0
    context.title = "Blog — Manage — Prototype"
    context.drafts = MY_DRAFTS
    context.pending_review = PENDING_REVIEW
    context.published = PUBLISHED
    return context
