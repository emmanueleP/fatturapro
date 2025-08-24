#!/bin/bash

# Pulisci le cartelle di build e dist
rm -rf build/ dist/

# Rimuovi DMG esistenti
rm -f "FatturaPro.dmg"

# Esegui il build
echo "Eseguendo il build con PyInstaller..."
python3 -m PyInstaller build.spec

# Verifica che il build sia riuscito
if [ ! -d "dist/FatturaPro.app" ]; then
    echo "ERRORE: Il build è fallito. L'applicazione FatturaPro.app non è stata creata."
    exit 1
fi

echo "Build completato con successo!"

# Crea il DMG con coordinate più sicure
echo "Creando il DMG..."
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

echo "DMG creato con successo!" 