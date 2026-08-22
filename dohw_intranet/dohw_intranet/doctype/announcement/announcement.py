"""DoWH Announcement — staff circulars with WebsiteGenerator integration."""

import frappe
from frappe.website.website_generator import WebsiteGenerator


class Announcement(WebsiteGenerator):
    # begin: auto-generated types
    from typing import TYPE_CHECKING
    if TYPE_CHECKING:
        from frappe.types import DF
        circular_number: DF.Data | None
        classification: DF.Literal["For Information", "For Action", "Urgent"]
        content: DF.TextEditor | None
        date: DF.Date
        priority: DF.Literal["Normal", "Important", "Urgent"]
        published: DF.Check
        route: DF.Data | None
        tags: DF.Data | None
        title: DF.Data
        wing: DF.Link | None
    # end: auto-generated types

    def before_save(self):
        """Auto-generate circular number if not set."""
        if not self.circular_number:
            self.circular_number = self._generate_circular_number()

    def _generate_circular_number(self) -> str:
        """Generate a sequential circular number like C-2026-001."""
        year = frappe.utils.getdate(self.date).year if self.date else frappe.utils.nowdate()[:4]
        count = frappe.db.count("Announcement", {"date": (">=", f"{year}-01-01")}) + 1
        return f"C-{year}-{count:03d}"

    def get_context(self, context):
        """Detail page context."""
        context.no_cache = 1
        context.show_sidebar = 1
        context.title = self.title
        context.parents = self.get_parents(context)
        return context

    def get_parents(self, context):
        """Breadcrumb trail — Wing hierarchy."""
        parents = [{"label": "Circulars", "route": "/circulars"}]
        if self.wing:
            parents.append({
                "label": self.wing,
                "route": f"/circulars?wing={self.wing}",
            })
        return parents


def get_list_context(context=None):
    """Configure the circular listing page."""
    context.update({
        "title": "Staff Circulars & Announcements",
        "no_cache": 1,
        "show_sidebar": 1,
        "order_by": "date desc",
        "list_title": "Staff Circulars & Announcements",
        "template": "dohw_intranet/templates/generators/announcement.html",
        "list_template": "dohw_intranet/templates/generators/announcement.html",
        "row_template": "dohw_intranet/templates/generators/announcement_row.html",
    })

    # Wing and classification filters
    wing_filter = frappe.form_dict.get("wing")
    class_filter = frappe.form_dict.get("classification")

    filters = {}
    if wing_filter:
        filters["wing"] = wing_filter
    if class_filter:
        filters["classification"] = class_filter

    context["filters"] = filters
    context["active_wing"] = wing_filter
    context["active_class"] = class_filter

    # Wings for filter dropdown
    context["wings"] = frappe.get_all(
        "Department",
        filters={"company": "Department of Works and Highways", "is_group": 1},
        fields=["name", "department_name"],
    )

    # All tags for tag cloud
    all_announcements = frappe.get_all(
        "Announcement", filters={"published": 1}, fields=["tags"]
    )
    tag_set = set()
    for a in all_announcements:
        if a.tags:
            for t in a.tags.split(","):
                tag_set.add(t.strip().lower())
    context["all_tags"] = sorted(tag_set)
    context["active_tag"] = frappe.form_dict.get("tag")

    # Quick stats
    context["stats"] = {
        "total": frappe.db.count("Announcement", {"published": 1}),
        "urgent": frappe.db.count("Announcement", {"published": 1, "classification": "Urgent"}),
        "for_action": frappe.db.count("Announcement", {"published": 1, "classification": "For Action"}),
    }

    # Introduction masthead
    context["introduction"] = (
        '<div class="dowh-masthead">'
        '<img src="/files/dowh-logo-original.svg" alt="DoWH Seal" class="dowh-seal">'
        '<h1>Department of Works & Highways</h1>'
        '<h2>Staff Circulars & Announcements</h2>'
        '</div>'
    )

    return context
