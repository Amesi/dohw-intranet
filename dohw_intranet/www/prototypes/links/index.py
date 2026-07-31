"""Links & Electronic Forms prototype."""

import frappe

def get_context(context):
    context.no_cache = 1
    context.show_sidebar = 1
    context.title = "Links & Electronic Forms"
    return context
