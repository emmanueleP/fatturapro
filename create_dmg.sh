#!/bin/bash

# Pulisci le cartelle di build e dist
rm -rf build/ dist/

# Rimuovi DMG esistenti
rm -f "FatturaPro.dmg"

# Esegui il build
python3 -m PyInstaller build.spec

# Crea il DMG
create-dmg \
  --volname "FatturaPro" \
  --volicon "assets/icon.icns" \
  --window-pos 200 120 \
  --window-size 800 400 \
  --icon-size 100 \
  --icon "FatturaPro.app" 200 190 \
  --hide-extension "FatturaPro.app" \
  --app-drop-link 600 185 \
  "FatturaPro.dmg" \
  "dist/" 