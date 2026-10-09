# 0004 — About page text sits on the hero divider

- **Status:** Implemented — see [changelog](../implementation/changelog.md)
- **Type:** Bug

## Symptom

On the About page the first paragraph ("I write character-driven fantasy
and...") starts directly under the hero's bottom rule with no breathing
room, unlike the space at the bottom of the page. It looks cramped.

## Cause

The section after the hero had `padding-top: 0` set inline. The hero draws a
border along its bottom edge, so the text touched it. Feedback, Journal,
Privacy and Terms had the same inline rule.

## Change

A shared `section.page-body` class (48px top padding) replaces the inline
zero, with `tight` (36px), `snug` (24px) and `flush` (0) modifiers where a
page needs different spacing. All five affected pages use it.
