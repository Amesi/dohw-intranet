"""DoWH Announcement — staff circulars.

Plain Document (not a WebsiteGenerator): circulars are served by the
www/circulars controller with inline <details> expansion and no separate
detail route, per docs/design/circulars.md. The generator registration
was removed because it shadowed the www controller and crashed on
/circulars/<slug> (no detail template).
"""

import frappe
from frappe.model.document import Document


class Announcement(Document):
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
