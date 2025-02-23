#!/bin/bash

# Rimuovi DMG esistenti
rm -f "FatturaPro.dmg"

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