"""Custom page_renderer serving Wiki Document content (frappe_wiki namespace).

The installed `wiki` app is pinned to upstream's `master` branch, which
already ships the Wiki Document data model and its Desk-side authoring UI,
but the website-facing renderer for that model only exists on upstream's
`develop` branch. Master's own page_renderer (WikiPageRenderer) only knows
the older Wiki Page doctype, which has zero rows on this site — so real
content already authored under Wiki Document/Wiki Space was invisible.

This renderer serves that content directly, styled to match the portal,
without bumping a third-party app to an unstable branch on a live production
site. Registered ahead of the wiki app's own page_renderer in hooks.py
(dohw_intranet is installed before wiki, and frappe.get_hooks merges
page_renderer in install order) so it claims space/document routes before
WikiPageRenderer's own (buggy, empty-sidebar) fallback ever runs.
"""

import frappe
from frappe.website.page_renderers.document_page import DocumentPage
from frappe.website.utils import build_response


class WikiDocumentRenderer(DocumentPage):
    def can_render(self):
        doc = frappe.db.get_value(
            "Wiki Document",
            {"route": self.path},
            ["name", "is_published", "is_group", "parent_wiki_document"],
            as_dict=True,
        )
        if not doc:
            return False

        # Root group nodes (the space's own landing page) are structural and
        # always unpublished by design — still render them as the space home.
        is_root_group = doc.is_group and not doc.parent_wiki_document
        if doc.is_published or is_root_group:
            self.docname = doc.name
            return True
        return False

    def render(self):
        if frappe.session.user == "Guest":
            frappe.local.flags.redirect_location = f"/login?redirect-to=/{self.path}"
            raise frappe.Redirect

        doc = frappe.get_cached_doc("Wiki Document", self.docname)
        space = frappe.get_cached_doc("Wiki Space", doc.wiki_space) if doc.wiki_space else None

        context = frappe._dict()
        context.doc = doc
        context.space = space
        context.title = doc.title
        context.content_html = frappe.utils.md_to_html(doc.content) if doc.content else None
        context.breadcrumbs = self._get_breadcrumbs(doc)
        context.children = self._get_children(doc.name) if doc.is_group else []
        context.tree = self._get_tree(space) if space else []
        context.spaces = self._get_spaces()
        context.current_route = self.path

        html = frappe.get_template("templates/wiki_document.html").render(context)
        html = self.add_csrf_token(html)
        return build_response(self.path, html, self.http_status_code or 200, self.headers)

    @staticmethod
    def _get_children(parent_name):
        return frappe.get_all(
            "Wiki Document",
            filters={"parent_wiki_document": parent_name, "is_published": 1},
            fields=["name", "title", "route", "is_group"],
            order_by="sort_order asc",
        )

    @staticmethod
    def _get_breadcrumbs(doc):
        """Ancestor trail, excluding the space's own (structural, unpublished) root group."""
        trail = []
        node = doc
        seen = set()
        while node and node.parent_wiki_document and node.parent_wiki_document not in seen:
            seen.add(node.parent_wiki_document)
            parent = frappe.db.get_value(
                "Wiki Document",
                node.parent_wiki_document,
                ["name", "title", "route", "parent_wiki_document"],
                as_dict=True,
            )
            if not parent or not parent.parent_wiki_document:
                break
            trail.insert(0, parent)
            node = parent
        return trail

    @staticmethod
    def _get_tree(space):
        rows = frappe.get_all(
            "Wiki Document",
            filters={"wiki_space": space.name, "is_published": 1},
            fields=["name", "title", "route", "is_group", "parent_wiki_document", "sort_order"],
            order_by="sort_order asc",
        )
        by_parent = {}
        for r in rows:
            by_parent.setdefault(r.parent_wiki_document, []).append(r)

        def build(parent_name):
            nodes = []
            for r in by_parent.get(parent_name, []):
                r["children"] = build(r.name)
                nodes.append(r)
            return nodes

        return build(space.root_group)

    @staticmethod
    def _get_spaces():
        return frappe.get_all(
            "Wiki Space",
            filters={"show_in_switcher": 1, "is_published": 1},
            fields=["route", "space_name"],
            order_by="switcher_order asc",
        )
