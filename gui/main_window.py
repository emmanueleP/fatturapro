from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                           QPushButton, QFileDialog, QTextEdit, QMenuBar, QMenu, QMessageBox, QHBoxLayout)
from PyQt6.QtCore import Qt, QSizeF, QMarginsF
from PyQt6.QtGui import QAction, QKeySequence, QDragEnterEvent, QDropEvent, QPageSize, QPageLayout
import xml.etree.ElementTree as ET
from pathlib import Path
from PyQt6.QtPrintSupport import QPrinter, QPrintDialog
from PyQt6.QtGui import QTextDocument
from utils.invoice_parser import InvoiceParser
import json
from utils.p7m_handler import P7MHandler
from gui.info_dialog import InfoDialog
from gui.settings_dialog import SettingsDialog
from utils.pdf_layout import PDFLayout
import pdfkit
import os
import sys
import tempfile
from utils.print_manager import PrintManager
from utils.menu_manager import MenuManager  # Importa il MenuManager
from gui.manual_dialog import ManualDialog  # Importa il ManualDialog

class MainWindow(QMainWindow):
    def __init__(self, theme_manager):
        super().__init__()
        self.theme_manager = theme_manager
        self.print_manager = PrintManager(self)  # Crea il PrintManager
        self.setup_ui()
        self.setAcceptDrops(True)  # Abilita drag & drop
        
        # Crea il menu
        self.menu_manager = MenuManager(self)  # Crea il MenuManager
        self.setMenuBar(self.menu_manager.get_menu_bar())  # Imposta la barra dei menu
        
    def setup_ui(self):
        self.setWindowTitle("FatturaPro - Visualizzatore Fatture Elettroniche")
        self.setMinimumSize(800, 600)
        
        # Widget centrale
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principale
        layout = QVBoxLayout(central_widget)
        
        # Aggiorna lo stile dei pulsanti
        button_style = """
            QPushButton {
                padding: 12px 20px;
                border-radius: 6px;
                background-color: #4a90e2;
                color: white;
                font-weight: bold;
                border: none;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #357abd;
            }
            QPushButton:pressed {
                background-color: #2d5986;
            }
        """
        
        # Area pulsanti in layout orizzontale
        button_layout = QHBoxLayout()
        
        self.btn_open = QPushButton("📂 Apri Fattura")
        self.btn_save_pdf = QPushButton("💾 Salva PDF")
        self.btn_print = QPushButton("🖨️ Stampa")
        
        # Applica stile ai pulsanti
        for btn in [self.btn_open, self.btn_save_pdf, self.btn_print]:
            btn.setStyleSheet(button_style)
            button_layout.addWidget(btn)
        
        # Area di visualizzazione
        self.viewer = QTextEdit()
        self.viewer.setReadOnly(True)
        # Forza lo sfondo bianco per il viewer e stile macOS
        self.viewer.setStyleSheet("""
            QTextEdit {
                background-color: white;
                color: black;
                border: 1px solid #cccccc;
                border-radius: 8px;  /* Più arrotondato per lo stile macOS */
                padding: 10px;
                margin-top: 10px;
            }
            QScrollBar:vertical {
                border: none;
                background: transparent;
                width: 14px;
                margin: 0;
            }
            QScrollBar::handle:vertical {
                background-color: #a1a1a1;
                min-height: 30px;
                border-radius: 7px;
                margin: 2px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #7d7d7d;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
        """)
        
        # Aggiungi i pulsanti e il viewer al layout
        layout.addLayout(button_layout)
        layout.addWidget(self.viewer)

        # Collega i pulsanti alle funzioni
        self.btn_open.clicked.connect(self.open_invoice)
        self.btn_save_pdf.clicked.connect(self.save_as_pdf)
        self.btn_print.clicked.connect(self.print_invoice)

    def show_info(self):
        info_dialog = InfoDialog(self)
        info_dialog.exec()
    
    def show_settings(self):
        dialog = SettingsDialog(self.theme_manager, self)
        dialog.exec()
    
    def show_manual(self):
        manual_dialog = ManualDialog(self)
        manual_dialog.exec()
        
    def open_file(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Seleziona Fattura XML",
            "",
            "File XML (*.xml);;File P7M (*.p7m)"
        )
        if file_name:
            self.load_xml(file_name)
            
    def load_xml(self, file_path):
        try:
            with open(file_path, 'rb') as file:
                content = file.read()
            
            # Verifica se il file è un P7M
            if file_path.lower().endswith('.p7m'):
                p7m_handler = P7MHandler()
                # Estrai il contenuto XML e le info sul firmatario
                xml_content = p7m_handler.extract_xml_from_p7m(content)
                signer_info = p7m_handler.get_signer_info(content)
                
                # Aggiungi le informazioni sulla firma al viewer
                signature_html = self._format_signature_info(signer_info)
            else:
                xml_content = content.decode('utf-8')
                signature_html = ""
            
            parser = InvoiceParser()
            self.current_invoice_data = parser.parse_invoice(xml_content)  # Salva i dati
            
            # Usa PDFLayout per generare l'HTML
            pdf_layout = PDFLayout()
            html_content = pdf_layout.generate_invoice_html(self.current_invoice_data)
            
            # Aggiungi le informazioni sulla firma se presenti
            if signature_html:
                html_content = html_content.replace('</body></html>', f'{signature_html}</body></html>')
            
            self.viewer.setHtml(html_content)
            
        except Exception as e:
            self.viewer.setText(f"Errore nel caricamento del file: {str(e)}")
    
    def _format_invoice_html(self, invoice_data):
        html = f"""
        <html>
        <head>
            <style>
                body {{
                    font-family: -apple-system, BlinkMacSystemFont, Arial, sans-serif;
                    margin: 20px;
                    color: #333;
                    line-height: 1.4;
                }}
                .container {{
                    max-width: 1000px;
                    margin: 0 auto;
                    border: 1px solid #ddd;
                    padding: 20px;
                    border-radius: 5px;
                    background: #fff;
                }}
                .header {{
                    border-bottom: 2px solid #1a75ff;
                    padding-bottom: 10px;
                    margin-bottom: 20px;
                }}
                .header h1 {{
                    color: #1a75ff;
                    font-size: 24px;
                    margin: 0;
                    padding: 0;
                }}
                .header .tipo-doc {{
                    color: #666;
                    font-size: 14px;
                    margin-top: 5px;
                }}
                .section {{
                    margin: 15px 0;
                    padding: 15px;
                    background: #f8f9fa;
                    border-radius: 5px;
                }}
                .section h2 {{
                    color: #1a75ff;
                    font-size: 16px;
                    margin: 0 0 10px 0;
                    padding-bottom: 5px;
                    border-bottom: 1px solid #ddd;
                }}
                .grid-container {{
                    display: grid;
                    grid-template-columns: repeat(2, 1fr);
                    gap: 20px;
                }}
                .info-group {{
                    margin-bottom: 10px;
                }}
                .info-label {{
                    font-weight: bold;
                    color: #666;
                    font-size: 13px;
                }}
                .info-value {{
                    margin-top: 2px;
                    font-size: 14px;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin: 10px 0;
                }}
                th {{
                    background: #1a75ff;
                    color: white;
                    padding: 8px;
                    text-align: left;
                    font-size: 14px;
                }}
                td {{
                    padding: 8px;
                    border-bottom: 1px solid #ddd;
                    font-size: 14px;
                }}
                tr:nth-child(even) {{
                    background: #f8f9fa;
                }}
                .totali {{
                    margin-top: 20px;
                    text-align: right;
                }}
                .totali-row {{
                    display: flex;
                    justify-content: flex-end;
                    margin: 5px 0;
                }}
                .totali-label {{
                    font-weight: bold;
                    margin-right: 20px;
                    min-width: 150px;
                    text-align: right;
                }}
                .totali-value {{
                    min-width: 100px;
                    text-align: right;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>FATTURA ELETTRONICA</h1>
                    <div class="tipo-doc">
                        Numero: {invoice_data['header']['numero']} del {invoice_data['header']['data']}<br>
                        Tipo documento: {invoice_data['header']['tipo_documento']}
                    </div>
                </div>

                <div class="grid-container">
                    <div class="section">
                        <h2>CEDENTE/PRESTATORE</h2>
                        <div class="info-group">
                            <div class="info-label">Denominazione:</div>
                            <div class="info-value">{invoice_data['supplier']['denominazione']}</div>
                        </div>
                        <div class="info-group">
                            <div class="info-label">Partita IVA:</div>
                            <div class="info-value">{invoice_data['supplier']['partita_iva']}</div>
                        </div>
                        <div class="info-group">
                            <div class="info-label">Indirizzo:</div>
                            <div class="info-value">
                                {invoice_data['supplier']['indirizzo']}<br>
                                {invoice_data['supplier']['cap']} {invoice_data['supplier']['citta']} ({invoice_data['supplier']['provincia']})
                            </div>
                        </div>
                    </div>

                    <div class="section">
                        <h2>CESSIONARIO/COMMITTENTE</h2>
                        <div class="info-group">
                            <div class="info-label">Denominazione:</div>
                            <div class="info-value">{invoice_data['customer']['denominazione']}</div>
                        </div>
                        <div class="info-group">
                            <div class="info-label">Partita IVA:</div>
                            <div class="info-value">{invoice_data['customer']['partita_iva']}</div>
                        </div>
                        <div class="info-group">
                            <div class="info-label">Indirizzo:</div>
                            <div class="info-value">
                                {invoice_data['customer']['indirizzo']}<br>
                                {invoice_data['customer']['cap']} {invoice_data['customer']['citta']} ({invoice_data['customer']['provincia']})
                            </div>
                        </div>
                    </div>
                </div>

                <div class="section">
                    <h2>DATI BENI/SERVIZI</h2>
                    <table>
                        <thead>
                            <tr>
                                <th>Descrizione</th>
                                <th>Quantità</th>
                                <th>Prezzo Unitario</th>
                                <th>Importo</th>
                                <th>IVA %</th>
                            </tr>
                        </thead>
                        <tbody>
        """

        for item in invoice_data['items']:
            html += f"""
                            <tr>
                                <td>{item['descrizione']}</td>
                                <td>{item['quantita']}</td>
                                <td>€ {item['prezzo_unitario']:.2f}</td>
                                <td>€ {item['importo']:.2f}</td>
                                <td>{item['aliquota_iva']}%</td>
                            </tr>
            """

        html += f"""
                        </tbody>
                    </table>
                </div>

                <div class="section">
                    <h2>RIEPILOGO IVA E TOTALI</h2>
                    <div class="totali">
                        <div class="totali-row">
                            <div class="totali-label">Imponibile:</div>
                            <div class="totali-value">€ {invoice_data['totals']['imponibile']:.2f}</div>
                        </div>
                        <div class="totali-row">
                            <div class="totali-label">IVA:</div>
                            <div class="totali-value">€ {invoice_data['totals']['imposta']:.2f}</div>
                        </div>
                        <div class="totali-row">
                            <div class="totali-label">Totale Documento:</div>
                            <div class="totali-value">€ {invoice_data['totals']['imponibile'] + invoice_data['totals']['imposta']:.2f}</div>
                        </div>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        return html
    
    def _format_signature_info(self, signer_info):
        html = """
            <h3>Informazioni sulla Firma Digitale:</h3>
            <table>
                <tr>
                    <th>Firmatario</th>
                    <th>Data Firma</th>
                    <th>Certificato emesso da</th>
                </tr>
        """
        
        for signer in signer_info:
            data_firma = signer['data_firma'].strftime('%d/%m/%Y %H:%M:%S') if signer['data_firma'] else 'N/D'
            html += f"""
                <tr>
                    <td>{signer['nome']}</td>
                    <td>{data_firma}</td>
                    <td>{signer['certificato_da']}</td>
                </tr>
            """
            
        html += "</table>"
        return html
    
    def save_as_pdf(self):
        if not self.viewer.toPlainText():
            return
            
        file_name, _ = QFileDialog.getSaveFileName(
            self,
            "Salva come PDF",
            "",
            "File PDF (*.pdf)"
        )
        
        if file_name:
            # Ottieni l'HTML dal viewer
            html_content = self.viewer.toHtml()
            
            # Ottieni il percorso corretto di wkhtmltopdf
            if getattr(sys, 'frozen', False):
                # Se l'app è in bundle (installata)
                bundle_dir = sys._MEIPASS
                wkhtmltopdf_path = os.path.join(bundle_dir, 'bin', 'wkhtmltopdf')
            else:
                # Se l'app è in sviluppo
                wkhtmltopdf_path = 'bin/wkhtmltopdf'
            
            # Configura pdfkit per utilizzare wkhtmltopdf
            config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)
            
            # Genera il PDF
            try:
                pdfkit.from_string(html_content, file_name, configuration=config, options={'quiet': ''})
            except Exception as e:
                QMessageBox.critical(self, "Errore", f"Errore durante la creazione del PDF: {str(e)}")
    
    def print_invoice(self):
        if not self.viewer.toPlainText():
            return
            
        # Ottieni le informazioni sulla firma se presenti
        signature_html = None
        if hasattr(self, 'current_signature_info'):
            signature_html = self._format_signature_info(self.current_signature_info)
        
        # Usa l'istanza di PrintManager creata nell'init
        self.print_manager.print_document(self.current_invoice_data, signature_html)
    
    # Gestione Drag & Drop
    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
    
    def dropEvent(self, event: QDropEvent):
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        for file_path in files:
            if file_path.lower().endswith(('.xml', '.p7m')):
                self.load_xml(file_path)
                break 

    def open_invoice(self):
        """Apre un file XML o P7M e lo carica nel visualizzatore."""
        file_name, _ = QFileDialog.getOpenFileName(self, "Apri Fattura", "", "Fatture (*.xml *.p7m)")
        if file_name:
            self.load_invoice(file_name)

    def load_invoice(self, file_path):
        """Carica e visualizza la fattura dal file specificato."""
        with open(file_path, 'rb') as file:
            content = file.read()
            invoice_data = InvoiceParser().parse_invoice(content)
            self.viewer.setHtml(PDFLayout().generate_invoice_html(invoice_data)) 