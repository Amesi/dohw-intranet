"""DoWH Intranet — Frappe app hooks."""

app_name = "dohw_intranet"
app_title = "DoWH Intranet"
app_publisher = "Department of Works and Highways"
app_description = "DoWH Staff Intranet Portal"
app_email = "ict@works.gov.pg"
app_license = "mit"

# Home page — circulars listing
home_page = "/circulars"

# Web CSS — loaded on all website pages
web_include_css = "/assets/dohw_intranet/css/dohw_intranet.css"

# Website context
website_context = {
    "favicon": "/files/dowh-favicon.png",
}
