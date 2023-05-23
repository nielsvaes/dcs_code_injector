from PySide6.QtWidgets import *
from PySide6.QtGui import *
from ez_settings import EZSettings
import os
from .ui.dcs_code_injector_settings_ui import Ui_settings_dialog


class SettingsDialog(QDialog, Ui_settings_dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.load()
        self.btn_browse.clicked.connect(self.open_file_browser)

    def open_file_browser(self):
        file_dialog = QFileDialog()
        file_dialog.setDirectory(os.path.join(os.environ.get('USERPROFILE'), 'Saved Games'))
        file_dialog.setNameFilter("Log files (*.log)")
        file_dialog.exec_()

        selected_files = file_dialog.selectedFiles()
        if selected_files:
            file_path = selected_files[0]
            self.txt_log_file.setText(file_path)

    def load(self):
        self.txt_log_file.setText(EZSettings().get("log_file", ""))
        self.spin_offset_time.setValue(EZSettings().get("shift_hours", 0))

    def save(self):
        EZSettings().set("log_file", self.txt_log_file.text())
        EZSettings().set("shift_hours", self.spin_offset_time.value())


    def closeEvent(self, arg__1: QCloseEvent) -> None:
        self.save()
        super().closeEvent(arg__1)