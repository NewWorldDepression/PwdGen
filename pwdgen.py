# password_generator.py
from PyQt6 import QtWidgets, QtGui, QtCore
import sys
import secrets
import string

class PasswordGenerator(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Générateur de mot de passe")
        self.setWindowIcon(QtGui.QIcon())  # tu peux mettre un chemin vers une icône si tu veux
        self.setFixedSize(420, 220)
        self.init_ui()

    def init_ui(self):
        layout = QtWidgets.QVBoxLayout()
        form = QtWidgets.QFormLayout()

        # Longueur
        self.length_spin = QtWidgets.QSpinBox()
        self.length_spin.setRange(4, 128)
        self.length_spin.setValue(16)
        form.addRow("Longueur :", self.length_spin)

        # Checkboxes
        cb_layout = QtWidgets.QHBoxLayout()
        self.cb_lower = QtWidgets.QCheckBox("Minuscules (a-z)")
        self.cb_lower.setChecked(True)
        self.cb_upper = QtWidgets.QCheckBox("Majuscules (A-Z)")
        self.cb_upper.setChecked(True)
        self.cb_digits = QtWidgets.QCheckBox("Chiffres (0-9)")
        self.cb_digits.setChecked(True)
        cb_layout.addWidget(self.cb_lower)
        cb_layout.addWidget(self.cb_upper)
        cb_layout.addWidget(self.cb_digits)
        form.addRow("Inclure :", cb_layout)

        # Symboles
        self.cb_symbols = QtWidgets.QCheckBox("Symboles (!@#...)")
        self.cb_symbols.setChecked(True)
        form.addRow("", self.cb_symbols)

        layout.addLayout(form)

        # Boutons
        buttons_layout = QtWidgets.QHBoxLayout()
        self.generate_btn = QtWidgets.QPushButton("Générer")
        self.generate_btn.clicked.connect(self.generate_password)
        self.copy_btn = QtWidgets.QPushButton("Copier")
        self.copy_btn.clicked.connect(self.copy_to_clipboard)
        self.copy_btn.setEnabled(False)
        buttons_layout.addWidget(self.generate_btn)
        buttons_layout.addWidget(self.copy_btn)
        layout.addLayout(buttons_layout)

        # Champ résultat
        self.result = QtWidgets.QLineEdit()
        self.result.setReadOnly(True)
        font = self.result.font()
        font.setPointSize(10)
        self.result.setFont(font)
        layout.addWidget(self.result)

        # Info / statut
        self.status = QtWidgets.QLabel("")
        layout.addWidget(self.status)

        self.setLayout(layout)

    def generate_password(self):
        length = int(self.length_spin.value())
        parts = []

        if self.cb_lower.isChecked():
            parts.append(string.ascii_lowercase)
        if self.cb_upper.isChecked():
            parts.append(string.ascii_uppercase)
        if self.cb_digits.isChecked():
            parts.append(string.digits)
        if self.cb_symbols.isChecked():
            # Exclut les espaces et caractères ambigus ; tu peux modifier la liste si tu veux
            parts.append("!#$%&()*+,-./:;<=>?@[]^_{|}~")

        if not parts:
            self.status.setText("Sélectionne au moins une catégorie de caractères.")
            self.result.clear()
            self.copy_btn.setEnabled(False)
            return

        # Construire l'alphabet possible
        alphabet = "".join(parts)

        # Pour s'assurer qu'au moins une catégorie soit présente dans le mot de passe,
        # on tire un caractère par catégorie, puis on complète le reste.
        password_chars = []
        for group in parts:
            password_chars.append(secrets.choice(group))

        # Remplir le reste
        remaining = length - len(password_chars)
        for _ in range(remaining):
            password_chars.append(secrets.choice(alphabet))

        # Mélanger de façon sécurisée
        secrets.SystemRandom().shuffle(password_chars)
        password = "".join(password_chars)

        self.result.setText(password)
        self.status.setText(f"Mot de passe généré — longueur {length}")
        self.copy_btn.setEnabled(True)

    def copy_to_clipboard(self):
        clipboard = QtWidgets.QApplication.clipboard()
        clipboard.setText(self.result.text())
        self.status.setText("Mot de passe copié dans le presse-papier.")

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = PasswordGenerator()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
