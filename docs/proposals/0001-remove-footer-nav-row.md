# 0001 — Remove the footer navigation row

- **Status:** Implemented — see [changelog](../implementation/changelog.md)
- **Relates to:** [UI/UX audit, finding 1](../implementation/ui-ux-audit.md#1-redundant-bottom-row-nav-in-the-footer)

## Problem

The navigation buttons in the footer's bottom row ruin the page's otherwise
decent appearance. They duplicate the header nav and add unrelated links
into one ungrouped row.

## Proposed change

The bottom-row navigation buttons in `AppFooter.vue` (`.footer-links`)
should not exist.

## Open questions

- That row is currently the only place that links to **Feedback**,
  **Privacy** and **Terms**; the header nav does not. The README notes the
  privacy page exists because the Play Store requires a privacy policy
  link. Removing the whole row would remove those entry points, so decide
  whether they move elsewhere or stay as a quiet legal line.
- X and GitHub are also available as icon buttons in the header.

## Outcome

Accepted and shipped. The nine-link row is gone. Because the footer was the
only entry point to Feedback, Privacy and Terms, those three stay as a small,
quiet line beside the copyright. Works, Store, Journal and About (duplicates
of the header) and the X and GitHub links (icon buttons in the header) were
removed.
