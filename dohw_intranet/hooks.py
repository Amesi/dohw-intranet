"""DoWH Intranet — Frappe app hooks."""

app_name = "dohw_intranet"
app_title = "DoWH Digital Portal"
app_publisher = "Department of Works and Highways"
app_description = "DoWH Digital Portal"
app_email = "ict@works.gov.pg"
app_license = "mit"

# Website generators — auto-generate web pages from DocTypes
website_generators = ["Announcement", "Blog Post"]

# Home page: circular listing is the default landing
home_page = "/circulars"

# Web CSS — all styling now lives in public/scss/website.scss, compiled into the
# "DoWH" Website Theme (see docs/design/tokens.md + navigation.md). The Website
# Theme is installed via fixture and activated in Website Settings, so no
# per-request web_include_css is needed here.

# Portal settings hook
website_context = {
    "favicon": "/files/dowh-favicon.png",
}

# Custom page_renderers for per-record routes that a normal www/ controller
# can't serve (Wiki Document and Event routes are per-record, not fixed
# pages) — see each renderer module's own docstring for detail. Blog Post is
# now a WebsiteGenerator (auto-served), so its renderer was removed.
page_renderer = [
    "dohw_intranet.wiki_document_renderer.WikiDocumentRenderer",
    "dohw_intranet.event_renderer.EventRenderer",
]

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
    {"doctype": "Website Theme", "filters": {"name": "DoWH"}},
    {"doctype": "Website Settings", "filters": {"name": "Website Settings"}},
]
