import xml.etree.ElementTree as ET
from datetime import datetime

class InvoiceParser:
    def __init__(self):
        # Namespace utilizzati nelle fatture elettroniche italiane secondo le specifiche dell'Agenzia delle Entrate
        # Supporto per diverse versioni delle specifiche tecniche
        self.ns = {
            'p': 'http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2',
            'p_v1_8': 'http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.8',
            'p_v1_9': 'http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.9',
            'ds': 'http://www.w3.org/2000/09/xmldsig#',
            'xsi': 'http://www.w3.org/2001/XMLSchema-instance'
        }
        
        # Codici tipo documento secondo le specifiche tecniche
        self.tipi_documento = {
            'TD01': 'Fattura',
            'TD02': 'Acconto/Anticipo su fattura',
            'TD03': 'Acconto/Anticipo su parcella',
            'TD04': 'Nota di credito',
            'TD05': 'Nota di debito',
            'TD06': 'Parcella',
            'TD16': 'Integrazione fattura reverse charge interno',
            'TD17': 'Integrazione autofattura per acquisti servizi dall\'estero',
            'TD18': 'Integrazione per acquisti di beni da soggetti non residenti',
            'TD19': 'Integrazione/autofattura per acquisti in san marino con soggetti identificati',
            'TD20': 'Autofattura per regolarizzazione e integrazione delle fatture (art.6 c.8 e 9-bis d.lgs.471/97 o art.46 c.5 D.L.331/93)',
            'TD21': 'Autofattura per splafonamento',
            'TD22': 'Estrazione beni da Deposito IVA',
            'TD23': 'Estrazione beni da Deposito IVA con versamento dell\'IVA',
            'TD24': 'Fattura differita di cui all\'art.21, 3° comma, lett. a)',
            'TD25': 'Fattura differita di cui all\'art.21, 3° comma, lett. b)',
            'TD26': 'Cessione di beni ammortizzabili e per passaggi interni (art.36 DPR 633/72)',
            'TD27': 'Fattura per autoconsumo o per cessioni gratuite senza rivalsa',
            'TD28': 'Acquisti di beni da soggetti non residenti con IVA assolta dal cessionario',
            'TD29': 'Fattura per acquisti di beni da soggetti non residenti con IVA assolta dal cessionario',
            'TD30': 'Fattura per acquisti di servizi da soggetti non residenti con IVA assolta dal cessionario',
            'TD31': 'Fattura per acquisti di beni da soggetti non residenti con IVA assolta dal cessionario',
            'TD32': 'Fattura per acquisti di servizi da soggetti non residenti con IVA assolta dal cessionario',
            'TD33': 'Fattura per acquisti di beni da soggetti non residenti con IVA assolta dal cessionario',
            'TD34': 'Fattura per acquisti di servizi da soggetti non residenti con IVA assolta dal cessionario',
            'TD35': 'Fattura per acquisti di beni da soggetti non residenti con IVA assolta dal cessionario',
            'TD36': 'Fattura per acquisti di servizi da soggetti non residenti con IVA assolta dal cessionario',
            'TD37': 'Fattura per acquisti di beni da soggetti non residenti con IVA assolta dal cessionario',
            'TD38': 'Fattura per acquisti di servizi da soggetti non residenti con IVA assolta dal cessionario',
            'TD39': 'Fattura per acquisti di beni da soggetti non residenti con IVA assolta dal cessionario',
            'TD40': 'Fattura per acquisti di servizi da soggetti non residenti con IVA assolta dal cessionario',
            'TD41': 'Fattura per acquisti di beni da soggetti non residenti con IVA assolta dal cessionario',
            'TD42': 'Fattura per acquisti di servizi da soggetti non residenti con IVA assolta dal cessionario',
            'TD43': 'Fattura per acquisti di beni da soggetti non residenti con IVA assolta dal cessionario',
            'TD44': 'Fattura per acquisti di servizi da soggetti non residenti con IVA assolta dal cessionario',
            'TD45': 'Fattura per acquisti di beni da soggetti non residenti con IVA assolta dal cessionario',
            'TD46': 'Fattura per acquisti di servizi da soggetti non residenti con IVA assolta dal cessionario',
            'TD47': 'Fattura per acquisti di beni da soggetti non residenti con IVA assolta dal cessionario',
            'TD48': 'Fattura per acquisti di servizi da soggetti non residenti con IVA assolta dal cessionario',
            'TD49': 'Fattura per acquisti di beni da soggetti non residenti con IVA assolta dal cessionario',
            'TD50': 'Fattura per acquisti di servizi da soggetti non residenti con IVA assolta dal cessionario'
        }
        
        # Modalità di pagamento secondo le specifiche
        self.modalita_pagamento = {
            'MP01': 'Contanti',
            'MP02': 'Assegno',
            'MP03': 'Assegno circolare',
            'MP04': 'Contanti presso Tesoreria',
            'MP05': 'Bonifico',
            'MP06': 'Vaglia cambiario',
            'MP07': 'Bollettino bancario',
            'MP08': 'Carta di pagamento',
            'MP09': 'RID',
            'MP10': 'RID utenze',
            'MP11': 'RID veloce',
            'MP12': 'RIBA',
            'MP13': 'MAV',
            'MP14': 'Quietanza erario',
            'MP15': 'Giroconto su conti di contabilità speciale',
            'MP16': 'Domiciliazione bancaria',
            'MP17': 'Domiciliazione postale',
            'MP18': 'Bollettino di c/c postale',
            'MP19': 'SEPA Direct Debit',
            'MP20': 'SEPA Direct Debit CORE',
            'MP21': 'SEPA Direct Debit B2B',
            'MP22': 'Trattenuta su somme già riscosse',
            'MP23': 'PagoPA'
        }
        
        # Condizioni di pagamento
        self.condizioni_pagamento = {
            'TP01': 'Pagamento a rate',
            'TP02': 'Pagamento completo',
            'TP03': 'Anticipo'
        }
    
    def parse_invoice(self, xml_content):
        if isinstance(xml_content, bytes):
            xml_content = xml_content.decode('utf-8')
            
        root = ET.fromstring(xml_content)
        
        # Determina il namespace effettivo dal file e la versione delle specifiche
        self._detect_namespace_and_version(root)
        
        # Estrae i dati principali della fattura
        header = self._parse_header(root)
        supplier = self._parse_supplier(root)
        customer = self._parse_customer(root)
        items = self._parse_items(root)
        totals = self._parse_totals(root)
        payment = self._parse_payment(root)
        
        return {
            'header': header,
            'supplier': supplier,
            'customer': customer,
            'items': items,
            'totals': totals,
            'payment': payment,
            'version': self.detected_version
        }
    
    def _detect_namespace_and_version(self, root):
        """Rileva il namespace e la versione delle specifiche utilizzate"""
        # Cerca il namespace nel tag root
        root_tag = root.tag
        if '}' in root_tag:
            detected_ns = root_tag.split('}')[0].strip('{')
            
            # Determina la versione basandosi sul namespace
            if 'v1.9' in detected_ns:
                self.detected_version = '1.9'
                self.ns['p'] = detected_ns
            elif 'v1.8' in detected_ns:
                self.detected_version = '1.8'
                self.ns['p'] = detected_ns
            elif 'v1.2' in detected_ns:
                self.detected_version = '1.2'
                self.ns['p'] = detected_ns
            else:
                self.detected_version = 'unknown'
                self.ns['p'] = detected_ns
        else:
            self.detected_version = 'unknown'
    
    def _safe_find_text(self, element, xpath, default='N/D'):
        """Trova in sicurezza un elemento XML e restituisce il suo testo"""
        try:
            # Prova prima con il namespace
            found = element.find(xpath, self.ns)
            if found is None:
                # Prova senza namespace
                found = element.find(xpath.replace('p:', ''))
            return found.text if found is not None else default
        except:
            return default
    
    def _parse_header(self, root):
        # Prova diversi percorsi possibili per i dati generali
        header_paths = [
            './/FatturaElettronicaHeader/DatiGeneraliDocumento',
            './/DatiGeneraliDocumento',
            './/p:FatturaElettronicaHeader/p:DatiGeneraliDocumento',
            './/p:DatiGeneraliDocumento'
        ]
        
        header_data = None
        for path in header_paths:
            header_data = root.find(path, self.ns)
            if header_data is not None:
                break
                
        if header_data is None:
            return {
                'tipo_documento': 'N/D',
                'tipo_documento_desc': 'N/D',
                'data': datetime.now().strftime('%d/%m/%Y'),
                'numero': 'N/D',
                'divisa': 'EUR'
            }
        
        data_str = self._safe_find_text(header_data, './/Data', '2000-01-01')
        try:
            data_formatted = datetime.strptime(data_str, '%Y-%m-%d').strftime('%d/%m/%Y')
        except:
            data_formatted = data_str
            
        tipo_doc = self._safe_find_text(header_data, './/TipoDocumento')
        tipo_doc_desc = self.tipi_documento.get(tipo_doc, 'N/D')
            
        return {
            'tipo_documento': tipo_doc,
            'tipo_documento_desc': tipo_doc_desc,
            'data': data_formatted,
            'numero': self._safe_find_text(header_data, './/Numero'),
            'divisa': self._safe_find_text(header_data, './/Divisa', 'EUR')
        }
    
    def _parse_supplier(self, root):
        # Prova diversi percorsi possibili per i dati del fornitore
        supplier_paths = [
            './/FatturaElettronicaHeader/CedentePrestatore/DatiAnagrafici',
            './/CedentePrestatore/DatiAnagrafici',
            './/p:FatturaElettronicaHeader/p:CedentePrestatore/p:DatiAnagrafici',
            './/p:CedentePrestatore/p:DatiAnagrafici'
        ]
        
        supplier_data = None
        for path in supplier_paths:
            supplier_data = root.find(path, self.ns)
            if supplier_data is not None:
                break
        
        address_paths = [
            './/FatturaElettronicaHeader/CedentePrestatore/Sede',
            './/CedentePrestatore/Sede',
            './/p:FatturaElettronicaHeader/p:CedentePrestatore/p:Sede',
            './/p:CedentePrestatore/p:Sede'
        ]
        
        address_data = None
        for path in address_paths:
            address_data = root.find(path, self.ns)
            if address_data is not None:
                break
        
        if supplier_data is None or address_data is None:
            return {
                'denominazione': 'N/D',
                'partita_iva': 'N/D',
                'id_fiscale_iva': 'N/D',
                'regime_fiscale': 'N/D',
                'indirizzo': 'N/D',
                'cap': 'N/D',
                'citta': 'N/D',
                'provincia': 'N/D',
                'nazione': 'IT'
            }
        
        # Gestione denominazione o nome+cognome
        denominazione = self._safe_find_text(supplier_data, './/Denominazione')
        if not denominazione or denominazione == 'N/D':
            nome = self._safe_find_text(supplier_data, './/Nome', '')
            cognome = self._safe_find_text(supplier_data, './/Cognome', '')
            denominazione = f"{nome} {cognome}".strip() if nome or cognome else 'N/D'
        
        return {
            'denominazione': denominazione,
            'partita_iva': self._safe_find_text(supplier_data, './/IdCodice'),
            'id_fiscale_iva': self._safe_find_text(supplier_data, './/IdFiscaleIVA/IdPaese', '') + 
                             self._safe_find_text(supplier_data, './/IdFiscaleIVA/IdCodice', ''),
            'regime_fiscale': self._safe_find_text(supplier_data, './/RegimeFiscale'),
            'indirizzo': self._safe_find_text(address_data, './/Indirizzo'),
            'cap': self._safe_find_text(address_data, './/CAP'),
            'citta': self._safe_find_text(address_data, './/Comune'),
            'provincia': self._safe_find_text(address_data, './/Provincia'),
            'nazione': self._safe_find_text(address_data, './/Nazione', 'IT')
        }
    
    def _parse_customer(self, root):
        # Prova diversi percorsi possibili per i dati del cliente
        customer_paths = [
            './/FatturaElettronicaHeader/CessionarioCommittente/DatiAnagrafici',
            './/CessionarioCommittente/DatiAnagrafici',
            './/p:FatturaElettronicaHeader/p:CessionarioCommittente/p:DatiAnagrafici',
            './/p:CessionarioCommittente/p:DatiAnagrafici'
        ]
        
        customer_data = None
        for path in customer_paths:
            customer_data = root.find(path, self.ns)
            if customer_data is not None:
                break
        
        address_paths = [
            './/FatturaElettronicaHeader/CessionarioCommittente/Sede',
            './/CessionarioCommittente/Sede',
            './/p:FatturaElettronicaHeader/p:CessionarioCommittente/p:Sede',
            './/p:CessionarioCommittente/p:Sede'
        ]
        
        address_data = None
        for path in address_paths:
            address_data = root.find(path, self.ns)
            if address_data is not None:
                break

        # Cerca i dati PEC
        pec_paths = [
            './/FatturaElettronicaHeader/CessionarioCommittente/Contatti',
            './/CessionarioCommittente/Contatti',
            './/p:FatturaElettronicaHeader/p:CessionarioCommittente/p:Contatti',
            './/p:CessionarioCommittente/p:Contatti'
        ]
        
        pec_data = None
        for path in pec_paths:
            pec_data = root.find(path, self.ns)
            if pec_data is not None:
                break

        # Cerca la causale
        causale_paths = [
            './/FatturaElettronicaBody/DatiGenerali/DatiGeneraliDocumento/Causale',
            './/DatiGenerali/DatiGeneraliDocumento/Causale',
            './/p:FatturaElettronicaBody/p:DatiGenerali/p:DatiGeneraliDocumento/p:Causale',
            './/p:DatiGenerali/p:DatiGeneraliDocumento/p:Causale'
        ]
        
        causale = None
        for path in causale_paths:
            causale = root.find(path, self.ns)
            if causale is not None:
                break
        
        if customer_data is None or address_data is None:
            return {
                'denominazione': 'N/D',
                'partita_iva': 'N/D',
                'codice_fiscale': 'N/D',
                'pec': 'N/D',
                'codice_destinatario': 'N/D',
                'indirizzo': 'N/D',
                'cap': 'N/D',
                'citta': 'N/D',
                'provincia': 'N/D',
                'nazione': 'IT',
                'causale': 'N/D'
            }
        
        # Gestione denominazione o nome+cognome
        denominazione = self._safe_find_text(customer_data, './/Denominazione')
        if not denominazione or denominazione == 'N/D':
            nome = self._safe_find_text(customer_data, './/Nome', '')
            cognome = self._safe_find_text(customer_data, './/Cognome', '')
            denominazione = f"{nome} {cognome}".strip() if nome or cognome else 'N/D'
        
        return {
            'denominazione': denominazione,
            'partita_iva': self._safe_find_text(customer_data, './/IdCodice'),
            'codice_fiscale': self._safe_find_text(customer_data, './/CodiceFiscale'),
            'pec': self._safe_find_text(pec_data, './/PECDestinatario') if pec_data is not None else 'N/D',
            'codice_destinatario': self._safe_find_text(root, './/CodiceDestinatario'),
            'indirizzo': self._safe_find_text(address_data, './/Indirizzo'),
            'cap': self._safe_find_text(address_data, './/CAP'),
            'citta': self._safe_find_text(address_data, './/Comune'),
            'provincia': self._safe_find_text(address_data, './/Provincia'),
            'nazione': self._safe_find_text(address_data, './/Nazione', 'IT'),
            'causale': causale.text if causale is not None else 'N/D'
        }
    
    def _parse_items(self, root):
        items = []
        # Prova diversi percorsi possibili per le linee della fattura
        items_paths = [
            './/FatturaElettronicaBody/DatiBeniServizi/DettaglioLinee',
            './/DatiBeniServizi/DettaglioLinee',
            './/p:FatturaElettronicaBody/p:DatiBeniServizi/p:DettaglioLinee',
            './/p:DatiBeniServizi/p:DettaglioLinee'
        ]
        
        for path in items_paths:
            for line in root.findall(path, self.ns):
                # Gestione sicura dei valori numerici
                try:
                    quantita = float(self._safe_find_text(line, './/Quantita', '1'))
                except:
                    quantita = 1.0
                    
                try:
                    prezzo_unitario = float(self._safe_find_text(line, './/PrezzoUnitario', '0'))
                except:
                    prezzo_unitario = 0.0
                    
                try:
                    importo = float(self._safe_find_text(line, './/PrezzoTotale', '0'))
                except:
                    importo = 0.0
                    
                try:
                    aliquota_iva = float(self._safe_find_text(line, './/AliquotaIVA', '0'))
                except:
                    aliquota_iva = 0.0
                
                items.append({
                    'descrizione': self._safe_find_text(line, './/Descrizione'),
                    'quantita': quantita,
                    'prezzo_unitario': prezzo_unitario,
                    'importo': importo,
                    'aliquota_iva': aliquota_iva,
                    'unita_misura': self._safe_find_text(line, './/UnitaMisura', 'N/D'),
                    'codice_articolo': self._safe_find_text(line, './/CodiceArticolo', 'N/D')
                })
            if items:  # Se abbiamo trovato degli elementi, usciamo dal ciclo
                break
        
        return items
    
    def _parse_totals(self, root):
        totals_paths = [
            './/FatturaElettronicaBody/DatiBeniServizi/DatiRiepilogo',
            './/DatiBeniServizi/DatiRiepilogo',
            './/p:FatturaElettronicaBody/p:DatiBeniServizi/p:DatiRiepilogo',
            './/p:DatiBeniServizi/p:DatiRiepilogo'
        ]
        
        totals_elements = []
        for path in totals_paths:
            totals_elements = root.findall(path, self.ns)
            if totals_elements:
                break
        
        if not totals_elements:
            return {
                'imponibile': 0.0,
                'imposta': 0.0,
                'aliquota_iva': 0.0,
                'esigibilita_iva': 'N/D',
                'riferimenti_normativi': 'N/D',
                'spese_accessorie': 0.0,
                'arrotondamento': 0.0,
                'riepilogo_aliquote': []
            }
        
        # Somma tutti i valori dei DatiRiepilogo
        total_imponibile = 0.0
        total_imposta = 0.0
        spese_accessorie = 0.0
        arrotondamento = 0.0
        riepilogo_aliquote = []
        
        for element in totals_elements:
            try:
                imponibile = float(self._safe_find_text(element, './/ImponibileImporto', '0'))
            except:
                imponibile = 0.0
                
            try:
                imposta = float(self._safe_find_text(element, './/Imposta', '0'))
            except:
                imposta = 0.0
                
            try:
                aliquota = float(self._safe_find_text(element, './/AliquotaIVA', '0'))
            except:
                aliquota = 0.0
                
            esigibilita = self._safe_find_text(element, './/EsigibilitaIVA', 'N/D')
            riferimenti = self._safe_find_text(element, './/RiferimentoNormativo', 'N/D')
            
            total_imponibile += imponibile
            total_imposta += imposta
            
            # Aggiungi al riepilogo delle aliquote
            riepilogo_aliquote.append({
                'aliquota': aliquota,
                'imponibile': imponibile,
                'imposta': imposta,
                'esigibilita': esigibilita,
                'riferimenti': riferimenti
            })
        
        # Cerca spese accessorie e arrotondamento
        spese_paths = [
            './/FatturaElettronicaBody/DatiGenerali/DatiGeneraliDocumento/SpeseAccessorie',
            './/DatiGenerali/DatiGeneraliDocumento/SpeseAccessorie'
        ]
        
        for path in spese_paths:
            spese = root.find(path, self.ns)
            if spese is not None:
                try:
                    spese_accessorie = float(spese.text)
                except:
                    spese_accessorie = 0.0
                break
        
        arr_paths = [
            './/FatturaElettronicaBody/DatiGenerali/DatiGeneraliDocumento/Arrotondamento',
            './/DatiGenerali/DatiGeneraliDocumento/Arrotondamento'
        ]
        
        for path in arr_paths:
            arr = root.find(path, self.ns)
            if arr is not None:
                try:
                    arrotondamento = float(arr.text)
                except:
                    arrotondamento = 0.0
                break
        
        return {
            'imponibile': total_imponibile,
            'imposta': total_imposta,
            'spese_accessorie': spese_accessorie,
            'arrotondamento': arrotondamento,
            'riepilogo_aliquote': riepilogo_aliquote
        }
    
    def _parse_payment(self, root):
        """Estrae i dati di pagamento dalla fattura"""
        payment_paths = [
            './/DatiPagamento',
            './/p:DatiPagamento',
            './/FatturaElettronicaBody/DatiPagamento',
            './/p:FatturaElettronicaBody/p:DatiPagamento'
        ]
        
        payment_data = None
        for path in payment_paths:
            payment_data = root.find(path, self.ns)
            if payment_data is not None:
                break
        
        if payment_data is None:
            return {
                'modalita': 'N/D',
                'modalita_desc': 'N/D',
                'termini': 'N/D',
                'termini_desc': 'N/D',
                'iban': 'N/D',
                'scadenza': 'N/D'
            }
        
        # Cerca la data di scadenza
        scadenza = self._safe_find_text(payment_data, './/DataScadenzaPagamento')
        if scadenza:
            try:
                scadenza = datetime.strptime(scadenza, '%Y-%m-%d').strftime('%d/%m/%Y')
            except:
                pass
        
        modalita = self._safe_find_text(payment_data, './/ModalitaPagamento')
        modalita_desc = self.modalita_pagamento.get(modalita, 'N/D')
        
        termini = self._safe_find_text(payment_data, './/CondizioniPagamento')
        termini_desc = self.condizioni_pagamento.get(termini, 'N/D')
        
        return {
            'modalita': modalita,
            'modalita_desc': modalita_desc,
            'termini': termini,
            'termini_desc': termini_desc,
            'iban': self._safe_find_text(payment_data, './/IBAN'),
            'scadenza': scadenza or 'N/D'
        } 