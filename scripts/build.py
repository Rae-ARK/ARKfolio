#!/usr/bin/env python3
"""ARKfolio's build entrypoint.

Replaces plain `arklight build site.py -o ARK` + a separate manual
`python scripts/postbuild_theme_persist.py ARK` step with a single
command. The `arklight` CLI has no flag to attach an extra `Backend`
to a build (`_cmd_build` in ARKlight's own `cli/main.py` always calls
`build()` with `backends=None`, i.e. `default_backends()` only), so
reaching the compiler's `Backend.postprocess` extension point at all
means calling `arklight.compiler.pipeline.build()` directly rather
than going through the CLI -- this script is that call, plus enough of
the CLI's own output formatting to be a drop-in replacement.

Usage
-----
    python scripts/build.py                  # -> ARK/index.html etc.
    python scripts/build.py -o dist           # custom output dir
    python scripts/build.py --no-open         # skip auto-opening the build
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from arklight.cli.main import open_in_browser  # noqa: E402
from arklight.compiler.pipeline import CompileError, build, default_backends  # noqa: E402
from theme_persist_backend import ThemePersistBackend  # noqa: E402

DEFAULT_ENTRY = "site.py"
DEFAULT_OUTPUT = "ARK"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("entry", nargs="?", default=DEFAULT_ENTRY, help=f"site entry file (default: {DEFAULT_ENTRY})")
    parser.add_argument("-o", "--output", default=DEFAULT_OUTPUT, help=f"output directory (default: {DEFAULT_OUTPUT})")
    parser.add_argument("--no-open", action="store_true", help="skip auto-opening the built site")
    args = parser.parse_args(argv)

    backends = [*default_backends(), ThemePersistBackend()]

    try:
        result = build(args.entry, args.output, backends=backends)
    except CompileError as exc:
        print(f"ARKfolio build failed: {exc}", file=sys.stderr)
        return 1

    print(f"ARKfolio built {len(result.written_paths)} file(s) -> {args.output}/ (theme persistence included)")
    for path in result.written_paths:
        print(f"  {path}")

    if not args.no_open:
        if open_in_browser(result, args.output):
            print("Opened in your default browser.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
