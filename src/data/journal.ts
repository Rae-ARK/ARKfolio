import { parseJournalEntry, type JournalEntry } from './journal/parseEntry'

export type { JournalEntry }

// One Markdown file per entry in ./journal/, each starting with a small
// front-matter block (date, tag, label, title) followed by the body as
// plain text — see journal/parseEntry.ts. Filenames use a zero-padded
// numeric prefix (001 = newest) so the default sort order is the display
// order without having to parse the entries' own date strings, several of
// which are vague ("Spring 2026", "Early 2026", "2025 – 2026").
//
// `eager: true` + `query: '?raw', import: 'default'` inlines every entry's
// raw text at build time (no extra runtime fetches); `parseJournalEntry`
// turns each one into the same JournalEntry shape the pages already consume,
// so JournalPage.vue, HomePage.vue and scripts/build-feed.mjs need no changes
// beyond what this file already exported.
const modules = import.meta.glob('./journal/*.md', {
  query: '?raw',
  import: 'default',
  eager: true,
}) as Record<string, string>

/** Newest first. The RSS feed (scripts/build-feed.mjs) publishes only the first 20, in this order. */
export const journalEntries: JournalEntry[] = Object.keys(modules)
  .sort()
  .map((path) => parseJournalEntry(modules[path]))
