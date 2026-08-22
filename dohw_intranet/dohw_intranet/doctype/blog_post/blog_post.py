"""DoWH Blog Post — internal editorial content, Draft -> In Review -> Published.

A WebsiteGenerator (see hooks.py `website_generators`): published posts are
served at `/blog/<route>` via the standard generator flow, replacing the old
custom `blog_post_renderer.py`. Web visibility is gated by the boolean
`published` field (kept in sync with the `status` workflow), because the
website router's document lookup filters on `is_published_field == 1` and a
`status` Select can't satisfy that.

See docs/design/blog.md for the full decision record.
"""

import re

import frappe
from frappe.website.website_generator import WebsiteGenerator

from dohw_intranet.sanitize import sanitize_rich_html


class BlogPost(WebsiteGenerator):
    # begin: auto-generated types
    from typing import TYPE_CHECKING
    if TYPE_CHECKING:
        from frappe.types import DF
        author: DF.Link
        category: DF.Literal["Project Updates", "Staff Spotlight", "Department News", "ICT & Systems"]
        content: DF.TextEditor | None
        excerpt: DF.SmallText | None
        featured_image: DF.AttachImage | None
        published: DF.Check
        published_date: DF.Datetime | None
        rejection_reason: DF.SmallText | None
        reviewer: DF.Link | None
        route: DF.Data | None
        status: DF.Literal["Draft", "In Review", "Published"]
        title: DF.Data
    # end: auto-generated types

    def before_insert(self):
        # Drafts need a route too (the compose/edit flow looks posts up by
        # route), so assign it on insert regardless of publish state. The
        # WebsiteGenerator `validate`/`set_route` only routes published docs.
        if not self.route:
            self.route = self._make_unique_route()

    def _make_unique_route(self) -> str:
        base = re.sub(r"[^a-z0-9]+", "-", self.title.lower()).strip("-") or "post"
        route = f"blog/{base}"
        n = 2
        while frappe.db.exists("Blog Post", {"route": route}):
            route = f"blog/{base}-{n}"
            n += 1
        return route

    def get_context(self, context):
        """Detail page context, served by the standard generator flow."""
        context.no_cache = 1
        context.title = self.title
        # Sanitize on read — legacy posts were authored via a bare
        # contenteditable and never passed through the editor's sanitizer.
        self.content = sanitize_rich_html(self.content or "")
        context.author_name = (
            frappe.db.get_value("Employee", self.author, "employee_name") or self.author
        )
        word_count = len((self.content or "").split())
        context.read_time = f"{max(1, round(word_count / 200))} min read"
        return context

    def has_website_permission(self, ptype="read", user=None, verbose=False):
        """Gate the detail page to logged-in staff (matches /blog and /blog/manage).

        The website router checks this during `can_render()`; raising a redirect
        here preserves the old custom renderer's behaviour of sending guests to
        /login?redirect-to=<route> rather than a bare 404.
        """
        if frappe.session.user == "Guest":
            frappe.local.flags.redirect_location = f"/login?redirect-to=/{self.route}"
            raise frappe.Redirect
        return True

    @frappe.whitelist()
    def submit_for_review(self):
        if self.status != "Draft":
            frappe.throw(frappe._("Only a Draft can be submitted for review"))
        self.status = "In Review"
        self.published = 0
        self.save()

    @frappe.whitelist()
    def approve(self):
        self._check_reviewer_not_author()
        if self.status != "In Review":
            frappe.throw(frappe._("Only a post In Review can be approved"))
        self.status = "Published"
        self.published = 1
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
        self.published = 0
        self.reviewer = _current_employee()
        self.rejection_reason = reason
        self.save()

    def _check_reviewer_not_author(self):
        if _current_employee() == self.author:
            frappe.throw(frappe._("You cannot review your own post"))


def _current_employee():
    return frappe.db.get_value("Employee", {"user_id": frappe.session.user}, "name")
