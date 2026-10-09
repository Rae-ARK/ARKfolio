# 0003 — Fix the cramped header just above the mobile breakpoint

- **Status:** Proposed
- **Type:** Bug

## Symptom

When the window is only a few pixels wider than the mobile view, the nav
bar does not collapse into the menu and the header looks cramped and bad.

The brand block, "Rae ARK" followed by a line break and
"嵐久 怜 · WEB NOVELIST", is not a single element in a div, so it does not
hold together as one unit when space gets tight.

## Likely cause (from reading the CSS; not yet reproduced in a browser)

- In `src/styles/main.css` the hamburger menu only takes over at
  `max-width: 700px` (and `.nav-toggle` is hidden from `min-width: 701px`).
- Just above 700px the full nav (five links plus the X / GitHub / theme icon
  group) still has to share one row with the brand, which is likely too
  wide.
- The brand is a flex column (`.brand`) holding the name link and
  `.sub` as separate elements inside `.brand-row`, and nothing stops them
  from wrapping or shrinking.

## Proposed direction

- Collapse the nav at a wider breakpoint than the current 700px.
- Keep the brand on one unit that does not wrap or shrink.
- Verify at widths from roughly 700px to 1000px.
