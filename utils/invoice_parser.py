import xml.etree.ElementTree as ET
from datetime import datetime

class InvoiceParser:
    def __init__(self):
        # Namespace utilizzati nelle fatture elettroniche italiane
        self.ns = {
            'p': 'http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2',
            'ds': 'http://www.w3.org/2000/09/xmldsig#',
            'xsi': 'http://www.w3.org/2001/XMLSchema-instance'
        }
    
    def parse_invoice(self, xml_content):
        if isinstance(xml_content, bytes):
            xml_content = xml_content.decode('utf-8')
            
        root = ET.fromstring(xml_content)
        
        # Determina il namespace effettivo dal file
        for key, value in root.attrib.items():
            if value == self.ns['p']:
                self.ns['p'] = root.tag.split('}')[0].strip('{')
                break
        
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
            'payment': payment
        }
    
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
                'data': datetime.now().strftime('%d/%m/%Y'),
                'numero': 'N/D',
                'divisa': 'EUR'
            }
        
        data_str = self._safe_find_text(header_data, './/Data', '2000-01-01')
        try:
            data_formatted = datetime.strptime(data_str, '%Y-%m-%d').strftime('%d/%m/%Y')
        except:
            data_formatted = data_str
            
        return {
            'tipo_documento': self._safe_find_text(header_data, './/TipoDocumento'),
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
                'provincia': 'N/D'
            }
        
        return {
            'denominazione': self._safe_find_text(supplier_data, './/Denominazione') or 
                           self._safe_find_text(supplier_data, './/Nome') + ' ' + 
                           self._safe_find_text(supplier_data, './/Cognome'),
            'partita_iva': self._safe_find_text(supplier_data, './/IdCodice'),
            'id_fiscale_iva': self._safe_find_text(supplier_data, './/IdFiscaleIVA/IdPaese', '') + 
                             self._safe_find_text(supplier_data, './/IdFiscaleIVA/IdCodice', ''),
            'regime_fiscale': self._safe_find_text(supplier_data, './/RegimeFiscale'),
            'indirizzo': self._safe_find_text(address_data, './/Indirizzo'),
            'cap': self._safe_find_text(address_data, './/CAP'),
            'citta': self._safe_find_text(address_data, './/Comune'),
            'provincia': self._safe_find_text(address_data, './/Provincia')
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
                'causale': 'N/D'
            }
        
        return {
            'denominazione': self._safe_find_text(customer_data, './/Denominazione') or 
                           self._safe_find_text(customer_data, './/Nome') + ' ' + 
                           self._safe_find_text(customer_data, './/Cognome'),
            'partita_iva': self._safe_find_text(customer_data, './/IdCodice'),
            'codice_fiscale': self._safe_find_text(customer_data, './/CodiceFiscale'),
            'pec': self._safe_find_text(pec_data, './/PECDestinatario') if pec_data is not None else 'N/D',
            'codice_destinatario': self._safe_find_text(root, './/CodiceDestinatario'),
            'indirizzo': self._safe_find_text(address_data, './/Indirizzo'),
            'cap': self._safe_find_text(address_data, './/CAP'),
            'citta': self._safe_find_text(address_data, './/Comune'),
            'provincia': self._safe_find_text(address_data, './/Provincia'),
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
                items.append({
                    'descrizione': self._safe_find_text(line, './/Descrizione'),
                    'quantita': float(self._safe_find_text(line, './/Quantita', '1')),
                    'prezzo_unitario': float(self._safe_find_text(line, './/PrezzoUnitario', '0')),
                    'importo': float(self._safe_find_text(line, './/PrezzoTotale', '0')),
                    'aliquota_iva': float(self._safe_find_text(line, './/AliquotaIVA', '0'))
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
            imponibile = float(self._safe_find_text(element, './/ImponibileImporto', '0'))
            imposta = float(self._safe_find_text(element, './/Imposta', '0'))
            aliquota = float(self._safe_find_text(element, './/AliquotaIVA', '0'))
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
                spese_accessorie = float(spese.text)
                break
        
        arr_paths = [
            './/FatturaElettronicaBody/DatiGenerali/DatiGeneraliDocumento/Arrotondamento',
            './/DatiGenerali/DatiGeneraliDocumento/Arrotondamento'
        ]
        
        for path in arr_paths:
            arr = root.find(path, self.ns)
            if arr is not None:
                arrotondamento = float(arr.text)
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
                'termini': 'N/D',
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
        
        return {
            'modalita': self._safe_find_text(payment_data, './/ModalitaPagamento'),
            'termini': self._safe_find_text(payment_data, './/CondizioniPagamento'),
            'iban': self._safe_find_text(payment_data, './/IBAN'),
            'scadenza': scadenza or 'N/D'
        } 