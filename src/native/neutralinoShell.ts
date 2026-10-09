// Desktop (Linux/Windows/macOS) shell — makes the app behave like a native
// window instead of "a website in a box" when it's running inside
// Neutralino. Everything here is a no-op on the web/Android build (there's
// no window.Neutralino global there), so this file is safe to import
// unconditionally from main.ts.
declare global {
  interface Window {
    Neutralino?: {
      init: () => void
      events: {
        on: (event: string, handler: (evt?: unknown) => void) => void
      }
      app: {
        exit: () => Promise<void>
      }
      window: {
        setTitle: (title: string) => Promise<void>
        show: () => Promise<void>
      }
      os: {
        open: (url: string) => Promise<void>
      }
    }
    NL_PORT?: number
  }
}

export function isNeutralino(): boolean {
  return typeof window !== 'undefined' && typeof window.Neutralino !== 'undefined'
}

/** Open outbound links (GitHub, X, retailers) with the OS's default browser
 *  instead of letting the embedded WebKitGTK/WebView2 window try (and fail)
 *  to handle target="_blank" itself. Neutralino's webview has no popup/tab
 *  chrome, so an unhandled target="_blank" click is a silent no-op — this
 *  is why external links previously did nothing in the desktop build. */
function wireExternalLinks() {
  const Neutralino = window.Neutralino!
  document.addEventListener('click', (event) => {
    const anchor = (event.target as HTMLElement)?.closest('a[target="_blank"]') as HTMLAnchorElement | null
    if (!anchor?.href) return
    event.preventDefault()
    Neutralino.os.open(anchor.href).catch(() => {
      // Fall back to a same-window navigation rather than a dead click if
      // the OS handler call itself fails for some reason.
      window.open(anchor.href, '_blank', 'noopener')
    })
  })
}

export async function initNeutralinoShell() {
  if (!isNeutralino()) return
  const Neutralino = window.Neutralino!

  Neutralino.init()

  // Flag the desktop shell in the DOM so main.css can drop backdrop-filter
  // blur there. WebKitGTK (the Linux engine Neutralino embeds) recomposites
  // that blur on every scroll frame under a `position: sticky` header, which
  // is the main source of the janky/laggy feel on desktop — it's fine on
  // Chromium/Safari (web + Android) so we only strip it for this shell.
  document.documentElement.setAttribute('data-shell', 'neutralino')

  // Clean shutdown when the window is closed instead of leaving the
  // background Neutralino process running.
  Neutralino.events.on('windowClose', () => {
    Neutralino.app.exit()
  })

  wireExternalLinks()

  await Neutralino.window.setTitle('Rae ARK — Web Novelist')
  await Neutralino.window.show()
}
