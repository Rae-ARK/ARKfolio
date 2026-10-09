# 0006 — Let readers say they're waiting for a paperback

- **Status:** Implemented — see [changelog](../implementation/changelog.md)
- **Relates to:** [UI/UX audit, finding 5](../implementation/ui-ux-audit.md)

## Problem

The Store says EPMC and STBF "aren't in print yet... they'll appear here
first", but gave readers no way to say they want them.

## Change

- The not-in-print note gets one button per series ("I'm waiting for EPMC →",
  "I'm waiting for STBF →"). Each links to `/feedback?subject=...`.
- The feedback form has two new subjects, "Waiting for the EPMC paperback"
  and "Waiting for the STBF paperback", and reads `?subject=` to pre-select
  one.
- Nothing is collected on the site: the reader's own email app sends the
  message, as with every other feedback subject.
