import type { CapacitorConfig } from '@capacitor/cli';

// Stage 7: wraps the adapter-static build for Android. vite.config.ts emits
// the production bundle to `build/` (pages/assets both point there, with
// 200.html as the SPA fallback) — NOT the Capacitor-default `dist/`, so
// webDir has to be pointed there explicitly or `cap sync` copies nothing.
const config: CapacitorConfig = {
  appId: 'com.ARKfolio.app',
  appName: 'ARKfolio',
  webDir: 'build',
  backgroundColor: '#f6f2e8', // --paper, avoids a white flash before the app paints
  android: {
    backgroundColor: '#f6f2e8'
  },
  plugins: {
    // Kept dark-on-light by default; src/lib/native/nativeShell.ts flips this
    // to light-on-dark as soon as the app boots into a saved dark-mode
    // preference. backgroundColor/overlaysWebView are intentionally omitted:
    // Android 16+ (this app's targetSdk) enforces edge-to-edge and ignores
    // them — see the safe-area-inset padding in src/lib/styles/main.css.
    StatusBar: {
      style: 'DARK'
    },
    // nativeShell.ts hides the splash manually once the Svelte app has
    // mounted, so it holds until the app is actually ready to paint instead
    // of auto-dismissing (the default) before that logic ever runs.
    SplashScreen: {
      launchAutoHide: false,
      backgroundColor: '#f6f2e8',
      androidSplashResourceName: 'splash',
      androidScaleType: 'CENTER_CROP'
    }
  }
};

export default config;
