// Proposal 0011: privacy-friendly analytics via Cloudflare Web Analytics.
// The beacon sets no cookies, uses no localStorage/client-side state, and
// collects no personally identifiable information — it only reports
// aggregate page-view and performance metrics for the zone, which is why
// this stays out of the "What's collected" exceptions in PrivacyPolicyPage.vue
// rather than needing a consent flow.
//
// The Android (Capacitor) and desktop (Neutralino) builds load this exact
// same bundle, but they aren't web page views of rae-ark.horizonarkstudio.workers.dev
// — loading the beacon there would both be pointless (it has nothing to do
// with a WebView session) and quietly inflate/skew the site's traffic
// numbers with app opens. So this only ever injects the script on the
// hosted web build, the same way nativeShell.ts/neutralinoShell.ts gate
// their own behavior to their one platform.
import { Capacitor } from '@capacitor/core'
import { isDesktopShell } from './neutralinoShell'

// From the Cloudflare dashboard for this zone (Analytics & Logs > Web
// Analytics > Manage Site > "Beacon token"). Safe to ship client-side: it
// only identifies which zone the beacon reports to, the same way a GA
// measurement ID would — it carries no visitor data itself.
const CF_BEACON_TOKEN = 'REPLACE_WITH_CLOUDFLARE_BEACON_TOKEN'

export function initAnalytics() {
  if (Capacitor.isNativePlatform() || isDesktopShell()) return
  // Dev/preview traffic shouldn't count toward the real site's numbers.
  if (!import.meta.env.PROD) return

  const script = document.createElement('script')
  script.defer = true
  script.src = 'https://static.cloudflareinsights.com/beacon.min.js'
  script.setAttribute('data-cf-beacon', JSON.stringify({ token: CF_BEACON_TOKEN }))
  document.head.appendChild(script)
}
