export interface JournalEntry {
  date: string
  title: string
  body: string
  tags: { thumb: 'epmc' | 'sbm' | 'stbf'; label: string }
}

/**
 * Parses one journal entry's raw Markdown: a `---` front-matter block
 * (date, tag, label, title) followed by the body as plain text.
 *
 * Deliberately minimal — plain `key: value` lines, no YAML dependency —
 * since this file has no imports of its own and is loaded two different
 * ways: through Vite (`import.meta.glob` in `../journal.ts`) for the app,
 * and transpiled and run directly under plain Node (`scripts/build-feed.mjs`)
 * for the RSS feed, which can't rely on any bundler macro.
 */
export function parseJournalEntry(raw: string): JournalEntry {
  const match = raw.match(/^---\r?\n([\s\S]*?)\r?\n---\r?\n([\s\S]*)$/)
  if (!match) throw new Error('Journal entry is missing its --- front-matter block')
  const [, frontMatter, rest] = match

  const fields: Record<string, string> = {}
  for (const line of frontMatter.split(/\r?\n/)) {
    const i = line.indexOf(':')
    if (i === -1) continue
    fields[line.slice(0, i).trim()] = line.slice(i + 1).trim()
  }

  for (const key of ['date', 'title', 'tag', 'label']) {
    if (!fields[key]) throw new Error(`Journal entry missing front-matter field "${key}"`)
  }

  return {
    date: fields.date,
    title: fields.title,
    body: rest.trim(),
    tags: { thumb: fields.tag as JournalEntry['tags']['thumb'], label: fields.label },
  }
}
