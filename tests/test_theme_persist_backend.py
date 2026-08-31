"""Unit tests for `scripts/theme_persist_backend.py`.

`inject()` is a pure string -> string function (see its own docstring
for why), so these exercise it directly against small synthetic HTML
fragments rather than running a full ARKlight build.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from theme_persist_backend import MARKER, STORAGE_KEY, inject  # noqa: E402


def _page(body_attrs: str = ' data-ark-state="{&quot;theme&quot;: false}"') -> str:
    return (
        "<!doctype html><html><head></head>"
        f"<body{body_attrs}>"
        '<div class="page-shell"><p>hi</p></div>'
        '<script src="arklight.js" defer></script>'
        "</body></html>"
    )


def test_inject_is_noop_without_data_ark_state():
    html = "<!doctype html><html><body><p>no state here</p></body></html>"
    assert inject(html) is None


def test_inject_is_idempotent():
    once = inject(_page())
    assert once is not None
    assert inject(once) is None  # MARKER already present -> no-op


def test_inject_adds_pre_init_script_right_after_body_tag():
    result = inject(_page())
    assert result is not None
    assert MARKER in result
    # Marker (and the pre-init script) must land right after <body ...>,
    # before the page's own content, not appended at the end.
    assert result.index(MARKER) < result.index('class="page-shell"')


def test_inject_adds_post_runtime_script_before_closing_body():
    result = inject(_page())
    assert result is not None
    assert "MutationObserver" in result
    assert result.index("MutationObserver") > result.index('class="page-shell"')
    assert result.rindex("</script>") < result.rindex("</body>")


def test_inject_storage_key_used_consistently():
    result = inject(_page())
    assert result is not None
    # Read (pre-init) + the single shared persist() write -- both the
    # MutationObserver callback and the click-listener path call the
    # same persist() function, so this is 2, not 3.
    assert result.count(f'"{STORAGE_KEY}"') == 2


def test_inject_includes_redundant_click_listener_path():
    # Regression: persistence must not depend solely on observing
    # `.page-shell`'s class -- a direct click listener on the toggle
    # is a second, independent trigger to the same persist() write.
    result = inject(_page())
    assert result is not None
    assert 'data-ark-action-state="theme"' in result
    assert 'addEventListener("click"' in result


def test_inject_warns_on_localstorage_failure_instead_of_swallowing():
    result = inject(_page())
    assert result is not None
    assert "console.warn" in result


def test_inject_handles_no_closing_body_tag_gracefully():
    # No </body> at all -- pre-init script should still be added, and
    # inject() should not raise.
    html = (
        "<!doctype html><html>"
        '<body data-ark-state="{&quot;theme&quot;: false}">'
        '<div class="page-shell"></div>'
    )
    result = inject(html)
    assert result is not None
    assert MARKER in result
