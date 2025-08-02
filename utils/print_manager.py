import tempfile
import os
import sys
import pdfkit
from PyQt6.QtPrintSupport import QPrinter, QPrintDialog
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtGui import QTextDocument, QPageSize
from utils.pdf_layout import PDFLayout

class PrintManager:
    def __init__(self, parent=None):
        self.parent = parent

    def print_document(self, invoice_data, signature_html=None):
        """Gestisce il processo di stampa utilizzando il layout PDF"""
        if not invoice_data:
            QMessageBox.warning(self.parent, "Attenzione", "Nessuna fattura caricata da stampare")
            return

        try:
            # Crea il PDF temporaneo usando il layout PDF
            pdf_path = self.create_invoice_pdf(invoice_data)
            
            if not pdf_path:
                QMessageBox.critical(self.parent, "Errore", "Impossibile creare il PDF per la stampa")
                return

            # Verifica se ci sono stampanti disponibili
            available_printers = self._get_available_printers()
            
            if not available_printers:
                # Se non ci sono stampanti, salva il PDF e chiedi all'utente cosa fare
                desktop_path = os.path.expanduser("~/Desktop")
                saved_path = os.path.join(desktop_path, "fattura_stampa.pdf")
                import shutil
                shutil.copy2(pdf_path, saved_path)
                
                from PyQt6.QtWidgets import QMessageBox, QPushButton
                msg_box = QMessageBox(self.parent)
                msg_box.setWindowTitle("Nessuna Stampante Configurata")
                msg_box.setText("Non ci sono stampanti configurate nel sistema.")
                msg_box.setInformativeText(f"Il PDF è stato salvato su Desktop come 'fattura_stampa.pdf'")
                
                # Aggiungi pulsanti personalizzati
                open_button = QPushButton("Apri PDF")
                ok_button = QPushButton("OK")
                msg_box.addButton(open_button, QMessageBox.ButtonRole.ActionRole)
                msg_box.addButton(ok_button, QMessageBox.ButtonRole.AcceptRole)
                
                msg_box.exec()
                
                if msg_box.clickedButton() == open_button:
                    # Apri il PDF con l'applicazione di default
                    self._open_pdf(saved_path)
                
                return

            # Configura la stampante
            printer = QPrinter()
            printer.setPageSize(QPageSize(QPageSize.PageSizeId.A4))
            
            # Mostra il dialogo di stampa
            dialog = QPrintDialog(printer, self.parent)
            if dialog.exec() == QPrintDialog.DialogCode.Accepted:
                # Stampa il PDF usando un comando di sistema
                self.print_pdf_file(pdf_path, printer)
                QMessageBox.information(self.parent, "Successo", "Stampa avviata con successo")

        except Exception as e:
            QMessageBox.critical(self.parent, "Errore", f"Errore durante la stampa: {str(e)}")
        finally:
            # Pulisci il file temporaneo
            if 'pdf_path' in locals() and pdf_path and os.path.exists(pdf_path):
                try:
                    os.unlink(pdf_path)
                except:
                    pass  # Ignora errori di pulizia

    def create_invoice_pdf(self, invoice_data):
        """Crea il PDF della fattura usando il layout PDF"""
        try:
            # Genera il contenuto HTML usando il layout PDF
            pdf_layout = PDFLayout()
            html_content = pdf_layout.generate_invoice_html(invoice_data)
            
            # Trova il percorso di wkhtmltopdf
            wkhtmltopdf_path = self._find_wkhtmltopdf()
            
            if not wkhtmltopdf_path:
                QMessageBox.critical(self.parent, "Errore", 
                    "wkhtmltopdf non trovato. Installalo da: https://wkhtmltopdf.org/downloads.html")
                return None
            
            # Crea un file temporaneo per il PDF
            with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp_file:
                pdf_path = tmp_file.name
            
            # Configura pdfkit per utilizzare wkhtmltopdf
            config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)
            
            # Opzioni per la stampa
            options = {
                'quiet': '',
                'page-size': 'A4',
                'margin-top': '20mm',
                'margin-right': '20mm',
                'margin-bottom': '20mm',
                'margin-left': '20mm',
                'encoding': 'UTF-8',
                'no-outline': None,
                'enable-local-file-access': None
            }
            
            # Genera il PDF
            pdfkit.from_string(html_content, pdf_path, configuration=config, options=options)
            
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
                    os.system(f'lpr -P "{printer_name}" "{pdf_path}"')
                else:
                    # Prova a trovare una stampante disponibile
                    available_printers = self._get_available_printers()
                    if available_printers:
                        # Usa la prima stampante disponibile
                        first_printer = available_printers[0]
                        os.system(f'lpr -P "{first_printer}" "{pdf_path}"')
                    else:
                        # Se non ci sono stampanti, salva il PDF e informa l'utente
                        desktop_path = os.path.expanduser("~/Desktop")
                        saved_path = os.path.join(desktop_path, "fattura_stampa.pdf")
                        import shutil
                        shutil.copy2(pdf_path, saved_path)
                        raise Exception(f"Nessuna stampante configurata. Il PDF è stato salvato su Desktop come 'fattura_stampa.pdf'")
                    
            elif sys.platform == 'win32':  # Windows
                # Su Windows, usa il comando print
                os.system(f'print "{pdf_path}"')
                
            else:  # Linux
                # Su Linux, usa lpr
                printer_name = printer.printerName()
                if printer_name:
                    os.system(f'lpr -P "{printer_name}" "{pdf_path}"')
                else:
                    os.system(f'lpr "{pdf_path}"')
                    
        except Exception as e:
            raise Exception(f"Errore durante l'invio alla stampante: {str(e)}")

    def _get_available_printers(self):
        """Ottiene la lista delle stampanti disponibili su macOS"""
        try:
            import subprocess
            # Usa lpstat per ottenere le stampanti disponibili
            result = subprocess.run(['lpstat', '-p'], capture_output=True, text=True)
            if result.returncode == 0:
                printers = []
                for line in result.stdout.split('\n'):
                    if line.startswith('printer'):
                        # Estrai il nome della stampante dalla riga "printer NOME is ..."
                        parts = line.split()
                        if len(parts) >= 2:
                            printer_name = parts[1]
                            printers.append(printer_name)
                return printers
            else:
                return []
        except:
            return []

    def _find_wkhtmltopdf(self):
        """Trova il percorso dell'eseguibile wkhtmltopdf."""
        import subprocess
        import shutil
        
        # Se l'app è in bundle, prova prima nella directory bin del bundle
        if getattr(sys, 'frozen', False):
            bundle_dir = sys._MEIPASS
            bundle_path = os.path.join(bundle_dir, 'bin', 'wkhtmltopdf')
            if os.path.exists(bundle_path) and os.access(bundle_path, os.X_OK):
                return bundle_path
        
        # Prova nella directory bin locale (sviluppo)
        local_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'bin', 'wkhtmltopdf')
        if os.path.exists(local_path) and os.access(local_path, os.X_OK):
            return local_path
        
        # Se non è nel bundle, prova a trovare wkhtmltopdf nel PATH del sistema
        wkhtmltopdf_path = shutil.which('wkhtmltopdf')
        if wkhtmltopdf_path:
            return wkhtmltopdf_path
        
        # Se non è nel PATH, prova percorsi comuni su macOS
        common_paths = [
            '/usr/local/bin/wkhtmltopdf',
            '/opt/homebrew/bin/wkhtmltopdf',
            '/usr/bin/wkhtmltopdf'
        ]
        
        for path in common_paths:
            if os.path.exists(path) and os.access(path, os.X_OK):
                return path
        
        return None

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