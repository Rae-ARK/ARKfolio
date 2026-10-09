# 0002 — Add a paperback card to "Where to Read" on the home page

- **Status:** Proposed

## Problem

The paperback/print edition is only discoverable through the Store page.
Readers on the home page have no pointer to it.

## Proposed change

Add a new card for the paperback/print edition that redirects to the store
page. It improves UX.

**Placement.** This was first suggested for the footer, then revised: the
card belongs on the home page, inside the existing **Where to Read**
section (the `.reads` group in `HomePage.vue`, alongside the Royal Road,
Scribble Hub and X cards). The footer placement is dropped.

**Target.** The card links to `/store`.

## Notes

- The section heading currently reads "Every chapter, free, wherever you
  already read". A paid print edition sits slightly outside that wording;
  consider whether the heading needs adjusting.
- Per [audit finding 2](../implementation/ui-ux-audit.md#2--external-link-arrows-on-internal-links),
  an internal link should not use the ↗ glyph.
