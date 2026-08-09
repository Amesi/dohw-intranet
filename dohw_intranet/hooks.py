"""DoWH Intranet — Frappe app hooks."""

app_name = "dohw_intranet"
app_title = "DoWH Intranet"
app_publisher = "Department of Works and Highways"
app_description = "DoWH Staff Intranet Portal"
app_email = "ict@works.gov.pg"
app_license = "mit"

# Website generators — auto-generate web pages from DocTypes
website_generators = ["Announcement"]

# Home page: circular listing is the default landing
home_page = "/circulars"

# Web CSS — loaded on all website pages.
# tokens.css is the frappe.io-modeled design-token foundation (see docs/design/tokens.md);
# dohw_intranet.css is the pre-revamp stylesheet, kept until each page's own build
# ticket migrates it off — do not remove until every page ticket has landed.
web_include_css = [
    "/assets/dohw_intranet/css/tokens.css",
    "/assets/dohw_intranet/css/navigation.css",
    "/assets/dohw_intranet/css/dohw_intranet.css",
]

# Portal settings hook
website_context = {
    "favicon": "/files/dowh-favicon.png",
}

# Custom page_renderer for /wiki content — see dohw_intranet/wiki_document_renderer.py
# for why this exists instead of relying on the wiki app's own renderer. Must be
# installed (hence listed) before "wiki" so it claims these routes first — see
# frappe.get_hooks()'s install-order merge, and the app's own docstring for detail.
page_renderer = ["dohw_intranet.wiki_document_renderer.WikiDocumentRenderer"]

# Fixtures — schema additions this app depends on, reproducible on any site
# via `bench migrate` rather than living only as a manual DB change.
# One fixture entry per doctype file: `bench export-fixtures` writes one
# output file per (doctype, filter) pair to a name derived from the doctype
# alone, so two separate "Custom Field" entries clobber each other rather
# than merging — hence a single filter here scoped by fieldname (specific
# enough not to collide with unrelated custom fields, e.g. HRMS's own
# Employee fields) rather than by dt.
fixtures = [
    {"doctype": "Custom Field", "filters": [["fieldname", "in", ["wing", "content_manager", "blog_author"]]]},
]
