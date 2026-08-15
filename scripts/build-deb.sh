#!/usr/bin/env bash
# Packages the embedded-resources Neutralino Linux x64 binary (produced by
# `npx neu build --release --embed-resources`) into a .deb.
#
# Expects:
#   dist/arkfolio/arkfolio-linux_x64   <- built by `neu build`
#   dist/icons/icon-512.png            <- built by `vite build`
#   packaging/debian/                  <- static desktop file, etc.
#
# Produces:
#   dist/deb/arkfolio_<version>_amd64.deb
set -euo pipefail
cd "$(dirname "$0")/.."

PKG_NAME=arkfolio
ARCH=amd64
VERSION=$(node -p "require('./package.json').version")
BINARY=dist/arkfolio/arkfolio-linux_x64
ICON=dist/icons/icon-512.png
BUILD_DIR=dist/deb-build
OUT_DIR=dist/deb

if [ ! -f "$BINARY" ]; then
  echo "error: $BINARY not found — run 'npx neu build --release --embed-resources' first" >&2
  exit 1
fi

rm -rf "$BUILD_DIR" "$OUT_DIR"
mkdir -p "$OUT_DIR"

# Copy the static packaging skeleton (desktop entry, any future config).
cp -r packaging/debian "$BUILD_DIR"

# Binary.
mkdir -p "$BUILD_DIR/usr/bin"
install -m 755 "$BINARY" "$BUILD_DIR/usr/bin/$PKG_NAME"

# Icon (for the .desktop entry's Icon=arkfolio to resolve via the icon theme).
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/512x512/apps"
install -m 644 "$ICON" "$BUILD_DIR/usr/share/icons/hicolor/512x512/apps/$PKG_NAME.png"

# Debian control metadata.
mkdir -p "$BUILD_DIR/DEBIAN"
INSTALLED_SIZE=$(du -sk "$BUILD_DIR/usr" | cut -f1)
cat > "$BUILD_DIR/DEBIAN/control" <<EOF
Package: $PKG_NAME
Version: $VERSION
Section: web
Priority: optional
Architecture: $ARCH
Installed-Size: $INSTALLED_SIZE
Depends: libwebkit2gtk-4.1-0 | libwebkit2gtk-4.0-37, libgtk-3-0
Maintainer: Rae ARK <noreply@example.com>
Homepage: https://github.com/Rae-ARK/My-Portfolio
Description: ArkFolio desktop app
 Desktop build of the Rae ARK portfolio, journal, and store site.
 Built with Vue 3 and packaged as a native window with NeutralinoJS.
EOF

find "$BUILD_DIR" -type d -exec chmod 755 {} \;
find "$BUILD_DIR" -type f -not -path "*/DEBIAN/*" -exec chmod 644 {} \;
chmod 755 "$BUILD_DIR/usr/bin/$PKG_NAME"

OUT_FILE="$OUT_DIR/${PKG_NAME}_${VERSION}_${ARCH}.deb"
dpkg-deb --build --root-owner-group "$BUILD_DIR" "$OUT_FILE"

echo "Built $OUT_FILE"
