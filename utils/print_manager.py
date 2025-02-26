import tempfile
import os
import sys
from PyQt6.QtPrintSupport import QPrinter, QPrintDialog
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtGui import QTextDocument, QPageSize, QPageLayout, QPainter, QFont
from PyQt6.QtCore import QMarginsF, Qt, QRectF
import pdfkit
from utils.pdf_layout import PDFLayout

class PrintManager:
    def __init__(self, parent=None):
        self.parent = parent

    def print_document(self, invoice_data, signature_html=None):
        """Gestisce il processo di stampa con layout professionale"""
        if not invoice_data:
            return

        printer = QPrinter()
        printer.setPageSize(QPageSize(QPageSize.PageSizeId.A4))
        printer.setPageMargins(QMarginsF(0, 0, 0, 0), QPageLayout.Unit.Millimeter)

        dialog = QPrintDialog(printer, self.parent)
        if dialog.exec() == QPrintDialog.DialogCode.Accepted:
            try:
                painter = QPainter()
                painter.begin(printer)

                # Imposta i font
                titleFont = QFont("Arial", 11, QFont.Weight.Bold)
                headerFont = QFont("Arial", 11, QFont.Weight.Bold)
                normalFont = QFont("Arial", 11)

                # Area di stampa
                pageRect = printer.pageRect(QPrinter.Unit.DevicePixel)
                width = int(pageRect.width())
                currentY = 20  # Margine superiore iniziale

                # Titolo
                painter.setFont(titleFont)
                painter.fillRect(0, currentY - 10, width, 40, Qt.GlobalColor.lightGray)
                painter.drawText(0, currentY, width, 30, Qt.AlignmentFlag.AlignCenter, "FATTURA ELETTRONICA")
                currentY += 40

                # Numero fattura e data
                painter.setFont(normalFont)
                text = f"Numero: {invoice_data['header']['numero']} del {invoice_data['header']['data']}\n"
                text += f"Tipo documento: {invoice_data['header']['tipo_documento']}"
                painter.drawText(50, currentY, width - 100, 40, Qt.AlignmentFlag.AlignLeft, text)
                currentY += 60

                # Cedente e Cessionario affiancati
                painter.setFont(headerFont)
                leftCol = 50
                rightCol = int(width / 2 + 50)
                colWidth = int(width / 2 - 100)

                # Cedente
                painter.fillRect(leftCol - 5, currentY - 5, colWidth + 10, 35, Qt.GlobalColor.lightGray)
                painter.drawText(leftCol, currentY, colWidth, 30, Qt.AlignmentFlag.AlignLeft, "CEDENTE/PRESTATORE")
                painter.setFont(normalFont)
                text = f"Denominazione: {invoice_data['supplier']['denominazione']}\n"
                text += f"Partita IVA: {invoice_data['supplier']['partita_iva']}\n"
                text += f"Indirizzo: {invoice_data['supplier']['indirizzo']}\n"
                text += f"{invoice_data['supplier']['cap']} {invoice_data['supplier']['citta']} ({invoice_data['supplier']['provincia']})"
                painter.drawText(leftCol, currentY + 30, colWidth, 80, Qt.AlignmentFlag.AlignLeft, text)

                # Cessionario
                painter.setFont(headerFont)
                painter.fillRect(rightCol - 5, currentY - 5, colWidth + 10, 35, Qt.GlobalColor.lightGray)
                painter.drawText(rightCol, currentY, colWidth, 30, Qt.AlignmentFlag.AlignLeft, "CESSIONARIO/COMMITTENTE")
                painter.setFont(normalFont)
                text = f"Denominazione: {invoice_data['customer']['denominazione']}\n"
                text += f"Partita IVA: {invoice_data['customer']['partita_iva']}\n"
                text += f"Indirizzo: {invoice_data['customer']['indirizzo']}\n"
                text += f"{invoice_data['customer']['cap']} {invoice_data['customer']['citta']} ({invoice_data['customer']['provincia']})"
                painter.drawText(rightCol, currentY + 30, colWidth, 80, Qt.AlignmentFlag.AlignLeft, text)

                currentY += 130  # Spazio dopo cedente e cessionario

                # Tabella dati
                painter.setFont(headerFont)
                painter.drawText(50, currentY, width - 100, 30, Qt.AlignmentFlag.AlignLeft, "DATI BENI/SERVIZI")
                currentY += 30

                # Intestazione tabella
                colWidths = [int(width * 0.4), int(width * 0.1), int(width * 0.15), int(width * 0.15), int(width * 0.1)]
                headers = ["Descrizione", "Quantità", "Prezzo Unit.", "Importo", "IVA %"]
                x = 50
                for i, header in enumerate(headers):
                    painter.fillRect(x, currentY, colWidths[i], 30, Qt.GlobalColor.lightGray)  # Righe grigie
                    painter.drawText(x, currentY, colWidths[i], 30, Qt.AlignmentFlag.AlignLeft, header)
                    x += colWidths[i]
                currentY += 30

                # Righe tabella
                painter.setFont(normalFont)
                for item in invoice_data['items']:
                    x = 50
                    painter.drawText(x, currentY, colWidths[0], 20, Qt.AlignmentFlag.AlignLeft, str(item['descrizione']))
                    x += colWidths[0]
                    painter.drawText(x, currentY, colWidths[1], 20, Qt.AlignmentFlag.AlignRight, str(item['quantita']))
                    x += colWidths[1]
                    painter.drawText(x, currentY, colWidths[2], 20, Qt.AlignmentFlag.AlignRight, f"€ {item['prezzo_unitario']:.2f}")
                    x += colWidths[2]
                    painter.drawText(x, currentY, colWidths[3], 20, Qt.AlignmentFlag.AlignRight, f"€ {item['importo']:.2f}")
                    x += colWidths[3]
                    painter.drawText(x, currentY, colWidths[4], 20, Qt.AlignmentFlag.AlignRight, f"{item['aliquota_iva']}%")
                    currentY += 20

                # Totali
                currentY += 20
                totaleWidth = 200
                x = width - totaleWidth - 50
                painter.setFont(headerFont)
                painter.fillRect(x - 5, currentY - 5, totaleWidth + 10, 65, Qt.GlobalColor.lightGray)  # Righe grigie
                painter.drawText(x, currentY, totaleWidth, 20, Qt.AlignmentFlag.AlignRight, f"Imponibile: € {invoice_data['totals']['imponibile']:.2f}")
                currentY += 20
                painter.drawText(x, currentY, totaleWidth, 20, Qt.AlignmentFlag.AlignRight, f"IVA: € {invoice_data['totals']['imposta']:.2f}")
                currentY += 20
                totale = invoice_data['totals']['imponibile'] + invoice_data['totals']['imposta']
                painter.drawText(x, currentY, totaleWidth, 20, Qt.AlignmentFlag.AlignRight, f"Totale: € {totale:.2f}")

                painter.end()

            except Exception as e:
                QMessageBox.critical(self.parent, "Errore", f"Errore durante la stampa: {str(e)}")

    def _create_temp_pdf(self, invoice_data, signature_html=None):
        """Crea un PDF temporaneo usando wkhtmltopdf"""
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp_file:
            temp_pdf_path = tmp_file.name

        # Genera HTML usando PDFLayout
        pdf_layout = PDFLayout()
        html_content = pdf_layout.generate_invoice_html(invoice_data)
        
        # Aggiungi firma se presente
        if signature_html:
            html_content = html_content.replace('</body></html>', f'{signature_html}</body></html>')

        # Configura wkhtmltopdf
        if getattr(sys, 'frozen', False):
            bundle_dir = sys._MEIPASS
            wkhtmltopdf_path = os.path.join(bundle_dir, 'bin', 'wkhtmltopdf')
        else:
            wkhtmltopdf_path = 'bin/wkhtmltopdf'

        # Genera il PDF
        config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)
        pdfkit.from_string(html_content, temp_pdf_path, configuration=config, options={'quiet': ''})

        return temp_pdf_path

    def _print_pdf(self, pdf_path, printer):
        """Stampa il PDF temporaneo"""
        document = QTextDocument()
        with open(pdf_path, 'rb') as pdf_file:
            document.setHtml(f'<embed src="file://{pdf_path}" type="application/pdf" width="100%" height="100%">')
        document.print(printer) 