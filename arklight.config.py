# include <stdlib.ARKlight>

# `pages/journal.py` links to "/feed.xml", a root-level file that
# `scripts/build_feed.py` writes into the build directory as a second
# pass after `arklight build` (see scripts/build.sh) -- ARKlight itself
# has no page or asset for it, so without this the link check halts the
# build on an href naming no registered page. This is exactly the
# narrow, server-might-supply-it-at-build-time case `overdrive` exists
# for (see docs/Foundational/CLI-REFERENCE.md's Overdrive section), not
# a general way to silence link-check errors -- every other internal
# link/asset in this project still resolves and stays checked.
CONFIG = {
    "overdrive": True,
}
