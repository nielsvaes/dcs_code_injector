from . import VERSION, LOGO

from PySide6.QtWidgets import *
from PySide6.QtGui import *

class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("About DCS Code Injector")

        layout = QVBoxLayout()

        title =  f"DCS Code Injector\n\n"
        lbl_title = QLabel(title)
        lbl_title.setStyleSheet("font-size: 14pt")

        lbl_image = QLabel()
        lbl_image.setPixmap(QPixmap(LOGO))

        msg = f"Version {VERSION}"
        msg += f"\n©️ Niels Vaes"

        lbl_version = QLabel(msg)
        layout.addWidget(lbl_title)
        layout.addWidget(lbl_image)
        layout.addWidget(lbl_version)

        close_button = QPushButton("Close")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)

        self.setLayout(layout)