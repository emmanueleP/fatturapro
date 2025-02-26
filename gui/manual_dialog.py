from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QDialogButtonBox

class ManualDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Manuale")
        self.setMinimumSize(400, 300)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        manual_text = """
        Benvenuto in FatturaPro!

        Questa applicazione ti permette di visualizzare, convertire in PDF e stampare fatture elettroniche in formato XML e P7M.

        Funzionalità principali:
        - Apri fatture elettroniche in formato XML o P7M.
        - Salva le fatture come PDF.
        - Stampa le fatture direttamente dall'app.
        - Visualizza informazioni sulla firma digitale per file P7M.

        Per utilizzare l'app:
        1. Clicca su "Apri Fattura" per selezionare un file XML o P7M.
        2. Visualizza i dettagli della fattura.
        3. Usa "Salva PDF" per esportare la fattura in formato PDF.
        4. Clicca su "Stampa" per stampare la fattura.

        Se hai bisogno di ulteriore assistenza, consulta il manuale o contatta il supporto.
        """

        label = QLabel(manual_text)
        layout.addWidget(label)

        button_box = QDialogButtonBox()
        close_button = QPushButton("Chiudi")
        close_button.clicked.connect(self.accept)
        button_box.addButton(close_button, QDialogButtonBox.ButtonRole.AcceptRole)

        layout.addWidget(button_box) 