#!/bin/bash

# Pulisci le cartelle di build e dist
rm -rf build/ dist/

# Rimuovi DMG esistenti
rm -f "FatturaPro.dmg"

# Esegui il build
python3 -m PyInstaller build.spec

# Crea il DMG con coordinate più sicure
create-dmg \
  --volname "FatturaPro" \
  --volicon "assets/icon.icns" \
  --window-pos 200 120 \
  --window-size 800 400 \
  --icon-size 100 \
  --icon "FatturaPro.app" 200 200 \
  --hide-extension "FatturaPro.app" \
  --app-drop-link 600 200 \
  --no-internet-enable \
  "FatturaPro.dmg" \
  "dist/" 