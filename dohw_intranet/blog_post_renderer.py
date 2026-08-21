"""Custom page_renderer serving individual Blog Post articles at /blog/<route>.

Blog Post routes are per-record slugs (e.g. "historic-steel-arch-bridge..."),
not a fixed page, so a normal www/ controller can't serve them — same
reasoning as WikiDocumentRenderer. Unlike Wiki Document, Blog Post is a
properly-registered doctype (created via bench migrate, not orphaned
metadata), so this uses the ORM normally rather than raw SQL.
"""

import frappe
from frappe.website.page_renderers.document_page import DocumentPage
from frappe.website.utils import build_response

from dohw_intranet.sanitize import sanitize_rich_html


class BlogPostRenderer(DocumentPage):
    def can_render(self):
        if not self.path.startswith("blog/"):
            return False

        route = self.path[len("blog/"):]
        if not route:
            return False

        name = frappe.db.get_value("Blog Post", {"route": route, "status": "Published"}, "name")
        if not name:
            return False

        self.docname = name
        return True

    def render(self):
        if frappe.session.user == "Guest":
            frappe.local.flags.redirect_location = f"/login?redirect-to=/{self.path}"
            raise frappe.Redirect

        doc = frappe.get_cached_doc("Blog Post", self.docname)
        doc.content = sanitize_rich_html(doc.content or "")
        author_name = frappe.db.get_value("Employee", doc.author, "employee_name") or doc.author
        word_count = len((doc.content or "").split())
        read_time = max(1, round(word_count / 200))

        self.init_context()
        self.context.doc = doc
        self.context.author_name = author_name
        self.context.read_time = f"{read_time} min read"
        self.post_process_context()

        html = frappe.get_template("templates/blog_post.html").render(self.context)
        html = self.add_csrf_token(html)
        return build_response(self.path, html, self.http_status_code or 200, self.headers)
