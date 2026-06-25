#!/bin/bash

set -e

PACKAGE_NAME="audioharvester"
VERSION=$(grep VERSION src/version.py | cut -d'"' -f2)
ARCH="all"

APP_DIR="packaging/deb/usr/share/audioharvester"

echo "Preparing package files..."

cp src/main.py "$APP_DIR/"
cp src/settings.py "$APP_DIR/"
cp src/version.py "$APP_DIR/"
cp src/download.py "$APP_DIR/"
cp src/legal.py "$APP_DIR/"
cp src/about.py "$APP_DIR/"
cp src/changelog.py "$APP_DIR/"
cp CHANGELOG.md "$APP_DIR/"

mkdir -p "$APP_DIR/icons"
cp icons/audioharvester.png "$APP_DIR/icons/"
cp icons/audioharvester.png packaging/deb/usr/share/pixmaps/

echo "Building ${PACKAGE_NAME}_${VERSION}_${ARCH}.deb..."

rm -f packaging/*.deb

dpkg-deb --build --root-owner-group packaging/deb

mv packaging/deb.deb "packaging/${PACKAGE_NAME}_${VERSION}_${ARCH}.deb"

echo "Done:"
echo "packaging/${PACKAGE_NAME}_${VERSION}_${ARCH}.deb"