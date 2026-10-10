// Writes dist/feed.xml (RSS 2.0) from src/data/journal/*.md. Runs at the end
// of `npm run build`; the app itself stays a plain client-rendered SPA.
//
// No new dependency: the data files are plain TypeScript/Markdown, so the
// TypeScript ones are transpiled in memory with the `typescript` package
// that is already a devDependency, then imported.
//
// The journal entries themselves are read straight off disk and parsed with
// journal/parseEntry.ts, rather than importing src/data/journal.ts, because
// that file uses Vite's `import.meta.glob` to load its Markdown files — a
// bundler macro this plain-Node script has no equivalent for.
// parseEntry.ts has no imports of its own, so it's safe to load with the
// same data-URL trick used for the other TS files below.
import { readFile, writeFile, mkdir, readdir } from 'node:fs/promises'
import { fileURLToPath } from 'node:url'
import { dirname, resolve } from 'node:path'
import ts from 'typescript'

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..')

async function loadTs(relPath) {
  const source = await readFile(resolve(root, relPath), 'utf8')
  const { outputText } = ts.transpileModule(source, {
    compilerOptions: { module: ts.ModuleKind.ESNext, target: ts.ScriptTarget.ES2022 },
  })
  return import('data:text/javascript;base64,' + Buffer.from(outputText).toString('base64'))
}

const { SITE_ORIGIN } = await loadTs('src/seo/site.ts')
const { parseJournalEntry } = await loadTs('src/data/journal/parseEntry.ts')

const journalDir = resolve(root, 'src/data/journal')
const journalFiles = (await readdir(journalDir)).filter((f) => f.endsWith('.md')).sort()
const journalEntries = await Promise.all(
  journalFiles.map(async (f) => parseJournalEntry(await readFile(resolve(journalDir, f), 'utf8')))
)

const esc = (s) =>
  String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;')

// Only entries with a real calendar date get a <pubDate> ("October 3, 2026").
// Vague ones ("July 2026", "Spring 2026") are left undated rather than
// guessed; pubDate is optional in RSS 2.0.
const FULL_DATE = /^[A-Z][a-z]+ \d{1,2}, \d{4}$/
function pubDate(label) {
  if (!FULL_DATE.test(label)) return null
  const d = new Date(`${label} 12:00:00 UTC`)
  return Number.isNaN(d.getTime()) ? null : d.toUTCString()
}

const slug = (s) => s.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '')

// Only the newest FEED_LIMIT entries are published. journalEntries is kept
// newest-first (the Journal page shows it in that order), and some entries
// have vague dates that can't be sorted, so the array order is the order used.
const FEED_LIMIT = 20
const feedEntries = journalEntries.slice(0, FEED_LIMIT)

const items = feedEntries
  .map((e) => {
    const date = pubDate(e.date)
    return [
      '    <item>',
      `      <title>${esc(e.title)}</title>`,
      `      <link>${SITE_ORIGIN}/journal</link>`,
      `      <guid isPermaLink="false">${esc(`${SITE_ORIGIN}/journal#${slug(e.date)}-${slug(e.title)}`)}</guid>`,
      ...(date ? [`      <pubDate>${date}</pubDate>`] : []),
      `      <category>${esc(e.tags.label)}</category>`,
      `      <description>${esc(e.body)}</description>`,
      '    </item>',
    ].join('\n')
  })
  .join('\n')

const xml = `<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>Rae ARK — Writing Journal</title>
    <link>${SITE_ORIGIN}/journal</link>
    <atom:link href="${SITE_ORIGIN}/feed.xml" rel="self" type="application/rss+xml" />
    <description>Not news. Just the process — the breaks, the doubts, the small wins — as it actually happens.</description>
    <language>en</language>
${items}
  </channel>
</rss>
`

const out = resolve(root, 'dist/feed.xml')
await mkdir(dirname(out), { recursive: true })
await writeFile(out, xml)
console.log(`feed.xml: ${feedEntries.length} of ${journalEntries.length} entries -> dist/feed.xml`)
