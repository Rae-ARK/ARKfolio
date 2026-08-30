"""ARKlight `Backend` that makes the theme toggle persist across page loads.

Supersedes `scripts/postbuild_theme_persist.py`: same fix, same injected
HTML, but wired in through the compiler's actual extension point
(`Backend.postprocess`, see `arklight/backend/base.py`) instead of a
second command a person has to remember to run by hand after
`arklight build`. See `scripts/build.py` for how this gets attached to
`default_backends()`.

Why the fix itself is needed
-----------------------------
ARKfolio's site is a static multi-page build -- every nav link is a
real page load, not an SPA route. ARKlight's `State(...)`/`Bind`/
`Action.toggle_bool` reactivity is *page-scoped*: each page bakes its
initial state into a `data-ark-state="{...}"` JSON attribute on
`<body>` at build time, and `initState()` (see ARKlight's
`arklight/backend/js/runtime/state.py`) only ever reads that
attribute. There's no localStorage/cookie sync anywhere in the
framework, so every page you land on starts from whatever
`State("theme", False)` was declared as in `pages/*.py` -- always
light -- regardless of what the visitor last picked. That's the whole
bug: it isn't a broken toggle, it's a toggle with nowhere to remember
its value between page loads.

ARKlight also has no site-author hook to inject a `<script>` into
`<head>`/`<body>` (no `Script` node, no head-injection kwarg on
`Page(...)` as of this alpha checkout), so this can't be fixed from
`site.py`/`pages/*.py` alone -- it has to happen as a transform over
already-rendered HTML. `Backend.postprocess` is exactly that
extension point: it runs as a second pass over the *combined* output
of every backend's `render()`, in the same in-process build, so there
is no separate command and no risk of shipping a build where the
patch step was silently skipped.

What gets injected, per HTML page
----------------------------------
1. Right after `<body ...>` (before anything else runs): reads
   `localStorage`, and if the visitor last chose dark mode, rewrites
   that page's `data-ark-state` attribute so it starts as
   `{"theme": true}` instead of the baked-in `{"theme": false}`.
   Because this runs *before* ARKlight's own `arklight.js` reads that
   attribute (`initState()` runs on `DOMContentLoaded`, later than
   this inline script), the page's in-memory state store and its
   visible `.dark` class end up agreeing from the start -- no desync,
   no need to reach into ARKlight's closed-over `arkStore`.

2. Right before `</body>` (after `arklight.js` has already run and
   wired up the toggle button): a `MutationObserver` watching
   `.page-shell`'s `class` attribute, writing the new theme to
   `localStorage` every time it changes. Watching the DOM class rather
   than hooking the button's click handler keeps this decoupled from
   ARKlight's internal event wiring -- it works no matter what state
   change caused the class to flip.
"""

from __future__ import annotations

import re

from arklight.backend.base import Backend
from arklight.ir.build import WebsiteIR

MARKER = "<!-- theme_persist_backend -->"

# Storage key. Namespaced so it can't collide with some other script's
# unrelated "theme" key if one ever gets added to this site.
STORAGE_KEY = "arkfolio-theme"

# Matches ARKlight's emitted body-state attribute, e.g.:
#   <body data-ark-state="{&quot;theme&quot;: false}">
# HTML-attribute-escaped, so the literal text contains &quot; not ".
BODY_STATE_RE = re.compile(
    r'(<body\b[^>]*\bdata-ark-state=")([^"]*)("[^>]*>)'
)

PRE_INIT_SCRIPT = f"""{MARKER}
<script>
(function () {{
  try {{
    var saved = localStorage.getItem("{STORAGE_KEY}");
    if (saved !== "dark") return;
    var body = document.body;
    var raw = body.getAttribute("data-ark-state");
    if (!raw) return;
    // The attribute value is HTML-attribute-escaped by the browser's
    // own parser by the time we read it here, so this is already the
    // real JSON text (e.g. {{"theme": false}}) -- no manual unescaping
    // needed.
    var state = JSON.parse(raw);
    state.theme = true;
    body.setAttribute("data-ark-state", JSON.stringify(state));
  }} catch (err) {{
    // Corrupt/unavailable localStorage or unexpected state shape --
    // fail open to the page's normal baked-in (light) default rather
    // than breaking the page.
  }}
}})();
</script>
"""

POST_RUNTIME_SCRIPT = f"""<script>
(function () {{
  try {{
    var shell = document.querySelector(".page-shell");
    if (!shell) return;
    var persist = function () {{
      var isDark = shell.classList.contains("dark");
      try {{
        localStorage.setItem("{STORAGE_KEY}", isDark ? "dark" : "light");
      }} catch (err) {{
        // localStorage unavailable (private browsing, quota, etc.) --
        // the toggle still works for this page, it just won't carry
        // over to the next one.
      }}
    }};
    new MutationObserver(persist).observe(shell, {{
      attributes: true,
      attributeFilter: ["class"],
    }});
  }} catch (err) {{
    // No .page-shell / no MutationObserver support -- leave the page
    // exactly as ARKlight rendered it.
  }}
}})();
</script>
"""


def inject(html: str) -> str | None:
    """Return patched HTML, or None if already patched / nothing to do.

    Pure string -> string, deliberately: `ThemePersistBackend.postprocess`
    below is the only caller in the normal build, but keeping this as a
    standalone function (rather than inlining it into the class) makes
    it trivial to unit test without constructing a `WebsiteIR` or
    running the full pipeline.
    """
    if MARKER in html:
        return None  # already patched, idempotent no-op

    match = BODY_STATE_RE.search(html)
    if not match:
        # Page has no data-ark-state (no State(...) declared) -- nothing
        # to sync, leave it untouched.
        return None

    insert_at = match.end()
    html = html[:insert_at] + "\n" + PRE_INIT_SCRIPT + html[insert_at:]

    body_close = html.rfind("</body>")
    if body_close == -1:
        return html  # pre-init script alone still helps; skip the rest
    html = html[:body_close] + POST_RUNTIME_SCRIPT + html[body_close:]

    return html


class ThemePersistBackend(Backend):
    """Adds theme-persistence `<script>` tags to every rendered HTML page.

    Contributes no files of its own (`render()` is a no-op) -- all the
    work happens in `postprocess()`, which runs after HTMLBackend has
    already rendered every page, per `Backend.postprocess`'s contract
    of seeing the *combined* output of every backend in `backends=[...]`.
    Attach it alongside the stock backends, e.g.:

        from arklight.compiler.pipeline import build, default_backends
        build(site_path, out_dir, backends=[*default_backends(), ThemePersistBackend()])

    See `scripts/build.py`, which does exactly this.
    """

    name = "theme-persist"

    def render(self, ir: WebsiteIR) -> dict[str, str]:  # noqa: ARG002
        return {}

    def postprocess(self, output_files: dict[str, str]) -> dict[str, str]:
        patched = dict(output_files)
        for path, contents in output_files.items():
            if not path.endswith(".html"):
                continue
            result = inject(contents)
            if result is not None:
                patched[path] = result
        return patched
