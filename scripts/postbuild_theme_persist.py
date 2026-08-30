#!/usr/bin/env python3
"""Post-build step: make the theme toggle persist across page loads.

Why this exists
----------------
ARKfolio's site is a static multi-page build (`arklight build`) -- every
nav link is a real page load, not an SPA route. ARKlight's `State(...)`/
`Bind`/`Action.toggle_bool` reactivity is *page-scoped*: each page bakes
its initial state into a `data-ark-state="{...}"` JSON attribute on
`<body>` at build time, and `initState()` (see ARKlight's
`arklight/backend/js/runtime/state.py`) only ever reads that attribute.
There's no localStorage/cookie sync anywhere in the framework, so every
page you land on starts from whatever `State("theme", False)` was
declared as in `pages/*.py` -- always light -- regardless of what the
visitor last picked. That's the whole bug: it isn't a broken toggle,
it's a toggle with nowhere to remember its value between page loads.

ARKlight also has no site-author hook to inject a `<script>` into
`<head>`/`<body>` (no `Script` node, no head-injection kwarg on
`Page(...)` as of this alpha checkout), so this can't be fixed from
`site.py`/`pages/*.py` alone. This script instead patches the *compiled
HTML output* after `arklight build` runs, injecting two small vanilla
`<script>` tags per page:

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

Usage
-----
    arklight build site.py --out _build
    python scripts/postbuild_theme_persist.py _build

Idempotent: safe to re-run against the same output directory (it
checks for its own marker comment before injecting).
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

MARKER = "<!-- postbuild_theme_persist -->"

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
    """Return patched HTML, or None if already patched / no <body> match."""
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


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(f"usage: {argv[0]} <build-output-dir>", file=sys.stderr)
        return 2

    out_dir = Path(argv[1])
    if not out_dir.is_dir():
        print(f"error: {out_dir} is not a directory", file=sys.stderr)
        return 2

    patched = 0
    skipped = 0
    for html_path in sorted(out_dir.glob("*.html")):
        original = html_path.read_text(encoding="utf-8")
        result = inject(original)
        if result is None:
            skipped += 1
            continue
        html_path.write_text(result, encoding="utf-8")
        patched += 1
        print(f"  patched {html_path}")

    print(f"Theme persistence: patched {patched} file(s), skipped {skipped}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
