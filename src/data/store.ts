export interface Retailer {
  label: string
  url: string
  /** Shown under the buttons when the link isn't a plain product page. */
  note?: string
}

export interface StoreBook {
  workSlug: 'sbm'
  thumbClass: 'sbm'
  edition: string
  title: string
  description: string
  note: string
  retailers: Retailer[]
}

export const storeBooks: StoreBook[] = [
  {
    workSlug: 'sbm',
    thumbClass: 'sbm',
    edition: 'SBM · June 2026 Edition',
    title: 'Summoned by Mistake, I Decided to Learn How to Live',
    description:
      'Volume 1 — Unwanted Summoning / Of Names and New Beginnings (Arc 1–2). Lightly formatted paperback, limited run. Includes a QR code for a free PDF copy with purchase.',
    note: 'Published under Horizon ARK Studio · ISBN 979-8-1810-7869-7',
    retailers: [
      {
        label: 'Amazon',
        url: 'https://www.royalroad.com/amazon/B0H62KQV8D?maas=&ref=',
        note: 'Opens through a Royal Road redirect link on its way to the Amazon listing.',
      },
      { label: 'Walmart', url: 'https://www.walmart.com/ip/Summoned-by-Mistake-I-Decided-to-Learn-How-to-Live-Volume-1-Unwanted-Summoning-Of-Names-and-New-Beginnings-Arc-1-2-Paperback-9798181078697/20471956500' },
      { label: 'eBay (AU)', url: 'https://www.ebay.com.au/itm/137466978621' },
      { label: 'Saxo (DK)', url: 'https://www.saxo.com/dk/summoned-by-mistake-i-decided-to-learn-how-to-live_bog_9798181078697' },
      {
        label: 'Books-A-Million',
        url: 'https://www.booksamillion.com/search?query=Rae%20Ark&filters%5Bauthors%5D=Rae%20Ark&filters%5Bavailable_in_stores%5D=1',
        note: 'Opens an author search rather than a direct product page — use it to check in-store availability.',
      },
    ],
  },
]

export interface UpcomingPrint {
  slug: 'epmc' | 'stbf'
  shortTitle: string
  title: string
}

export const notYetInPrint: UpcomingPrint[] = [
  { slug: 'epmc', shortTitle: 'EPMC', title: 'Enigmatic Pathways Mystic Circuits' },
  { slug: 'stbf', shortTitle: 'STBF', title: 'The Shadow I Cast Over Two Beautiful Flowers' },
]

export const notYetInPrintNote =
  "Enigmatic Pathways Mystic Circuits and The Shadow I Cast Over Two Beautiful Flowers aren't in print yet. If that changes, they'll appear here first."

export const notYetInPrintCta =
  "Waiting on one of them? Tell me which — it opens an email to me, and it genuinely helps me decide what goes to print."
