import type { CapacitorConfig } from '@capacitor/cli';

// Stage 3: wraps the same Stage 1/2 web build (`dist/`) for Android.
// No UI components change for this — Capacitor just hosts the built
// app in a WebView. appId/appName can be changed any time before your
// first Play Store upload; changing appId *after* release requires a
// new app listing, so lock this in once you're happy with it.
const config: CapacitorConfig = {
  appId: 'com.raeark.arkfolio',
  appName: 'Rae ARK',
  webDir: 'dist',
  backgroundColor: '#f6f2e8', // --paper, avoids a white flash before the app paints
  android: {
    backgroundColor: '#f6f2e8',
  },
  plugins: {
    // Kept dark-on-light by default; src/native/nativeShell.ts flips this to
    // light-on-dark as soon as the app boots into a saved dark-mode preference.
    // backgroundColor/overlaysWebView are intentionally omitted: Android 16+
    // (this app's targetSdk) enforces edge-to-edge and ignores them — see
    // the safe-area-inset padding in main.css instead.
    StatusBar: {
      style: 'DARK',
    },
    // We hide the splash manually from nativeShell.ts once Vue has mounted,
    // so it holds until the app is actually ready to paint instead of racing it.
    SplashScreen: {
      launchAutoHide: false,
      backgroundColor: '#f6f2e8',
      androidSplashResourceName: 'splash',
      androidScaleType: 'CENTER_CROP',
    },
  },
};

export default config;
