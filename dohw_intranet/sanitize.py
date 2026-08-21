"""Rich-text HTML sanitization for the TipTap editor content.

Uses nh3 (ammonia) directly because Frappe's
``frappe.utils.html_utils.clean_html`` is too restrictive for a full editor
(it strips headings, images, tables and blockquotes).

Safety notes (verified against nh3 in this bench):
  * relative ``/files/...`` image/link URLs are preserved (Frappe file URLs)
  * ``javascript:`` / ``data:`` URLs are stripped
  * ``<script>`` / ``<style>`` are removed
  * nh3 passes arbitrary CSS through when ``style`` is whitelisted, so we
    post-process ``style`` to keep ONLY ``text-align`` (from the toolbar's
    alignment control) and drop everything else.
"""

import re

import nh3

_TAGS = {
    "p", "br", "hr",
    "h1", "h2", "h3", "h4", "h5", "h6",
    "strong", "b", "em", "i", "u", "s", "strike",
    "ul", "ol", "li",
    "blockquote", "pre", "code",
    "a", "img",
    "table", "thead", "tbody", "tfoot", "tr", "th", "td",
    "div", "span",
}

_ATTRIBUTES = {
    "a": {"href", "title", "target"},
    "img": {"src", "alt", "title"},
    "th": {"colspan", "rowspan"},
    "td": {"colspan", "rowspan"},
    "p": {"style"},
    "h1": {"style"},
    "h2": {"style"},
    "h3": {"style"},
    "h4": {"style"},
    "div": {"style"},
}

_STYLE_ATTR_RE = re.compile(r'style="([^"]*)"')
_TEXT_ALIGN_RE = re.compile(r'(?:^|;)\s*text-align\s*:\s*(left|center|right|justify)\s*;?')


def _sanitize_style(match):
    align = _TEXT_ALIGN_RE.search(match.group(1))
    if align:
        return f'style="text-align: {align.group(1)}"'
    return ""


def sanitize_rich_html(html):
    if not html:
        return ""
    out = nh3.clean(
        html,
        tags=_TAGS,
        attributes=_ATTRIBUTES,
        link_rel="noopener noreferrer",
        strip_comments=True,
    )
    return _STYLE_ATTR_RE.sub(_sanitize_style, out)
