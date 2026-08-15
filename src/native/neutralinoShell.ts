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
    }
    NL_PORT?: number
  }
}

export function isNeutralino(): boolean {
  return typeof window !== 'undefined' && typeof window.Neutralino !== 'undefined'
}

export async function initNeutralinoShell() {
  if (!isNeutralino()) return
  const Neutralino = window.Neutralino!

  Neutralino.init()

  // Clean shutdown when the window is closed instead of leaving the
  // background Neutralino process running.
  Neutralino.events.on('windowClose', () => {
    Neutralino.app.exit()
  })

  await Neutralino.window.setTitle('Rae ARK — Web Novelist')
  await Neutralino.window.show()
}
