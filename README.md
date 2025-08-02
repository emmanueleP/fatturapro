# FatturaPro

FatturaPro è un visualizzatore di fatture elettroniche moderno e intuitivo per macOS. Permette di visualizzare, convertire in PDF e stampare fatture elettroniche in formato XML e P7M. L'idea di creare quest'app nasce dalla quasi completa mancanza di software specifico per macOS per visualizzare le fatture elettroniche.

![Screenshot dell'applicazione](assets/icon_256x256.png)

## Caratteristiche

- 📄 Visualizzazione di fatture elettroniche in formato XML
- 🔐 Supporto per fatture firmate digitalmente (P7M)
- 💾 Conversione in PDF
- 🖨️ Stampa dei documenti
- 🌓 Tema chiaro/scuro
- 🖱️ Supporto per drag & drop
- ✅ Conformità alle specifiche tecniche dell'Agenzia delle Entrate

## Requisiti di Sistema

- macOS 13 (Ventura) o superiore
- Apple Silicon
- wkhtmltopdf (per la generazione di PDF)

## Installazione

### Installazione dell'Applicazione

1. Scarica l'ultima versione da [Releases](https://github.com/emmanueleP/fatturapro/releases)
2. Sposta FatturaPro nella cartella Applicazioni
3. Al primo avvio, clicca con il tasto destro sull'icona e seleziona "Apri"

### Installazione di wkhtmltopdf

Per utilizzare la funzionalità di conversione in PDF, è necessario installare `wkhtmltopdf`:

#### macOS (Raccomandato)
```bash
brew install wkhtmltopdf
```

#### Verifica dell'installazione
```bash
wkhtmltopdf --version
```

Per istruzioni dettagliate, consulta [INSTALL_WKHTMLTOPDF.md](INSTALL_WKHTMLTOPDF.md).

## Conformità Normativa

FatturaPro è conforme alle specifiche tecniche dell'Agenzia delle Entrate per le fatture elettroniche:

- **Versione 1.2**: Supporto base
- **Versione 1.8**: Utilizzabile dal 1° febbraio 2024
- **Versione 1.9**: Utilizzabile dal 1° aprile 2025

Per maggiori dettagli, consulta [SPECIFICHE_AGENZIA_ENTRATE.md](SPECIFICHE_AGENZIA_ENTRATE.md).

## Licenza
Questo software è rilasciato sotto licenza GPL v3.0

## Author
Written by Emmanuele Pani.

## Bugs and issues
You can open a bug report or an issue through the GitHub repo page.

