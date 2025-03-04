import tempfile
import os
import sys
from PyQt6.QtPrintSupport import QPrinter, QPrintDialog
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtGui import QTextDocument, QPageSize
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak

class PrintManager:
    def __init__(self, parent=None):
        self.parent = parent

    def print_document(self, invoice_data, signature_html=None):
        """Gestisce il processo di stampa con layout professionale"""
        if not invoice_data:
            return

        try:
            # Crea il PDF con ReportLab
            pdf_path = self.create_invoice_pdf(invoice_data)

            # Configura la stampante
            printer = QPrinter()
            printer.setPageSize(QPageSize(QPageSize.PageSizeId.A4))
            
            # Mostra il dialogo di stampa
            dialog = QPrintDialog(printer, self.parent)
            if dialog.exec() == QPrintDialog.DialogCode.Accepted:
                # Stampa il PDF usando un comando di sistema
                if sys.platform == 'darwin':  # macOS
                    os.system(f'lpr "{pdf_path}"')
                elif sys.platform == 'win32':  # Windows
                    os.system(f'print "{pdf_path}"')
                else:  # Linux
                    os.system(f'lpr "{pdf_path}"')

        except Exception as e:
            QMessageBox.critical(self.parent, "Errore", f"Errore durante la stampa: {str(e)}")
        finally:
            # Pulisci il file temporaneo
            if 'pdf_path' in locals():
                os.unlink(pdf_path)

    def create_invoice_pdf(self, invoice_data):
        """Crea il PDF della fattura usando ReportLab"""
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp_file:
            doc = SimpleDocTemplate(
                tmp_file.name,
                pagesize=A4,
                rightMargin=20*mm,
                leftMargin=20*mm,
                topMargin=20*mm,
                bottomMargin=20*mm
            )

            elements = []
            styles = getSampleStyleSheet()
            
            # Stili personalizzati
            styles.add(ParagraphStyle(
                name='BoxTitle',
                parent=styles['Heading2'],
                fontSize=10,
                spaceAfter=3*mm
            ))
            
            # Header con dati fornitore e cliente
            header_data = [
                [Paragraph("Cedente/prestatore (fornitore)", styles['BoxTitle']),
                 Paragraph("Cessionario/committente (cliente)", styles['BoxTitle'])],
                [
                    # Dati fornitore
                    Paragraph(f"{invoice_data['supplier']['denominazione']}<br/>"
                            f"Regime fiscale: {invoice_data['supplier']['regime_fiscale']}<br/>"
                            f"Indirizzo: {invoice_data['supplier']['indirizzo']}<br/>"
                            f"Comune: {invoice_data['supplier']['citta']} Provincia: {invoice_data['supplier']['provincia']}<br/>"
                            f"Cap: {invoice_data['supplier']['cap']} Nazione: IT", styles['Normal']),
                    # Dati cliente
                    Paragraph(f"Codice fiscale: {invoice_data['customer']['codice_fiscale']}<br/>"
                            f"Denominazione: {invoice_data['customer']['denominazione']}<br/>"
                            f"Indirizzo: {invoice_data['customer']['indirizzo']}<br/>"
                            f"Comune: {invoice_data['customer']['citta']} Provincia: {invoice_data['customer']['provincia']}<br/>"
                            f"Cap: {invoice_data['customer']['cap']} Nazione: IT<br/>"
                            f"Email: {invoice_data['customer']['pec']}", styles['Normal'])
                ]
            ]
            
            header_table = Table(header_data, colWidths=[90*mm, 90*mm])
            header_table.setStyle(TableStyle([
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ]))
            elements.append(header_table)
            elements.append(Spacer(1, 10*mm))

            # Dati documento
            doc_data = [[
                Paragraph("Tipologia documento", styles['BoxTitle']),
                Paragraph("Numero documento", styles['BoxTitle']),
                Paragraph("Data", styles['BoxTitle']),
                Paragraph("Codice destinatario", styles['BoxTitle'])
            ], [
                invoice_data['header']['tipo_documento'],
                invoice_data['header']['numero'],
                invoice_data['header']['data'],
                invoice_data['customer']['codice_destinatario']
            ]]
            
            doc_table = Table(doc_data, colWidths=[45*mm, 45*mm, 45*mm, 45*mm])
            doc_table.setStyle(TableStyle([
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ]))
            elements.append(doc_table)
            elements.append(Spacer(1, 10*mm))

            # Tabella articoli
            items_data = [
                ['Cod. articolo', 'Descrizione', 'Quantità', 'Prezzo unitario', 'UM', '%IVA', 'Prezzo totale']
            ]
            
            # Aggiungi righe per ogni articolo
            for item in invoice_data['items']:
                row = [
                    str(item.get('codice', '')),
                    Paragraph(str(item['descrizione']), styles['Normal']),  # Usa Paragraph per il wrapping del testo
                    str(item['quantita']),
                    f"{item['prezzo_unitario']:.4f}",
                    str(item.get('um', 'PZ')),
                    str(item['aliquota_iva']),
                    f"{item['importo']:.2f}"
                ]
                items_data.append(row)

            # Crea la tabella articoli con le proporzioni corrette
            items_table = Table(items_data, colWidths=[25*mm, 65*mm, 20*mm, 25*mm, 15*mm, 15*mm, 25*mm])
            
            # Stile della tabella articoli
            items_style = TableStyle([
                # Bordi
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('BOX', (0, 0), (-1, -1), 2, colors.black),
                
                # Header
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                
                # Contenuto
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('ALIGN', (2, 1), (-1, -1), 'RIGHT'),  # Allinea a destra i numeri
                ('ALIGN', (0, 1), (1, -1), 'LEFT'),    # Allinea a sinistra codice e descrizione
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ])
            
            items_table.setStyle(items_style)
            elements.append(items_table)
            elements.append(Spacer(1, 10*mm))

            # Riepilogo IVA su nuova pagina
            elements.append(PageBreak())
            elements.append(Paragraph("RIEPILOGHI IVA E TOTALI", styles['Heading1']))
            
            # Tabella riepilogo IVA
            data = [
                ['esigibilità iva / riferimenti normativi', '%IVA', 'Spese\naccessorie', 'Arr.', 'Totale imponibile', 'Totale imposta']
            ]
            
            # Aggiungi righe per ogni aliquota
            for aliquota in invoice_data['totals']['riepilogo_aliquote']:
                row = [
                    'Esigib. non dich. (si presume immediata)',
                    f"{aliquota['aliquota']:.2f}",
                    '',  # Spese accessorie
                    '0,00',  # Arrotondamento
                    f"{aliquota['imponibile']:.2f}",
                    f"{aliquota['imposta']:.2f}"
                ]
                data.append(row)

            # Riga finale
            totale = (invoice_data['totals']['imponibile'] + 
                     invoice_data['totals']['imposta'] + 
                     invoice_data['totals']['spese_accessorie'] + 
                     invoice_data['totals']['arrotondamento'])

            data.append([
                'Imposta bollo',
                {'span': (1, 2), 'content': 'Sconto/Maggiorazione'},
                None,  # Questa cella viene unita con la precedente
                'Arr.',
                {'span': (4, 5), 'content': f'Totale documento: {totale:.2f}'},
                None  # Questa cella viene unita con la precedente
            ])

            # Crea la tabella con le proporzioni corrette
            col_widths = [70*mm, 20*mm, 25*mm, 15*mm, 30*mm, 30*mm]
            table = Table(data, colWidths=col_widths, repeatRows=1)
            
            # Stile della tabella
            table_style = TableStyle([
                # Bordi
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('BOX', (0, 0), (-1, -1), 2, colors.black),
                
                # Allineamenti
                ('ALIGN', (0, 0), (0, -1), 'LEFT'),  # Prima colonna a sinistra
                ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),  # Altre colonne a destra
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                
                # Header
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                
                # Contenuto
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 10),
                
                # Unisci celle nell'ultima riga
                ('SPAN', (1, -1), (2, -1)),  # Unisci celle per Sconto/Maggiorazione
                ('SPAN', (4, -1), (5, -1)),  # Unisci celle per Totale documento
            ])
            
            table.setStyle(table_style)
            elements.append(table)
            
            # Genera il PDF
            doc.build(elements)
            return tmp_file.name 