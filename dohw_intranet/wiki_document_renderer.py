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

Wiki Document itself is queried via raw SQL rather than the ORM
(frappe.get_all/get_value/get_doc): the `wiki` app's modules.txt only
registers the old "Wiki" module, so frappe_wiki's doctypes — including
Wiki Document — were never synced into tabDocType even though their tables
and data exist. Any ORM call against them raises
`DoesNotExistError: DocType Wiki Document not found`. Wiki Space *is*
registered (it's shared with the old architecture), so it's queried
normally. Registering frappe_wiki's module properly is a wiki-app-level
fix that's out of scope here — this stays a read-only, parameterized-SQL
workaround scoped entirely to dohw_intranet.
"""

import frappe
from frappe.website.page_renderers.document_page import DocumentPage
from frappe.website.utils import build_response

WIKI_DOCUMENT_FIELDS = "name, title, route, content, is_published, is_group, wiki_space, parent_wiki_document, sort_order"


class WikiDocumentRenderer(DocumentPage):
    def can_render(self):
        doc = self._get_document_by_route(self.path)
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

        doc = self._get_document(self.docname)
        space = frappe.get_cached_doc("Wiki Space", doc.wiki_space) if doc.wiki_space else None

        # init_context()/post_process_context() come from BaseTemplatePage and set up
        # required website context (base_template_path, metatags, etc.) — DocumentPage's
        # own get_html() does this too, but assumes self.doc is a real ORM Document,
        # which Wiki Document isn't (see module docstring), so it's replicated here
        # around our own raw-SQL-backed context values instead.
        self.init_context()
        self.context.doc = doc
        self.context.space = space
        self.context.title = doc.title
        self.context.content_html = frappe.utils.md_to_html(doc.content) if doc.content else None
        self.context.breadcrumbs = self._get_breadcrumbs(doc)
        self.context.children = self._get_children(doc.name) if doc.is_group else []
        self.context.tree = self._get_tree(space) if space else []
        self.context.spaces = self._get_spaces()
        self.context.current_route = self.path
        self.post_process_context()

        html = frappe.get_template("templates/wiki_document.html").render(self.context)
        html = self.add_csrf_token(html)
        return build_response(self.path, html, self.http_status_code or 200, self.headers)

    @staticmethod
    def _get_document_by_route(route):
        rows = frappe.db.sql(
            f"""select {WIKI_DOCUMENT_FIELDS} from `tabWiki Document` where route = %s""",
            (route,),
            as_dict=True,
        )
        return rows[0] if rows else None

    @staticmethod
    def _get_document(name):
        rows = frappe.db.sql(
            f"""select {WIKI_DOCUMENT_FIELDS} from `tabWiki Document` where name = %s""",
            (name,),
            as_dict=True,
        )
        return rows[0] if rows else None

    @staticmethod
    def _get_children(parent_name):
        return frappe.db.sql(
            """select name, title, route, is_group from `tabWiki Document`
            where parent_wiki_document = %s and is_published = 1
            order by sort_order asc""",
            (parent_name,),
            as_dict=True,
        )

    @staticmethod
    def _get_breadcrumbs(doc):
        """Ancestor trail, excluding the space's own (structural, unpublished) root group."""
        trail = []
        node = doc
        seen = set()
        while node and node.parent_wiki_document and node.parent_wiki_document not in seen:
            seen.add(node.parent_wiki_document)
            rows = frappe.db.sql(
                """select name, title, route, parent_wiki_document from `tabWiki Document`
                where name = %s""",
                (node.parent_wiki_document,),
                as_dict=True,
            )
            parent = rows[0] if rows else None
            if not parent or not parent.parent_wiki_document:
                break
            trail.insert(0, parent)
            node = parent
        return trail

    @staticmethod
    def _get_tree(space):
        rows = frappe.db.sql(
            """select name, title, route, is_group, parent_wiki_document, sort_order
            from `tabWiki Document` where wiki_space = %s and is_published = 1
            order by sort_order asc""",
            (space.name,),
            as_dict=True,
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
