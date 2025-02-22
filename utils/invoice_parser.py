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
        
        return {
            'header': header,
            'supplier': supplier,
            'customer': customer,
            'items': items,
            'totals': totals
        }
    
    def _safe_find_text(self, element, xpath, default='N/D'):
        """Trova in sicurezza un elemento XML e restituisce il suo testo"""
        try:
            found = element.find(xpath, self.ns)
            return found.text if found is not None else default
        except:
            return default
    
    def _parse_header(self, root):
        header_data = root.find('.//FatturaElettronicaHeader/DatiGeneraliDocumento', self.ns)
        if header_data is None:
            header_data = root.find('.//DatiGeneraliDocumento', self.ns)
        
        return {
            'tipo_documento': self._safe_find_text(header_data, './/TipoDocumento'),
            'data': datetime.strptime(
                self._safe_find_text(header_data, './/Data', '2000-01-01'),
                '%Y-%m-%d'
            ).strftime('%d/%m/%Y'),
            'numero': self._safe_find_text(header_data, './/Numero'),
            'divisa': self._safe_find_text(header_data, './/Divisa', 'EUR')
        }
    
    def _parse_supplier(self, root):
        supplier_data = root.find('.//FatturaElettronicaHeader/CedentePrestatore/DatiAnagrafici', self.ns)
        if supplier_data is None:
            supplier_data = root.find('.//CedentePrestatore', self.ns)
        
        address_data = root.find('.//FatturaElettronicaHeader/CedentePrestatore/Sede', self.ns)
        if address_data is None:
            address_data = root.find('.//CedentePrestatore/Sede', self.ns)
        
        return {
            'denominazione': self._safe_find_text(supplier_data, './/Denominazione'),
            'partita_iva': self._safe_find_text(supplier_data, './/IdCodice'),
            'indirizzo': self._safe_find_text(address_data, './/Indirizzo'),
            'cap': self._safe_find_text(address_data, './/CAP'),
            'citta': self._safe_find_text(address_data, './/Comune'),
            'provincia': self._safe_find_text(address_data, './/Provincia')
        }
    
    def _parse_customer(self, root):
        customer_data = root.find('.//FatturaElettronicaHeader/CessionarioCommittente/DatiAnagrafici', self.ns)
        if customer_data is None:
            customer_data = root.find('.//CessionarioCommittente', self.ns)
        
        address_data = root.find('.//FatturaElettronicaHeader/CessionarioCommittente/Sede', self.ns)
        if address_data is None:
            address_data = root.find('.//CessionarioCommittente/Sede', self.ns)
        
        return {
            'denominazione': self._safe_find_text(customer_data, './/Denominazione'),
            'partita_iva': self._safe_find_text(customer_data, './/IdCodice'),
            'indirizzo': self._safe_find_text(address_data, './/Indirizzo'),
            'cap': self._safe_find_text(address_data, './/CAP'),
            'citta': self._safe_find_text(address_data, './/Comune'),
            'provincia': self._safe_find_text(address_data, './/Provincia')
        }
    
    def _parse_items(self, root):
        items = []
        for line in root.findall('.//FatturaElettronicaBody/DatiBeniServizi/DettaglioLinee', self.ns):
            items.append({
                'descrizione': self._safe_find_text(line, './/Descrizione'),
                'quantita': float(self._safe_find_text(line, './/Quantita', '1')),
                'prezzo_unitario': float(self._safe_find_text(line, './/PrezzoUnitario', '0')),
                'importo': float(self._safe_find_text(line, './/PrezzoTotale', '0')),
                'aliquota_iva': float(self._safe_find_text(line, './/AliquotaIVA', '0'))
            })
        return items
    
    def _parse_totals(self, root):
        totals_data = root.find('.//FatturaElettronicaBody/DatiBeniServizi/DatiRiepilogo', self.ns)
        if totals_data is None:
            totals_data = root.find('.//DatiRiepilogo', self.ns)
        
        return {
            'imponibile': float(self._safe_find_text(totals_data, './/ImponibileImporto', '0')),
            'imposta': float(self._safe_find_text(totals_data, './/Imposta', '0')),
            'aliquota_iva': float(self._safe_find_text(totals_data, './/AliquotaIVA', '0'))
        } 