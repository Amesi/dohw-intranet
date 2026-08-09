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
    "/assets/dohw_intranet/css/dohw_intranet.css",
]

# Portal settings hook
website_context = {
    "favicon": "/files/dowh-favicon.png",
}
