"""Custom page_renderer serving individual Event detail pages at /events/<name>.

Event routes use the doctype's own autoname id directly (e.g. "EV00002")
rather than a slug — unlike Blog Post, this is a stock ERPNext doctype and
no new route/slug field is added to it just for prettier URLs, per
docs/design/events.md. Handles RSVP as a POST-then-redirect on the same
route, writing to core ERPNext's Event Participants child table.
"""

import frappe
from frappe.website.page_renderers.document_page import DocumentPage
from frappe.website.utils import build_response


class EventRenderer(DocumentPage):
    def can_render(self):
        if not self.path.startswith("events/"):
            return False

        name = self.path[len("events/"):]
        if not name:
            return False

        exists = frappe.db.exists("Event", {"name": name, "event_category": "Event"})
        if not exists:
            return False

        self.docname = name
        return True

    def render(self):
        if frappe.session.user == "Guest":
            frappe.local.flags.redirect_location = f"/login?redirect-to=/{self.path}"
            raise frappe.Redirect

        employee = frappe.db.get_value("Employee", {"user_id": frappe.session.user}, "name")

        if frappe.request.method == "POST":
            status = frappe.form_dict.get("rsvp_status")
            if employee and status in ("Yes", "No", "Maybe"):
                self._set_rsvp(self.docname, employee, status)
            frappe.local.flags.redirect_location = f"/{self.path}"
            raise frappe.Redirect

        doc = frappe.get_cached_doc("Event", self.docname)
        host_name = frappe.db.get_value("Department", doc.wing, "department_name") if doc.wing else None

        attendees = frappe.get_all(
            "Event Participants",
            filters={"parent": doc.name, "reference_doctype": "Employee"},
            fields=["reference_docname", "attending"],
        )
        emp_names = frappe.get_all(
            "Employee", filters={"name": ["in", [a.reference_docname for a in attendees]] or [""]},
            fields=["name", "employee_name"],
        )
        emp_map = {e.name: e.employee_name for e in emp_names}
        for a in attendees:
            a.employee_name = emp_map.get(a.reference_docname, a.reference_docname)

        my_rsvp = next((a.attending for a in attendees if a.reference_docname == employee), None)

        self.init_context()
        self.context.event = doc
        self.context.host_name = host_name or "Department of Works and Highways"
        self.context.attendees = [a for a in attendees if a.attending]
        self.context.going_count = len([a for a in attendees if a.attending == "Yes"])
        self.context.my_rsvp = my_rsvp
        self.post_process_context()

        html = frappe.get_template("templates/event_detail.html").render(self.context)
        html = self.add_csrf_token(html)
        return build_response(self.path, html, self.http_status_code or 200, self.headers)

    @staticmethod
    def _set_rsvp(event_name, employee, status):
        existing = frappe.db.get_value(
            "Event Participants",
            {"parent": event_name, "reference_doctype": "Employee", "reference_docname": employee},
            "name",
        )
        if existing:
            frappe.db.set_value("Event Participants", existing, "attending", status)
        else:
            doc = frappe.get_doc("Event", event_name)
            doc.append("event_participants", {
                "reference_doctype": "Employee",
                "reference_docname": employee,
                "attending": status,
            })
            doc.save(ignore_permissions=True)
        frappe.db.commit()
