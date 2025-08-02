# Installazione di wkhtmltopdf

Questo documento spiega come installare `wkhtmltopdf` necessario per la generazione di PDF nel sistema FATT.

## Cos'è wkhtmltopdf

`wkhtmltopdf` è uno strumento da riga di comando che converte pagine HTML in PDF utilizzando il motore di rendering WebKit. È utilizzato dal sistema FATT per generare i PDF delle fatture elettroniche.

## Installazione

### macOS

#### Metodo 1: Homebrew (Raccomandato)
```bash
brew install wkhtmltopdf
```

#### Metodo 2: Download diretto
1. Vai su https://wkhtmltopdf.org/downloads.html
2. Scarica la versione per macOS
3. Installa il pacchetto .pkg

#### Metodo 3: MacPorts
```bash
sudo port install wkhtmltopdf
```

### Linux (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install wkhtmltopdf
```

### Linux (CentOS/RHEL/Fedora)
```bash
sudo yum install wkhtmltopdf
# oppure
sudo dnf install wkhtmltopdf
```

### Windows
1. Vai su https://wkhtmltopdf.org/downloads.html
2. Scarica la versione per Windows
3. Esegui l'installer

## Verifica dell'Installazione

Dopo l'installazione, verifica che `wkhtmltopdf` sia disponibile:

```bash
wkhtmltopdf --version
```

Dovresti vedere output simile a:
```
wkhtmltopdf 0.12.6 (with patched qt)
```

## Gestione delle Stampanti

### Verifica delle Stampanti Configurate

Per verificare le stampanti configurate nel sistema:

#### macOS
```bash
lpstat -p
```

#### Linux
```bash
lpstat -p
```

#### Windows
```bash
wmic printer get name
```

### Nessuna Stampante Configurata

Se non ci sono stampanti configurate nel sistema, il sistema FATT gestisce automaticamente questa situazione:

1. **Salvataggio automatico**: Il PDF viene salvato automaticamente sul Desktop come `fattura_stampa.pdf`
2. **Dialog informativo**: Viene mostrato un messaggio che spiega la situazione
3. **Opzione di apertura**: L'utente può scegliere di aprire il PDF direttamente con l'applicazione di default
4. **Nessun errore**: Il sistema non si blocca o mostra errori confusi

### Configurazione di una Stampante

#### macOS
1. Vai su **Preferenze di Sistema** > **Stampanti e Scanner**
2. Clicca su **+** per aggiungere una stampante
3. Seleziona la stampante dalla lista o aggiungi una stampante di rete

#### Linux
```bash
# Installa CUPS se non è già installato
sudo apt-get install cups

# Avvia il servizio CUPS
sudo systemctl start cups

# Apri l'interfaccia web di configurazione
# http://localhost:631
```

#### Windows
1. Vai su **Impostazioni** > **Dispositivi** > **Stampanti e scanner**
2. Clicca su **Aggiungi stampante o scanner**
3. Segui le istruzioni per aggiungere la stampante

## Risoluzione Problemi

### Errore: "wkhtmltopdf non trovato"

Se ricevi questo errore nel sistema FATT:

1. **Verifica l'installazione**:
   ```bash
   which wkhtmltopdf
   ```

2. **Se non è installato**, segui le istruzioni di installazione sopra

3. **Se è installato ma non viene trovato**, verifica che sia nel PATH:
   ```bash
   echo $PATH
   ```

4. **Su macOS con Homebrew**, assicurati che `/usr/local/bin` sia nel PATH

### Errore: "Nessuna destinazione di default" (lpr)

Questo errore indica che non ci sono stampanti configurate:

1. **Verifica le stampanti**:
   ```bash
   lpstat -p
   ```

2. **Se non ci sono stampanti**, il sistema FATT gestirà automaticamente la situazione salvando il PDF

3. **Per configurare una stampante**, segui le istruzioni nella sezione "Configurazione di una Stampante"

### Errore di Permessi

Se ricevi errori di permessi:

```bash
# Su macOS/Linux
chmod +x /usr/local/bin/wkhtmltopdf
```

### Problemi con X11 (Linux)

Su alcuni sistemi Linux potrebbe essere necessario installare X11:

```bash
# Ubuntu/Debian
sudo apt-get install xvfb

# CentOS/RHEL
sudo yum install xorg-x11-server-Xvfb
```

## Configurazione Avanzata

### Opzioni wkhtmltopdf

Il sistema FATT utilizza le seguenti opzioni per `wkhtmltopdf`:
- `--quiet`: Riduce l'output verboso
- `--encoding UTF-8`: Assicura la corretta codifica dei caratteri
- `--page-size A4`: Imposta la dimensione della pagina
- `--margin-* 20mm`: Imposta i margini

### Personalizzazione

Se desideri personalizzare le opzioni di `wkhtmltopdf`, puoi modificare il file `gui/main_window.py` nella funzione `save_as_pdf()`.

## Supporto

Se riscontri problemi con l'installazione o l'utilizzo di `wkhtmltopdf`:

1. Controlla la documentazione ufficiale: https://wkhtmltopdf.org/documentation.html
2. Verifica i requisiti di sistema
3. Controlla i log di errore per dettagli specifici

## Note per gli Sviluppatori

Il sistema FATT cerca `wkhtmltopdf` nei seguenti percorsi (in ordine di priorità):

1. Nel PATH del sistema (`which wkhtmltopdf`)
2. Percorsi comuni su macOS:
   - `/usr/local/bin/wkhtmltopdf`
   - `/opt/homebrew/bin/wkhtmltopdf`
   - `/usr/bin/wkhtmltopdf`
3. Nella directory `bin/` del progetto (per sviluppo)
4. Nella directory `bin/` del bundle (per distribuzione)

Se nessuno di questi percorsi funziona, il sistema mostrerà un messaggio di errore con istruzioni per l'installazione.

### Gestione delle Stampanti

Il sistema gestisce automaticamente i casi senza stampanti:

1. **Rilevamento**: Verifica la presenza di stampanti con `lpstat -p`
2. **Fallback**: Se non ci sono stampanti, salva il PDF sul Desktop
3. **Interfaccia utente**: Mostra un dialog con opzioni per l'utente
4. **Apertura PDF**: Permette di aprire il PDF con l'applicazione di default 