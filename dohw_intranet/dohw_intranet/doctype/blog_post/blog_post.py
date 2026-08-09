"""DoWH Blog Post — internal editorial content, Draft -> In Review -> Published.

See docs/design/blog.md for the full decision record. Route is auto-slugified
from title (no WebsiteGenerator — this app's convention is custom www/
controllers + a custom page_renderer for per-record routes, matching how
Wiki content is served, not Frappe's built-in website-generator flow).
"""

import re

import frappe
from frappe.model.document import Document


class BlogPost(Document):
    # begin: auto-generated types
    from typing import TYPE_CHECKING
    if TYPE_CHECKING:
        from frappe.types import DF
        author: DF.Link
        category: DF.Literal["Project Updates", "Staff Spotlight", "Department News", "ICT & Systems"]
        content: DF.TextEditor | None
        excerpt: DF.SmallText | None
        featured_image: DF.AttachImage | None
        published_date: DF.Datetime | None
        rejection_reason: DF.SmallText | None
        reviewer: DF.Link | None
        route: DF.Data | None
        status: DF.Literal["Draft", "In Review", "Published"]
        title: DF.Data
    # end: auto-generated types

    def before_insert(self):
        if not self.route:
            self.route = self._make_unique_route()

    def _make_unique_route(self) -> str:
        base = re.sub(r"[^a-z0-9]+", "-", self.title.lower()).strip("-") or "post"
        route = base
        n = 2
        while frappe.db.exists("Blog Post", {"route": route}):
            route = f"{base}-{n}"
            n += 1
        return route

    @frappe.whitelist()
    def submit_for_review(self):
        if self.status != "Draft":
            frappe.throw(frappe._("Only a Draft can be submitted for review"))
        self.status = "In Review"
        self.save()

    @frappe.whitelist()
    def approve(self):
        self._check_reviewer_not_author()
        if self.status != "In Review":
            frappe.throw(frappe._("Only a post In Review can be approved"))
        self.status = "Published"
        self.reviewer = _current_employee()
        self.published_date = frappe.utils.now_datetime()
        self.rejection_reason = None
        self.save()

    @frappe.whitelist()
    def reject(self, reason: str):
        self._check_reviewer_not_author()
        if self.status != "In Review":
            frappe.throw(frappe._("Only a post In Review can be rejected"))
        self.status = "Draft"
        self.reviewer = _current_employee()
        self.rejection_reason = reason
        self.save()

    def _check_reviewer_not_author(self):
        if _current_employee() == self.author:
            frappe.throw(frappe._("You cannot review your own post"))


def _current_employee():
    return frappe.db.get_value("Employee", {"user_id": frappe.session.user}, "name")
