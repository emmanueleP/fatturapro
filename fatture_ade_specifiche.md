# Conformità alle Specifiche Tecniche dell'Agenzia delle Entrate

Questo documento descrive come il sistema FATT è stato aggiornato per essere conforme alle specifiche tecniche dell'Agenzia delle Entrate per le fatture elettroniche.

## Riferimenti Normativi

Il sistema è stato aggiornato seguendo le specifiche tecniche disponibili sul sito dell'Agenzia delle Entrate:
- [Normativa, prassi e regole tecniche – Fatture elettroniche](https://www.agenziaentrate.gov.it/portale/normativa-prassi-e-regole-tecniche-fatture-elettroniche)

### Versioni delle Specifiche Supportate

Il sistema ora supporta le seguenti versioni delle specifiche tecniche:
- **Versione 1.2**: Versione base supportata
- **Versione 1.8**: Utilizzabile a partire dal 1° febbraio 2024
- **Versione 1.9**: Utilizzabile dal 1° aprile 2025

## Modifiche Implementate

### 1. Parser delle Fatture Elettroniche (`utils/invoice_parser.py`)

#### Namespace Supportati
```python
self.ns = {
    'p': 'http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2',
    'p_v1_8': 'http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.8',
    'p_v1_9': 'http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.9',
    'ds': 'http://www.w3.org/2000/09/xmldsig#',
    'xsi': 'http://www.w3.org/2001/XMLSchema-instance'
}
```

#### Rilevamento Automatico della Versione
Il sistema rileva automaticamente la versione delle specifiche utilizzate nel file XML e si adatta di conseguenza.

#### Codici Tipo Documento Conformi
Implementati tutti i codici tipo documento secondo le specifiche tecniche:

- **TD01**: Fattura
- **TD02**: Acconto/Anticipo su fattura
- **TD03**: Acconto/Anticipo su parcella
- **TD04**: Nota di credito
- **TD05**: Nota di debito
- **TD06**: Parcella
- **TD16**: Integrazione fattura reverse charge interno
- **TD17**: Integrazione autofattura per acquisti servizi dall'estero
- **TD18**: Integrazione per acquisti di beni da soggetti non residenti
- **TD19**: Integrazione/autofattura per acquisti in san marino con soggetti identificati
- **TD20**: Autofattura per regolarizzazione e integrazione delle fatture
- **TD21**: Autofattura per splafonamento
- **TD22**: Estrazione beni da Deposito IVA
- **TD23**: Estrazione beni da Deposito IVA con versamento dell'IVA
- **TD24**: Fattura differita (art.21, 3° comma, lett. a)
- **TD25**: Fattura differita (art.21, 3° comma, lett. b)
- **TD26**: Cessione di beni ammortizzabili e per passaggi interni
- **TD27**: Fattura per autoconsumo o per cessioni gratuite senza rivalsa
- **TD28-TD50**: Fatture per acquisti da soggetti non residenti con IVA assolta dal cessionario

#### Modalità di Pagamento Conformi
Implementate tutte le modalità di pagamento secondo le specifiche:

- **MP01**: Contanti
- **MP02**: Assegno
- **MP03**: Assegno circolare
- **MP04**: Contanti presso Tesoreria
- **MP05**: Bonifico
- **MP06**: Vaglia cambiario
- **MP07**: Bollettino bancario
- **MP08**: Carta di pagamento
- **MP09**: RID
- **MP10**: RID utenze
- **MP11**: RID veloce
- **MP12**: RIBA
- **MP13**: MAV
- **MP14**: Quietanza erario
- **MP15**: Giroconto su conti di contabilità speciale
- **MP16**: Domiciliazione bancaria
- **MP17**: Domiciliazione postale
- **MP18**: Bollettino di c/c postale
- **MP19**: SEPA Direct Debit
- **MP20**: SEPA Direct Debit CORE
- **MP21**: SEPA Direct Debit B2B
- **MP22**: Trattenuta su somme già riscosse
- **MP23**: PagoPA

#### Condizioni di Pagamento
- **TP01**: Pagamento a rate
- **TP02**: Pagamento completo
- **TP03**: Anticipo

### 2. Layout PDF Conforme (`utils/pdf_layout.py`)

#### Miglioramenti alla Presentazione
- Visualizzazione della versione delle specifiche tecniche utilizzate
- Mostra sia il codice che la descrizione per tipo documento, modalità di pagamento e condizioni di pagamento
- Aggiunta di colonne per codice articolo e unità di misura nella tabella beni/servizi
- Visualizzazione della nazione per cedente e cessionario
- Miglioramento della formattazione del totale documento

#### Gestione Sicura dei Dati
- Gestione robusta dei valori numerici con try/catch
- Valori di default appropriati per tutti i campi
- Supporto per dati mancanti o malformati

### 3. Sistema di Stampa Unificato (`utils/print_manager.py`)

#### Coerenza tra Visualizzazione e Stampa
- **Layout unificato**: La stampa utilizza lo stesso layout PDF della visualizzazione
- **Qualità uniforme**: Stesso aspetto per visualizzazione, salvataggio PDF e stampa
- **Gestione stampanti**: Supporto per selezione stampante e opzioni di stampa

#### Funzionalità di Stampa
- **Dialog di stampa**: Interfaccia nativa per selezione stampante e opzioni
- **Supporto multi-piattaforma**: macOS, Windows e Linux
- **Gestione errori**: Messaggi chiari per problemi di stampa
- **Pulizia automatica**: Rimozione automatica dei file temporanei

#### Processo di Stampa
1. **Generazione PDF temporaneo**: Crea un PDF usando il layout unificato
2. **Dialog di stampa**: Mostra l'interfaccia nativa per selezione stampante
3. **Invio alla stampante**: Utilizza comandi di sistema appropriati per piattaforma
4. **Conferma**: Mostra messaggio di successo o errore
5. **Pulizia**: Rimuove automaticamente i file temporanei

## Funzionalità Aggiuntive

### 1. Rilevamento Automatico della Versione
Il sistema rileva automaticamente la versione delle specifiche utilizzate nel file XML e si adatta di conseguenza.

### 2. Gestione Robusta degli Errori
- Gestione sicura dei valori numerici
- Fallback per dati mancanti
- Supporto per diversi formati di namespace

### 3. Informazioni Dettagliate
- Descrizioni complete per tutti i codici
- Informazioni sulla versione delle specifiche
- Dati aggiuntivi come unità di misura e codice articolo

### 4. Sistema di Stampa Professionale
- Layout unificato per tutte le operazioni
- Supporto completo per stampanti
- Gestione robusta degli errori di stampa

## Conformità Normativa

Il sistema ora è conforme a:

1. **Provvedimento del 24 novembre 2022**: Regole tecniche per l'emissione e la ricezione delle fatture elettroniche
2. **Provvedimento dell'8 marzo 2024**: Modifiche alle regole tecniche
3. **Specifiche tecniche versione 1.8**: Utilizzabili dal 1° febbraio 2024
4. **Specifiche tecniche versione 1.9**: Utilizzabili dal 1° aprile 2025

## Utilizzo

Il sistema ora gestisce automaticamente:
- Rilevamento della versione delle specifiche
- Parsing conforme di tutti i campi obbligatori e facoltativi
- Visualizzazione delle descrizioni complete per tutti i codici
- Gestione robusta di fatture con formati diversi
- Stampa professionale con layout unificato

## Note Tecniche

- Il sistema mantiene la retrocompatibilità con le versioni precedenti
- Tutti i namespace sono supportati automaticamente
- La gestione degli errori è migliorata per evitare crash con dati malformati
- Le descrizioni dei codici sono basate sulle specifiche ufficiali dell'Agenzia delle Entrate
- Il sistema di stampa utilizza `wkhtmltopdf` per garantire qualità uniforme
- Rimossa dipendenza da ReportLab per semplificare il sistema 