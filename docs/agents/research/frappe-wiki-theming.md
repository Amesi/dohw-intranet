# Frappe Wiki 3.0 — theming & customization surface

Research for [#16](https://github.com/Amesi/dohw-intranet/issues/16), part of the [UI/UX Revamp map](https://github.com/Amesi/dohw-intranet/issues/14). Feeds [#23](https://github.com/Amesi/dohw-intranet/issues/23) (Wiki page layout revamp).

**Method:** cloned the primary source, `https://github.com/frappe/wiki`, at commit `5dee77d415f227664128f10e9ef721a3261f310e` (2026-08-05), and read the actual template/CSS/hooks source directly — not docs or blog posts. No Frappe bench / vendored copy of the app exists on this machine (only an unrelated Obsidian-style reference note at `/opt/vault/Frappe/Apps/Frappe_Wiki/Frappe_Wiki.md`, which is a secondary AI-generated summary describing an older architecture — see "Note on a stale local reference" at the end). All claims below are cited against the cloned repo unless flagged "inferred."

## 1. Architecture: two rendering surfaces, not one

Wiki 3.0 is **not** a single themeable page — it's two separate UIs sharing a Frappe backend:

1. **The public reader** (`/<space-route>/<page-route>`) — server-rendered Jinja/HTML (`wiki/templates/wiki/*.html`), styled by a Tailwind v4 pipeline compiled to `wiki/public/css/main.css`. This is what `/wiki` shows to a browsing/reading staff member. **This is the surface that matters for issue #23** — it's what a "Document Library page" visually is.
2. **The editor/contribution app** — a Vue 3 SPA under `frontend/src/` (editor, space settings, contribution review, GitHub sync UI), built with `frappe-ui` (Frappe's Vue component/design-token library) and Tailwind v3. This only appears once a user starts editing or managing a space.

Both pull their design tokens from the same source (frappe-ui's Figma-synced token JSON), so they're visually consistent with each other, but they're two different build pipelines with different override mechanics. Source: `wiki/templates/wiki/layout.html`, `frontend/tailwind.config.js`, `wiki/public/css/main.css` (top-of-file `@import` chain), `scripts/generate-public-theme.mjs` header comment.

## 2. The public reader's CSS is a closed, generated pipeline

`wiki/public/css/main.css` imports, in order: `tailwindcss`, `./font.css`, `./frappe-ui-tokens.css`, `./theme.css`, `./frappe-ui-prose.css`, `./frappe-ui-code.css`. (Source: `wiki/public/css/main.css:1-14`.)

- `frappe-ui-tokens.css`, `frappe-ui-prose.css`, `frappe-ui-code.css` are **generated files** (gitignored, rebuilt from `frontend/node_modules/frappe-ui`'s token JSON by `scripts/generate-public-theme.mjs` / `generate-public-prose.mjs`). Their explicit purpose, per the script's own header comment, is to keep the reader's tokens byte-identical to the SPA editor's — "upgrade frappe-ui, rebuild, done." (Source: `scripts/generate-public-theme.mjs:1-18`.)
- `theme.css` is the one hand-authored file, and it explicitly disclaims being a place to change colors: *"Design tokens (colors, radius, shadows, typography) are NOT defined here — they are generated from frappe-ui's token source."* (Source: `wiki/public/css/theme.css:1-3`.) It only carries spacing/breakpoint extensions and form-control base styles.

**Conclusion: there is no config field, settings panel, or app-facing hook in Wiki itself that changes its color palette, radii, shadows, or typography scale.** Those come from `frappe-ui`'s own design tokens, compiled at build time. A consuming app cannot influence this pipeline without forking/patching the wiki app's build scripts.

## 3. But the tokens are CSS custom properties — which is the actual override seam

`generate-public-theme.mjs` emits the semantic tokens as plain CSS custom properties on `:root` (light) and `[data-theme="dark"]` (dark) — e.g. `--surface-base`, `--surface-gray-1..4`, `--ink-gray-3..9`, `--outline-gray-1..4`, plus color-family variants (`--surface-blue-2`, `--ink-red-3`, `--surface-amber-2`, etc.). Confirmed by reading the generator's `semanticVars()`/`paletteVars()` functions (`scripts/generate-public-theme.mjs:56-77`) and by grepping actual variable usage across the reader's CSS/templates — 38 distinct `var(--...)` tokens in use (`wiki/public/css/main.css`, `wiki/templates/wiki/`).

Every template and stylesheet in the reader references these by variable name, not hardcoded hex — e.g. `layout.html`'s `<body class="... bg-[var(--surface-base)] text-[var(--ink-gray-9)] ...">`, `document.html`'s `class="text-4xl-semibold text-[var(--ink-gray-9)]"`. Because they're inherited custom properties on `:root`/`html`, **any CSS declared later in the cascade that redefines the same variable names on `:root` (or `html[data-theme=...]`) will override them site-wide**, with no build changes to the wiki app itself. This is standard CSS cascade behavior, not a documented Wiki feature — but it works because Wiki's own authors chose a token-based architecture throughout.

Practical implication for a DoWH Gold (#FFBF00) / dark (#1A1A1A) rebrand: you would not swap in one "--accent" variable. Grepping for the one hardcoded brand-adjacent color (blue) in the reader's rendered-content CSS shows it's confined to two narrow semantic uses — the "note" callout background/icon color (`--surface-blue-2`, `--ink-blue-3`) and a checkbox tint — not a global interactive/primary color (`wiki/public/css/main.css:349-353`, `frontend/src/wiki-rendered.css:110-113`). Full-surface rebranding means overriding the whole `--surface-*` / `--ink-*` / `--outline-*` families, not one token.

## 4. The concrete, actually-wired injection point: `Wiki Settings.head_html`

The `Wiki Settings` singleton DocType has a `head_html` (Code/HTML) field, described in its own schema as *"Will be included in all public Wiki pages."* (Source: `wiki/wiki/doctype/wiki_settings/wiki_settings.json`, field `head_html`.) It's rendered as the **last** thing in `<head>`, after the reader's own `tailwind.css` link:

```html
<!-- wiki/templates/wiki/layout.html -->
<link rel="stylesheet" href="/assets/wiki/css/tailwind.css?v={{get_tailwindcss_hash()}}">
...
{% block head %} {% endblock %}
{{ head_html or "" }}
```

Because it renders after the compiled stylesheet, a `<style>` block placed here redefining `--surface-base`, `--ink-gray-9`, etc. on `:root`/`[data-theme="dark"]` wins the cascade. **This is the one real, currently-functional theming hook Wiki exposes**, and it's global (site-wide across all Wiki Spaces, not per-space).

A companion `javascript` field exists on the same DocType but a 2026-06-29 spec document in the Wiki repo explicitly flags it as dead: *"Deliberately not surfaced... `javascript` (only `head_html` is actually injected, via `wiki_document.py` → `templates/wiki/layout.html`)."* (Source: `specs/frontend_global_wiki_settings.md`, "Fields to surface" section — this is the Wiki maintainers' own design doc, high-confidence primary source.) Do not rely on `Wiki Settings.javascript`; it is unused.

## 5. dohw_intranet's existing `web_include_css` hook does NOT reach /wiki

`dohw_intranet/hooks.py` currently sets `web_include_css = "/assets/dohw_intranet/css/dohw_intranet.css"`, described as "loaded on all website pages" (source: `/root/dohw-intranet/hooks.py`). **This does not apply to `/wiki` pages.** `wiki/templates/wiki/layout.html` is a fully self-contained `<!DOCTYPE html>` template — it does not `{% extends %}` Frappe's standard web base template, and nowhere in it (or in `wiki/hooks.py`) is `web_include_css`/`web_include_js` consumed. In fact `wiki/hooks.py` itself carries those hook keys only as **commented-out boilerplate** from the Frappe app scaffold template, never activated:

```python
# include js, css files in header of web template
# web_include_css = "/assets/wiki/css/wiki.css"
# web_include_js = "/assets/wiki/js/wiki.js"
```
(Source: `wiki/hooks.py`.) The only two content injection points the reader's template pulls in are the shared `templates/includes/meta_block.html` (Frappe core, meta tags only) and `Wiki Settings.head_html` (section 4 above).

**This means the DoWH revamp cannot reuse the existing sitewide CSS hook for /wiki** — a separate injection path is needed (most directly: `head_html`, or see section 6/7 for app-level alternatives).

## 6. Per-space branding fields — real, but deliberately narrow

`Wiki Space` (the doctype for a wiki instance/section) exposes real per-space appearance fields, confirmed in its schema (`wiki/wiki/doctype/wiki_space/wiki_space.json`):

- `light_mode_logo`, `dark_mode_logo` — Attach Image, shown in the sidebar/header logo slot.
- `app_switcher_logo`, `favicon` — Attach Image.
- `navbar_items` — a child table of `Top Bar Item` records (Frappe core doctype, reused here), for a custom navbar-items list per space.
- `enable_tabs`, `home_tab_title`, `home_tab_icon` — v3's horizontal tab-bar feature (labels/icon only, not styling).
- `wiki_config` — a read-only, auto-generated JSON field (`.wiki.json`) — not an admin-editable theming config; appears to be sync/export metadata, not a customization surface (unverified further; out of scope here).

The 2026-06-29 Wiki maintainers' spec is explicit about the design intent here: when they brought global `Wiki Settings` into the frontend UI, they scoped it deliberately — *"no new appearance/design fields (logos/favicon/navbar stay per-space, by design)"* (`specs/frontend_global_wiki_settings.md`, Scope section). So logo/navbar customization is a first-class, supported feature — but it's swap-an-image / relabel-a-tab level, not layout or chrome restructuring.

## 7. Page chrome (nav, sidebar, header) is baked into Wiki's own templates

The reader's chrome — top navbar (`wiki/templates/wiki/includes/header.html`), mobile header (`includes/mobile_header.html`), sidebar tree (`includes/sidebar.html`, `macros/sidebar_tree.html`), tab bar (`includes/tabs.html`), TOC (`includes/toc.html`), search modal (`includes/search_modal.html`) — are all Wiki's own Jinja includes, wired into one fixed layout in `layout.html`. There is no hook, config flag, or slot system to swap these for custom markup; the only structural toggle is `hide_chrome` (a boolean the renderer can set per-document to strip all chrome down to a bare title + content, used today for "orphan documents" — see `document.html`'s `{% if hide_chrome %}` branch). That's a binary "chrome or no chrome" switch, not a way to inject a frappe.io-style nav.

**Template overriding (inferred, not verified in this session):** standard Frappe framework behavior lets a later-installed app's template at the same relative path (e.g. `dohw_intranet/templates/wiki/layout.html`) shadow another app's template in Frappe's Jinja loader search order. If true here, this would be the way to genuinely restructure the chrome. I did not have a Frappe framework checkout available to confirm this holds for Wiki's custom `page_renderer`-based rendering path (`wiki/hooks.py`'s `page_renderer = [...WikiDocumentRenderer]`, which calls `frappe.render_template` directly rather than going through the standard web-page dispatch) — this needs a real spike (install both apps in a bench, drop a same-path override file, confirm it wins) before being relied on for #23's design. Flag this explicitly to whoever picks up #23.

## Direct answer

**/wiki can be meaningfully re-colored (light/dark palette, brand colors, spacing/typography tokens) but not meaningfully re-componentized.** Concretely:

- **In reach today, with a documented/wired hook:** global color rebrand via CSS custom-property overrides injected through `Wiki Settings.head_html` — redefine `--surface-*`, `--ink-*`, `--outline-*` (and friends) on `:root` / `[data-theme="dark"]` to bring the palette to DoWH Gold/dark. Per-space logo, favicon, and navbar-item labels via `Wiki Space` fields. This gets you frappe.io-*feeling* colors and branding marks on top of Wiki's existing layout.
- **Not in reach without forking/patching the wiki app:** the actual chrome — sidebar structure, header layout, tab bar, search modal, page-action buttons — is hardcoded in Wiki's own Jinja templates with no slot/override API. A true frappe.io-style nav (the kind #14's map wants) is not achievable through Wiki's exposed surface alone.
- **Existing `dohw_intranet` sitewide CSS hook is a dead end here** — it doesn't reach `/wiki` at all; whatever revamp CSS gets built needs its own delivery path (most direct: `head_html`).
- **Open question requiring a spike, not covered by static reading:** whether Frappe's standard cross-app template-override mechanism works against Wiki's custom `page_renderer` dispatch. If it does, layout-level restructuring becomes possible without forking the wiki app; if not, #23 is likely limited to a "themed-config spec" (color/typography/branding only) rather than a true clickable prototype of new chrome, per the framing already anticipated in #23 itself.

## Note on a stale local reference

`/opt/vault/Frappe/Apps/Frappe_Wiki/Frappe_Wiki.md` is a local Obsidian-style note (dated 2026-07-15, citing "v3.0.0-rc.5, June 2026") describing Wiki as a `Wiki Page`/`Wiki Space`/`Wiki Page Revision`/`Wiki Page Patch` DocType model with an Ace-editor-based UI. That data model does not match the actual cloned source at all (current source uses `Wiki Document`, `Wiki Change Request`, `Wiki Revision`, a Vue/Tiptap-based editor, GitHub sync, SQLite/RediSearch search variants, etc.) — it appears to describe a materially older or hypothetical version of the app, or is simply an inaccurate secondary summary. Its section 10 ("Customisation Patterns," e.g. generic `web_include_css`/`web_include_js` hooks.py advice) is **not corroborated by the actual source** — section 5 of this document shows those specific hook keys are dead/commented-out boilerplate in the real `wiki/hooks.py`, and don't apply to Wiki's custom-rendered pages regardless. Treat that vault note as unreliable for this ticket; this document supersedes it.

## Sources

- `https://github.com/frappe/wiki` @ `5dee77d415f227664128f10e9ef721a3261f310e` (cloned and read directly)
  - `wiki/hooks.py`
  - `wiki/templates/wiki/layout.html`, `document.html`, `includes/header.html`, `includes/sidebar.html`
  - `wiki/public/css/main.css`, `theme.css`
  - `wiki/wiki/doctype/wiki_settings/wiki_settings.json`
  - `wiki/wiki/doctype/wiki_space/wiki_space.json`
  - `scripts/generate-public-theme.mjs`
  - `specs/frontend_global_wiki_settings.md`
  - `specs/public_reader_prose_v3.md`
  - `frontend/tailwind.config.js`, `frontend/src/index.css`, `frontend/src/composables/useTheme.js`
- `/root/dohw-intranet/hooks.py`, `/root/dohw-intranet/README.md` (this repo, for current integration state)
- `/opt/vault/Frappe/Apps/Frappe_Wiki/Frappe_Wiki.md` (local secondary note — flagged above as unreliable/outdated, not used as an evidentiary source for any claim in this document)
