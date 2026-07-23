app_name = "dohw_intranet"
app_title = "DoWH Intranet"
app_publisher = "Department of Works and Highways"
app_description = "DoWH Staff Intranet Portal"
app_email = "ict@works.gov.pg"
app_license = "mit"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "dohw_intranet",
# 		"logo": "/assets/dohw_intranet/logo.png",
# 		"title": "DoWH Intranet",
# 		"route": "/dohw_intranet",
# 		"has_permission": "dohw_intranet.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/dohw_intranet/css/dohw_intranet.css"
# app_include_js = "/assets/dohw_intranet/js/dohw_intranet.js"

# include js, css files in header of web template
# web_include_css = "/assets/dohw_intranet/css/dohw_intranet.css"
# web_include_js = "/assets/dohw_intranet/js/dohw_intranet.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "dohw_intranet/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "dohw_intranet/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# automatically load and sync documents of this doctype from downstream apps
# importable_doctypes = [doctype_1]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "dohw_intranet.utils.jinja_methods",
# 	"filters": "dohw_intranet.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "dohw_intranet.install.before_install"
# after_install = "dohw_intranet.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "dohw_intranet.uninstall.before_uninstall"
# after_uninstall = "dohw_intranet.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "dohw_intranet.utils.before_app_install"
# after_app_install = "dohw_intranet.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "dohw_intranet.utils.before_app_uninstall"
# after_app_uninstall = "dohw_intranet.utils.after_app_uninstall"

# Build
# ------------------
# To hook into the build process

# after_build = "dohw_intranet.build.after_build"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "dohw_intranet.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"dohw_intranet.tasks.all"
# 	],
# 	"daily": [
# 		"dohw_intranet.tasks.daily"
# 	],
# 	"hourly": [
# 		"dohw_intranet.tasks.hourly"
# 	],
# 	"weekly": [
# 		"dohw_intranet.tasks.weekly"
# 	],
# 	"monthly": [
# 		"dohw_intranet.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "dohw_intranet.install.before_tests"

# Extend DocType Class
# ------------------------------
#
# Specify custom mixins to extend the standard doctype controller.
# extend_doctype_class = {
# 	"Task": "dohw_intranet.custom.task.CustomTaskMixin"
# }

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "dohw_intranet.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "dohw_intranet.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["dohw_intranet.utils.before_request"]
# after_request = ["dohw_intranet.utils.after_request"]

# Job Events
# ----------
# before_job = ["dohw_intranet.utils.before_job"]
# after_job = ["dohw_intranet.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"dohw_intranet.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

# Translation
# ------------
# List of apps whose translatable strings should be excluded from this app's translations.
# ignore_translatable_strings_from = []

