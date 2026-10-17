#!/usr/bin/env python3
"""Writes <build-dir>/feed.xml (RSS 2.0) from content/journal.py, the same
newest-first JOURNAL_ENTRIES list the Journal page renders.

Python port of the original ARKfolio's scripts/build-feed.mjs: same
RSS 2.0 shape, same <pubDate>-only-for-a-full-calendar-date rule, same
FEED_LIMIT. Run after `arklight build` (see scripts/build.sh) since
ARKlight's build directory is the thing this writes into, and the site
has no ARKlight-native way to emit an extra non-page file like this yet.
"""

import re
import sys
from datetime import datetime, timezone
from email.utils import format_datetime
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from content.journal import JOURNAL_ENTRIES  # noqa: E402

# Keep in sync with the og:* tags / sitemap.xml / robots.txt, same as the
# original scripts/build-feed.mjs's SITE_ORIGIN comment.
SITE_ORIGIN = "https://rae-ark.horizonarkstudio.workers.dev"
FEED_LIMIT = 20

_FULL_DATE = re.compile(r"^[A-Z][a-z]+ \d{1,2}, \d{4}$")


def _pub_date(label: str):
    """Only a real calendar date ("October 3, 2026") gets a <pubDate>;
    vague ones ("July 2026") are left undated, same as the original."""
    if not _FULL_DATE.match(label):
        return None
    try:
        d = datetime.strptime(label, "%B %d, %Y").replace(
            hour=12, tzinfo=timezone.utc
        )
    except ValueError:
        return None
    return format_datetime(d, usegmt=True)


def _slug(s: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", s.lower())
    return s.strip("-")


def _item(entry: dict) -> str:
    date = _pub_date(entry["date"])
    guid = f"{SITE_ORIGIN}/journal#{_slug(entry['date'])}-{_slug(entry['title'])}"
    lines = [
        "    <item>",
        f"      <title>{escape(entry['title'])}</title>",
        f"      <link>{SITE_ORIGIN}/journal</link>",
        f'      <guid isPermaLink="false">{escape(guid)}</guid>',
    ]
    if date:
        lines.append(f"      <pubDate>{date}</pubDate>")
    lines.append(f"      <category>{escape(entry['tags']['label'])}</category>")
    lines.append(f"      <description>{escape(entry['body'])}</description>")
    lines.append("    </item>")
    return "\n".join(lines)


def build_feed_xml() -> str:
    feed_entries = JOURNAL_ENTRIES[:FEED_LIMIT]
    items = "\n".join(_item(e) for e in feed_entries)
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>Rae ARK \u2014 Writing Journal</title>
    <link>{SITE_ORIGIN}/journal</link>
    <atom:link href="{SITE_ORIGIN}/feed.xml" rel="self" type="application/rss+xml" />
    <description>Not news. Just the process \u2014 the breaks, the doubts, the small wins \u2014 as it actually happens.</description>
    <language>en</language>
{items}
  </channel>
</rss>
"""


def main():
    build_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "ARK"
    build_dir.mkdir(parents=True, exist_ok=True)
    out = build_dir / "feed.xml"
    xml = build_feed_xml()
    out.write_text(xml, encoding="utf-8")
    feed_entries = JOURNAL_ENTRIES[:FEED_LIMIT]
    print(f"feed.xml: {len(feed_entries)} of {len(JOURNAL_ENTRIES)} entries -> {out}")


if __name__ == "__main__":
    main()
