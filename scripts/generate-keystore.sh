#!/usr/bin/env bash
# Generates a self-managed release keystore for signing ArkFolio APKs
# outside the Play Store. Run this ONCE, locally, and never commit the
# resulting .jks file — it's the private key that proves future updates
# come from you. Losing it means any future release needs a new
# applicationId (Android won't let you update-in-place with a different key).
#
# Usage:
#   scripts/generate-keystore.sh [keystore-path] [alias]
#
# Defaults to android/release-keystore.jks and alias "arkfolio".
set -euo pipefail
cd "$(dirname "$0")/.."

KEYSTORE_PATH="${1:-android/release-keystore.jks}"
ALIAS="${2:-arkfolio}"

if [ -f "$KEYSTORE_PATH" ]; then
  echo "error: $KEYSTORE_PATH already exists — refusing to overwrite it." >&2
  echo "If you really want a new one, move or delete the old file first." >&2
  exit 1
fi

echo "Creating a release keystore at $KEYSTORE_PATH"
echo "You'll be asked for a keystore password, some identity details, and a key password."
echo "Store both passwords in a password manager — there is no recovery if you lose them."
echo

keytool -genkeypair -v \
  -keystore "$KEYSTORE_PATH" \
  -alias "$ALIAS" \
  -keyalg RSA -keysize 2048 -validity 10000

echo
echo "Done. Next steps:"
echo "  1. Confirm $KEYSTORE_PATH is gitignored (it is, by default) — never commit it."
echo "  2. Base64-encode it for GitHub Actions:"
echo "       base64 -w0 $KEYSTORE_PATH"
echo "  3. Add these four repo secrets (Settings -> Secrets and variables -> Actions):"
echo "       ANDROID_KEYSTORE_BASE64   <- output of step 2"
echo "       ANDROID_KEYSTORE_PASSWORD <- the keystore password you just set"
echo "       ANDROID_KEY_ALIAS         <- $ALIAS"
echo "       ANDROID_KEY_PASSWORD      <- the key password you just set"
echo "  4. Back up $KEYSTORE_PATH itself somewhere safe outside git (password manager, encrypted drive)."
