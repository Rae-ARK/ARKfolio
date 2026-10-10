import { storeBooks } from '@/data/store'
import { SITE_ORIGIN } from './site'

export type SchemaKind = 'person' | 'book'

const AUTHOR = {
  '@type': 'Person',
  name: 'Rae ARK',
  alternateName: '嵐久 怜',
  url: `${SITE_ORIGIN}/about`,
}

// JSON-LD is injected by the router (see router/index.ts). Google executes
// JavaScript, so this works in a client-rendered SPA; crawlers that don't
// run JS simply won't see it.
export function buildJsonLd(kind: SchemaKind): Record<string, unknown> | null {
  if (kind === 'person') {
    return {
      '@context': 'https://schema.org',
      ...AUTHOR,
      '@id': `${SITE_ORIGIN}/about#author`,
      jobTitle: 'Web novelist',
      image: `${SITE_ORIGIN}/assets/images/png/profile.png`,
      sameAs: ['https://x.com/Rae7866', 'https://www.youtube.com/@Rae0611'],
    }
  }

  const book = storeBooks.find((b) => b.isbn)
  if (!book) return null
  return {
    '@context': 'https://schema.org',
    '@type': 'Book',
    name: book.title,
    description: book.description,
    url: `${SITE_ORIGIN}/store`,
    image: encodeURI(`${SITE_ORIGIN}/assets/images/png/Summoned By Mistake, I Decided To Learn How To Live Arc 1.png`),
    isbn: book.isbn,
    bookFormat: 'https://schema.org/Paperback',
    inLanguage: 'en',
    datePublished: book.datePublished,
    author: AUTHOR,
    publisher: { '@type': 'Organization', name: 'Independently Published' },
  }
}
