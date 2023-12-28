from . import VERSION
from PySide6.QtWidgets import *

class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("About DCS Code Injector")
        # self.setWindowIcon(QIcon(ICON))

        layout = QVBoxLayout()

        title =  f"DCS Code Injector\n\n"
        lbl_title = QLabel(title)
        lbl_title.setStyleSheet("font-size: 14pt")

        msg = f"Version {VERSION}"
        msg += f"\n(c) Niels Vaes"

        lbl_version = QLabel(msg)
        layout.addWidget(lbl_title)
        layout.addWidget(lbl_version)

        close_button = QPushButton("Close")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)

        self.setLayout(layout)