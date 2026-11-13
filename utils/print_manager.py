import tempfile
import os
import sys
from PyQt6.QtCore import QMarginsF, QEventLoop, QTimer, QUrl
from PyQt6.QtPrintSupport import QPrinter, QPrintDialog
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtGui import QPageSize, QPageLayout
# NB: QtWebEngineCore deve essere importato prima della creazione di QApplication
from PyQt6.QtWebEngineCore import QWebEnginePage
from utils.pdf_layout import PDFLayout

# CSS aggiuntivo applicato solo in fase di stampa/PDF
_PRINT_CSS = """
<style>
    @media print {
        * { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
        body { margin: 0 !important; font-size: 12px; }
        .container { border: none !important; padding: 0 !important; max-width: none !important; }
        .section { margin: 10px 0 !important; padding: 10px !important; }
        .section h2 { break-after: avoid; page-break-after: avoid; }
        .grid-container, tr, .info-group, .totali, .payment-info { break-inside: avoid; page-break-inside: avoid; }
        thead { display: table-header-group; }
        th, td { font-size: 11px !important; padding: 5px 6px !important; }
        td { white-space: nowrap; }
        td:first-child { white-space: normal; }
    }
</style>
"""


def html_to_pdf(html_content, pdf_path, timeout_ms=30000):
    """Converte HTML in PDF con Qt WebEngine (Chromium, nativo arm64).

    Supporta CSS moderno (grid, flex) e restituisce True se il PDF è stato creato.
    """
    if '</head>' in html_content:
        html_content = html_content.replace('</head>', _PRINT_CSS + '</head>', 1)
    else:
        html_content = _PRINT_CSS + html_content

    page = QWebEnginePage()
    loop = QEventLoop()
    state = {'ok': False, 'error': None}

    page_layout = QPageLayout(
        QPageSize(QPageSize.PageSizeId.A4),
        QPageLayout.Orientation.Portrait,
        QMarginsF(15, 15, 15, 15),
        QPageLayout.Unit.Millimeter,
    )

    def on_load_finished(ok):
        if not ok:
            state['error'] = "Impossibile caricare il contenuto della fattura"
            loop.quit()
            return
        page.printToPdf(pdf_path, page_layout)

    def on_pdf_finished(_path, ok):
        state['ok'] = ok
        if not ok:
            state['error'] = "Generazione del PDF non riuscita"
        loop.quit()

    def on_timeout():
        state['error'] = "Timeout durante la generazione del PDF"
        loop.quit()

    page.loadFinished.connect(on_load_finished)
    page.pdfPrintingFinished.connect(on_pdf_finished)
    QTimer.singleShot(timeout_ms, on_timeout)

    page.setHtml(html_content, QUrl("file:///"))
    loop.exec()
    page.loadFinished.disconnect()
    page.pdfPrintingFinished.disconnect()
    del page  # distrugge subito la pagina (evita warning sul profilo all'uscita)

    if not state['ok']:
        raise RuntimeError(state['error'] or "Errore sconosciuto nella generazione del PDF")
    return True


class PrintManager:
    def __init__(self, parent=None):
        self.parent = parent

    def print_document(self, invoice_data, html_content=None):
        """Gestisce il processo di stampa utilizzando il layout PDF"""
        if not invoice_data:
            QMessageBox.warning(self.parent, "Attenzione", "Nessuna fattura caricata da stampare")
            return

        try:
            # Crea il PDF temporaneo usando il layout PDF
            pdf_path = self.create_invoice_pdf(invoice_data, html_content)
            
            if not pdf_path:
                QMessageBox.critical(self.parent, "Errore", "Impossibile creare il PDF per la stampa")
                return

            # Configura la stampante
            printer = QPrinter()
            printer.setPageSize(QPageSize(QPageSize.PageSizeId.A4))
            
            # Mostra il dialogo di stampa
            dialog = QPrintDialog(printer, self.parent)
            if dialog.exec() == QPrintDialog.DialogCode.Accepted:
                # Prova a stampare il PDF
                try:
                    self.print_pdf_file(pdf_path, printer)
                    QMessageBox.information(self.parent, "Successo", "Stampa avviata con successo")
                except Exception as print_error:
                    # Se la stampa fallisce, salva il PDF e informa l'utente
                    self._handle_print_failure(pdf_path, str(print_error))

        except Exception as e:
            QMessageBox.critical(self.parent, "Errore", f"Errore durante la stampa: {str(e)}")
        finally:
            # Pulisci il file temporaneo
            if 'pdf_path' in locals() and pdf_path and os.path.exists(pdf_path):
                try:
                    os.unlink(pdf_path)
                except:
                    pass  # Ignora errori di pulizia

    def create_invoice_pdf(self, invoice_data, html_content=None):
        """Crea il PDF della fattura usando il layout PDF"""
        try:
            # Genera il contenuto HTML usando il layout PDF (se non già fornito)
            if not html_content:
                html_content = PDFLayout().generate_invoice_html(invoice_data)
            
            # Crea un file temporaneo per il PDF
            with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp_file:
                pdf_path = tmp_file.name
            
            # Genera il PDF con il motore nativo di Qt
            html_to_pdf(html_content, pdf_path)
            
            return pdf_path
            
        except Exception as e:
            QMessageBox.critical(self.parent, "Errore", f"Errore durante la creazione del PDF: {str(e)}")
            return None

    def print_pdf_file(self, pdf_path, printer):
        """Stampa il file PDF usando il sistema operativo"""
        try:
            if sys.platform == 'darwin':  # macOS
                # Ottieni il nome della stampante dal dialog
                printer_name = printer.printerName()
                
                if printer_name and printer_name != "Default":
                    # Usa la stampante specifica selezionata
                    result = os.system(f'lpr -P "{printer_name}" "{pdf_path}"')
                else:
                    # Usa la stampante di default
                    result = os.system(f'lpr "{pdf_path}"')
                
                # Controlla se il comando è fallito
                if result != 0:
                    raise Exception("Comando lpr fallito")
                    
            elif sys.platform == 'win32':  # Windows
                # Su Windows, usa il comando print
                result = os.system(f'print "{pdf_path}"')
                if result != 0:
                    raise Exception("Comando print fallito")
                
            else:  # Linux
                # Su Linux, usa lpr
                printer_name = printer.printerName()
                if printer_name:
                    result = os.system(f'lpr -P "{printer_name}" "{pdf_path}"')
                else:
                    result = os.system(f'lpr "{pdf_path}"')
                
                if result != 0:
                    raise Exception("Comando lpr fallito")
                    
        except Exception as e:
            raise Exception(f"Errore durante l'invio alla stampante: {str(e)}")

    def _open_pdf(self, pdf_path):
        """Apre il PDF con l'applicazione di default"""
        try:
            if sys.platform == 'darwin':  # macOS
                os.system(f'open "{pdf_path}"')
            elif sys.platform == 'win32':  # Windows
                os.system(f'start "{pdf_path}"')
            else:  # Linux
                os.system(f'xdg-open "{pdf_path}"')
        except Exception as e:
            QMessageBox.warning(self.parent, "Attenzione", f"Impossibile aprire il PDF: {str(e)}") 

    def _handle_print_failure(self, pdf_path, error_message):
        """Gestisce il fallimento della stampa salvando il PDF"""
        try:
            # Salva il PDF sul Desktop
            desktop_path = os.path.expanduser("~/Desktop")
            saved_path = os.path.join(desktop_path, "fattura_stampa.pdf")
            import shutil
            shutil.copy2(pdf_path, saved_path)
            
            # Mostra dialog con opzioni
            from PyQt6.QtWidgets import QMessageBox, QPushButton
            msg_box = QMessageBox(self.parent)
            msg_box.setWindowTitle("Errore di Stampa")
            msg_box.setText("Impossibile inviare il documento alla stampante.")
            msg_box.setInformativeText(f"Errore: {error_message}\n\nIl PDF è stato salvato su Desktop come 'fattura_stampa.pdf'")
            
            # Aggiungi pulsanti personalizzati
            open_button = QPushButton("Apri PDF")
            ok_button = QPushButton("OK")
            msg_box.addButton(open_button, QMessageBox.ButtonRole.ActionRole)
            msg_box.addButton(ok_button, QMessageBox.ButtonRole.AcceptRole)
            
            msg_box.exec()
            
            if msg_box.clickedButton() == open_button:
                # Apri il PDF con l'applicazione di default
                self._open_pdf(saved_path)
                
        except Exception as e:
            QMessageBox.critical(self.parent, "Errore", f"Errore durante il salvataggio del PDF: {str(e)}") 