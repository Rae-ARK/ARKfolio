export interface Retailer {
  label: string
  url: string
  /** Shown under the buttons when the link isn't a plain product page. */
  note?: string
  /** The one retailer shown as the main "Buy" button; the rest are grouped
   *  under "Other retailers". */
  primary?: boolean
}

export interface StoreBook {
  workSlug: 'sbm'
  thumbClass: 'sbm' | 'sbm2'
  edition: string
  title: string
  description: string
  /** Publisher/ISBN line. Omitted for books that aren't in print yet. */
  note?: string
  /** Bare ISBN-13 (digits only) and publication month (YYYY-MM). Feed the
   *  Book structured data; omitted for books that aren't in print yet. */
  isbn?: string
  datePublished?: string
  retailers: Retailer[]
  /** Set on a volume that's announced but not yet purchasable. When set,
   *  the Store renders an availability badge instead of the retailer grid. */
  status?: 'coming-soon'
  /** Shown on the badge when status is 'coming-soon', e.g. "Winter 2027". */
  availability?: string
}

export const storeBooks: StoreBook[] = [
  {
    workSlug: 'sbm',
    thumbClass: 'sbm',
    edition: 'SBM · June 2026 Edition',
    title: 'Summoned by Mistake, I Decided to Learn How to Live',
    description:
      'Volume 1 — Unwanted Summoning / Of Names and New Beginnings (Arc 1 & 2). Lightly formatted paperback, limited run. Includes a QR code for a free PDF copy with purchase.',
    note: 'Independently Published (unofficially under Horizon ARK Studio) · ISBN 979-8-1810-7869-7',
    isbn: '9798181078697',
    datePublished: '2026-06',
    retailers: [
      {
        label: 'Amazon',
        primary: true,
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
  {
    workSlug: 'sbm',
    thumbClass: 'sbm2',
    edition: 'SBM · Volume 2',
    title: 'Summoned by Mistake, I Decided to Learn How to Live',
    description: 'Volume 2 — Arc 3. Paperback edition, following the same lightly formatted print run as Volume 1.',
    retailers: [],
    status: 'coming-soon',
    availability: 'Coming soon — Winter 2027',
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
  "Novels which aren't available in print yet. If that changes, they'll appear here first."

export const notYetInPrintCta =
  "Waiting on one of them? Tell me which — it opens an email to me, and it genuinely helps me decide what goes to print."
