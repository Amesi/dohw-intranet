"""Prototype index — navigation to all zone prototypes."""

import frappe

def get_context(context):
    context.no_cache = 1
    context.show_sidebar = 1
    context.title = "Intranet Prototypes"
    return context
