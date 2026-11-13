#!/bin/bash
set -e

cd "$(dirname "$0")"

APP_NAME="FatturaPro"
DMG_NAME="${APP_NAME}.dmg"

# Usa il Python del virtualenv del progetto (arm64)
if [ -x "venv/bin/python" ]; then
    PYTHON="venv/bin/python"
else
    PYTHON="python3"
fi

# Verifica di essere su Apple Silicon
if [ "$(uname -m)" != "arm64" ]; then
    echo "ERRORE: il build deve essere eseguito su un Mac Apple Silicon (arm64)."
    exit 1
fi

# Pulisci le cartelle di build e dist
rm -rf build/ dist/

# Esegui il build
echo "Eseguendo il build con PyInstaller..."
"$PYTHON" -m PyInstaller --noconfirm build.spec

# Verifica che il build sia riuscito
if [ ! -d "dist/${APP_NAME}.app" ]; then
    echo "ERRORE: Il build è fallito. L'applicazione ${APP_NAME}.app non è stata creata."
    exit 1
fi

echo "Build completato con successo!"

# Rimuovi DMG esistenti (solo dopo un build riuscito)
rm -f "${DMG_NAME}" rw.*."${DMG_NAME}"

echo "Creando il DMG..."
if command -v create-dmg >/dev/null 2>&1; then
    create-dmg \
      --volname "${APP_NAME}" \
      --volicon "assets/icon.icns" \
      --window-pos 200 120 \
      --window-size 800 400 \
      --icon-size 100 \
      --icon "${APP_NAME}.app" 200 200 \
      --hide-extension "${APP_NAME}.app" \
      --app-drop-link 600 200 \
      --no-internet-enable \
      "${DMG_NAME}" \
      "dist/${APP_NAME}.app"
else
    # Fallback senza dipendenze: usa hdiutil (incluso in macOS)
    STAGING="$(mktemp -d)"
    cp -R "dist/${APP_NAME}.app" "${STAGING}/"
    ln -s /Applications "${STAGING}/Applications"
    hdiutil create \
      -volname "${APP_NAME}" \
      -srcfolder "${STAGING}" \
      -fs HFS+ \
      -format UDZO \
      -ov \
      "${DMG_NAME}"
    rm -rf "${STAGING}"
fi

echo "DMG creato con successo: ${DMG_NAME}"
