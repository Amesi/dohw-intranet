# Spike: does Frappe's cross-app template override work against Wiki's page_renderer?

Spike for [wayfinder ticket #28](https://github.com/Amesi/dohw-intranet/issues/28), part of the [UI/UX Revamp map](https://github.com/Amesi/dohw-intranet/issues/14). Follows on from [#16's Wiki theming research](./frappe-wiki-theming.md), which flagged this as an open question requiring source-level tracing rather than static reading.

**Method:** cloned both `https://github.com/frappe/frappe` and `https://github.com/frappe/wiki` (shallow, latest `main`) and traced the exact call path from Wiki's custom page renderer through to Frappe's template loader — not inference, not docs, the actual function bodies.

## The trace

1. **Wiki's renderer calls the same shared `render_template` as everything else.** `wiki/frappe_wiki/doctype/wiki_document/wiki_document.py:716`, inside `WikiDocumentRenderer`:
   ```python
   html = frappe.render_template("templates/wiki/document.html", context)
   ```
   This is a plain path string passed to Frappe core's `frappe.render_template` — nothing wiki-specific about the call.

2. **`frappe.render_template` for a path always routes through the one global Jinja environment.** `frappe/utils/jinja.py`: for a path, `render_template` → `get_template(path)` → `get_jenv()` → `_get_jenv()` (site-cached singleton) → `FrappeSandboxedEnvironment(loader=get_jloader(), ...)`. There is no branch anywhere in this path that depends on which renderer or dispatch mechanism initiated the call — a custom `page_renderer` and the standard web-page dispatch both end up at the exact same environment/loader.

3. **The loader searches every installed app, later-installed apps first.** `frappe/utils/jinja.py:186-205`, `_get_jloader()`:
   ```python
   apps = list(reversed(frappe.get_active_apps(_ensure_on_bench=True)))
   if "frappe" not in apps:
       apps.append("frappe")
   jloader = ChoiceLoader(
       [PrefixLoader({app: PackageLoader(app, ".") for app in apps})]
       + [PackageLoader(app, ".") for app in apps]
   )
   ```
   `get_active_apps()` returns apps in site-install order (frappe first). Reversing it means the **most recently installed app is searched first** — the code's own comment confirms the intent: *"frappe will be loaded last, so app templates will get precedence."* `ChoiceLoader` tries each sub-loader in order and returns the first match, so whichever app's `PackageLoader` comes first in the list wins for a given relative path.

4. **`dohw_intranet` is installed after `wiki`** (it consumes Wiki as a dependency), so `dohw_intranet`'s `PackageLoader` is searched *before* `wiki`'s for any matching path. A file at `dohw_intranet/templates/wiki/document.html` would be found first and used instead of Wiki's own `wiki/templates/wiki/document.html` — no forking, no monkey-patching, just placing a file at the matching relative path.

5. **This applies recursively to every included fragment, not just the top-level template.** Wiki's `layout.html` pulls in its chrome via plain path-based `{% include %}` tags — `templates/wiki/includes/header.html`, `includes/sidebar.html`, `includes/tabs.html`, `includes/search_modal.html`, `includes/mobile_header.html` (`wiki/templates/wiki/layout.html:71-88`). Jinja's `{% include %}` resolves through the same environment/loader as the top-level render, so **each of these chrome pieces is independently overridable** by placing a same-path file in `dohw_intranet` — you don't have to override the whole `layout.html` monolithically; header/sidebar/tabs/search-modal can each be swapped individually if that's more convenient.

## Direct answer

**Yes — cross-app template override works against Wiki's custom `page_renderer`.** The renderer's use of `frappe.render_template()` is not a special or isolated code path; it's the same shared, app-order-aware Jinja loader used everywhere in Frappe. `dohw_intranet` can override `templates/wiki/layout.html`, `document.html`, and any of the `includes/*.html` chrome fragments individually, by placing files at the identical relative paths in its own package.

This **upgrades #23's (Wiki page layout) options** beyond what #16 could confirm: full chrome-level restructuring (sidebar, header, tabs, search modal — not just color/typography via `Wiki Settings.head_html`) is achievable through standard template overriding, no forking of the wiki app required. #23 is not limited to a themed-config spec after all.

## What this doesn't cover

- Whether `dohw_intranet`'s site install order is actually confirmed as *after* `wiki` in this specific deployment (near-certain given the dependency direction, but not independently re-verified against this site's actual `installed_apps` list — a one-line `bench --site erpnext.kumi-tech.com list-apps` check would confirm, but doesn't change the mechanism itself)
- Whether overriding `document.html`/`layout.html` wholesale versus overriding individual `includes/*.html` fragments is the better implementation approach — that's a decision for whoever builds #23, not this spike

## Sources

- `https://github.com/frappe/frappe` (cloned, `main`) — `frappe/utils/jinja.py` (`render_template`, `get_jenv`, `_get_jenv`, `get_jloader`, `_get_jloader`), `frappe/apps.py` (`get_active_apps`)
- `https://github.com/frappe/wiki` (cloned, `main`) — `wiki/hooks.py` (`page_renderer` registration), `wiki/frappe_wiki/doctype/wiki_document/wiki_document.py:716` (`WikiDocumentRenderer`'s `render_template` call), `wiki/templates/wiki/layout.html:71-88` (chrome `{% include %}` paths)
