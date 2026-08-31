"""Theme-toggle persistence, wired through `Site.raw_postprocess(...)`.

Supersedes the old `scripts/build.py` + `scripts/theme_persist_backend.py`
pair. That approach existed because, as of the `v0.048` alpha checkout,
the `arklight` CLI had no flag to attach an extra `Backend` to a build
(`_cmd_build` always calls `build()` with `backends=None`), so reaching
the compiler's `Backend.postprocess` extension point at all meant
calling `arklight.compiler.pipeline.build()` directly instead of going
through the CLI -- a whole parallel entrypoint script just to run one
extra transform over the rendered HTML.

The alpha branch has since grown the proper hook for exactly this:
`Site.raw_postprocess(fn)` (see ARKlight's CHANGELOG, "`Site.raw_
postprocess(...)`: user-facing raw output escape hatch"). It's the
user-facing equivalent of `Backend.postprocess()` -- same shape, same
"runs over the combined output of every backend, after every render()"
contract -- but registered directly on `Site` in `site.py`, so the
plain `arklight build site.py -o ARK` CLI command is enough again. See
`site.py` for the registration (`site.raw_postprocess(inject)`).

It's gated as an ARKlight *experimental* feature (unchecked write
access to every output file, unlike the rest of the validated
pipeline), so a normal build now prints ARKlight's standard
`[EXPERIMENTAL FEATURE ACTIVE]` banner -- expected, not an error.

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

(ARKlight's design doc tracks a future `State(persist=True)` -- see
the compiler's own Stage 8 note in `arklight/backend/android/
runtime.py` -- as the eventual first-class fix. Not implemented on
this alpha checkout, so this module remains the workaround until it
lands, at which point `pages/*.py`'s `State("theme", False)` calls can
switch to `State("theme", False, persist=True)` and this whole file
can go away.)

ARKlight also has no site-author hook to inject a `<script>` into
`<head>`/`<body>` from `Page(...)`/component code (no `Script` node,
no head-injection kwarg, as of this alpha checkout), so this can't be
fixed from `site.py`/`pages/*.py` alone -- it has to happen as a
transform over already-rendered HTML. `raw_postprocess` is exactly
that extension point.

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

2. Right before `</body>`: a `MutationObserver` watching
   `.page-shell`'s `class` attribute, writing the new theme to
   `localStorage` every time it changes, PLUS a direct `click`
   listener on the toggle button itself as a second, independent path
   to the same write (belt-and-suspenders -- see "Why two listeners"
   below). Note this script tag is placed textually *after*
   `<script src="arklight.js" defer>`, but because `defer` scripts
   only run once parsing finishes (right before `DOMContentLoaded`)
   while this inline script runs immediately, in place, during
   parsing, it actually executes *before* `arklight.js` does, not
   after. That ordering doesn't matter for correctness here: a
   `MutationObserver` only needs to be `observe()`d before a mutation
   happens, and `.page-shell` already exists in the DOM by the time
   this script runs (it's a fixed script src, meaning `.page-shell` --
   which is standard content -- is already parsed).

Why two listeners
------------------
`.page-shell`'s `class` attribute is driven entirely by
`renderClassBindings()` (see ARKlight's
`arklight/backend/js/runtime/bindings.py`), which does a plain
`el.classList.toggle(...)` -- an in-place mutation on the exact node
this script already holds a reference to, confirmed against a real
build via a `jsdom` harness (click -> persist -> fresh page load,
across 5 pages, in a loop). The `MutationObserver` alone is
sufficient and was the only listener here for a while. The `click`
listener is added as a second, independent path to the same
`persist()` write -- it doesn't change *what* gets written, just adds
a second trigger for it, so a future ARKlight internal refactor that
changes *how* the class gets updated (a different DOM API, a batched/
scheduled update, a class rename) can't silently break persistence by
breaking the thing this script happens to be watching. Both paths call
the same idempotent `persist()`, so this never double-applies anything
odd -- worst case is one redundant, identical `localStorage.setItem`.

Diagnosing "it isn't persisting"
----------------------------------
If a rebuild-and-verify (see `tests/test_theme_persist.py`) confirms
the injected script is correct but a live/deployed site still doesn't
carry theme across pages, that is a deployment/browser issue, not a
bug in this file's logic, and re-editing this script won't fix it. Two
known causes:

- **`file://` URLs.** Opening built `.html` files directly (double-
  click / drag into a browser) instead of via `http://`/`https://`
  puts each file in an isolated storage origin in some browsers, so
  `localStorage` doesn't carry across them at all -- even a perfect
  persistence script can't work around this, since it's the browser's
  security model, not application code. Serve over `http://` (a local
  static server, `arklight live-streaming`, etc.) to test this
  properly.
- **Stale cached pages**, especially on a CDN edge (e.g. Cloudflare
  Workers/Pages, see `README.md`'s deploy section) -- a page cached
  from before this was wired in (or from before a later fix to it) can
  sit alongside freshly-rebuilt pages and look exactly like "some
  pages have it, some don't" even though every page in the *current*
  build is identical. Hard-refresh, test in an incognito window,
  and/or purge the CDN cache after deploying a rebuild.

`persist()`'s own failures (private-browsing storage limits, quota,
etc.) are logged via `console.warn` rather than swallowed silently --
see `PERSIST_FAILURE_WARNING` below -- specifically so this is easy to
tell apart from the two causes above: open devtools on the page in
question and see whether a warning fires when you toggle the theme.
"""

from __future__ import annotations

import re

MARKER = "<!-- theme_persist -->"

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
        // over to the next one. Surfaced via console.warn (rather
        // than swallowed) so this is distinguishable, in devtools,
        // from the file:// / stale-cache causes documented in this
        // module's docstring -- if this warning is NOT firing when
        // you toggle the theme, persist() is working and the problem
        // is elsewhere (origin/caching), not in this script.
        if (window.console && console.warn) {{
          console.warn("[theme_persist] localStorage.setItem failed:", err);
        }}
      }}
    }};
    // Primary trigger: watch the class ARKlight itself drives.
    new MutationObserver(persist).observe(shell, {{
      attributes: true,
      attributeFilter: ["class"],
    }});
    // Secondary, independent trigger: the toggle click itself. Reads
    // the class shortly after the click (a macrotask later, so
    // ARKlight's own click handler -- which flips the class
    // synchronously -- has already run) rather than assuming
    // anything about *how* the class got flipped. See "Why two
    // listeners" in this module's docstring.
    document.addEventListener("click", function (ev) {{
      if (ev.target.closest('[data-ark-action-state="theme"]')) {{
        setTimeout(persist, 0);
      }}
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

    Pure string -> string, deliberately: `site.raw_postprocess` below
    is the only caller in the normal build, but keeping this as a
    standalone function (rather than inlining it into the callback)
    makes it trivial to unit test without running a full ARKlight
    build.
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


def apply_theme_persist(output_files: dict[str, str]) -> dict[str, str]:
    """`Site.raw_postprocess`-shaped callable: `(files) -> files`.

    Registered in `site.py` via `site.raw_postprocess(apply_theme_persist)`.
    Runs `inject()` over every `.html` file in the combined build
    output, leaving non-HTML files (CSS, JS, assets) untouched.
    """
    patched = dict(output_files)
    for path, contents in output_files.items():
        if not path.endswith(".html"):
            continue
        result = inject(contents)
        if result is not None:
            patched[path] = result
    return patched
