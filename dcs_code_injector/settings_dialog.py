from PySide6.QtWidgets import *
from PySide6.QtGui import *

from ez_settings import EZSettings
from functools import partial
import os

from .ui.dcs_code_injector_settings_ui import Ui_settings_dialog
from .constants import DEFAULT_HIGHLIGHTING_RULES, sk
from . import lua_function_parser


class SettingsDialog(QDialog, Ui_settings_dialog):
    def __init__(self):
        """
        Constructor for the SettingsDialog class.
        """

        super().__init__()
        self.setupUi(self)

        self.tree_hilite_rules = LogHighlightingRulesTree()
        self.log_highlighting_rules_layout.insertWidget(0, self.tree_hilite_rules)

        self.btn_browse.clicked.connect(self.open_file_browser)
        self.btn_add_item.clicked.connect(partial(self.tree_hilite_rules.add_item, None))
        self.btn_save.clicked.connect(self.save)
        self.btn_cancel.clicked.connect(self.close)

        self.btn_update_MOOSE_data.clicked.connect(partial(self.download_code, self.txt_moose_url, sk.MOOSE_autocomplete))
        self.btn_update_mist_data.clicked.connect(partial(self.download_code, self.txt_mist_url, sk.mist_autocomplete))

        self.btn_clear_MOOSE.clicked.connect(partial(self.clear_code, sk.MOOSE_autocomplete))
        self.btn_clear_mist.clicked.connect(partial(self.clear_code, sk.mist_autocomplete))


        self.load()

    @staticmethod
    def download_code(sending_line_edit, settings_key):
        # msg_box = QMessageBox()

        url = sending_line_edit.text()
        lines = lua_function_parser.update_from_url(url)
        if len(lines):
            EZSettings().set(settings_key, lines)

            QMessageBox().information(None, "Info", "Code completion updated, restart the program to see code completion updates")
        else:
            QMessageBox().warning(None,f"Warning", f"Couldn't download the file at {url}, are you sure it's correct?")

    @staticmethod
    def clear_code(settings_key):
        EZSettings().remove(settings_key)
        QMessageBox().information(None, "Info","Code completion updated, restart the program to see code completion updates")

    def open_file_browser(self):
        """
        Opens a file dialog to select a log file.
        """

        file_dialog = QFileDialog()
        file_dialog.setDirectory(os.path.join(os.environ.get('USERPROFILE'), 'Saved Games'))
        file_dialog.setNameFilter("Log files (*.log)")
        file_dialog.exec_()

        selected_files = file_dialog.selectedFiles()
        if selected_files:
            file_path = selected_files[0]
            self.txt_log_file.setText(file_path)

    def load(self):
        """
        Loads the settings from the EZSettings instance and updates the UI accordingly.
        """

        self.txt_log_file.setText(EZSettings().get(sk.log_file, ""))
        self.chk_play_sound_on_mission_scripting_errors.setChecked(EZSettings().get(sk.play_sound_on_mission_scripting_error, True))
        self.spin_offset_time.setValue(EZSettings().get(sk.shift_hours, 0))
        hl_rules = EZSettings().get(sk.log_highlight_rules, {})
        if len(hl_rules):
            self.tree_hilite_rules.set_data(hl_rules)
        else:
            self.tree_hilite_rules.set_data(DEFAULT_HIGHLIGHTING_RULES)

        self.chk_enable_code_completion.setChecked(EZSettings().get(sk.enable_code_completion, True))
        self.txt_moose_url.setText(EZSettings().get(sk.MOOSE_url, sk.default_MOOSE_url))
        self.txt_mist_url.setText(EZSettings().get(sk.mist_url, sk.default_mist_url))


    def save(self):
        """
        Saves the current settings to the EZSettings instance.
        """

        EZSettings().set(sk.log_file, self.txt_log_file.text())
        EZSettings().set(sk.play_sound_on_mission_scripting_error, self.chk_play_sound_on_mission_scripting_errors.isChecked())
        EZSettings().set(sk.enable_code_completion, self.chk_enable_code_completion.isChecked())
        EZSettings().set(sk.shift_hours, self.spin_offset_time.value())
        EZSettings().set(sk.log_highlight_rules, self.tree_hilite_rules.get_data())

        EZSettings().set(sk.MOOSE_url, self.txt_moose_url.text())
        EZSettings().set(sk.mist_url, self.txt_mist_url.text())

        self.close()


class LogHighlightingRulesTree(QTreeWidget):
    def __init__(self, parent=None):
        """
        Constructor for the LogHighlightingRulesTree class.

        :param parent: <QWidget> the parent widget
        """

        super().__init__(parent)
        self.setHeaderLabels(["String or regex", "Back color", "Text color"])

        self.itemDoubleClicked.connect(self.item_double_clicked)

        self.setRootIsDecorated(False)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        self.setColumnWidth(0, 500)
        self.setColumnWidth(1, 130)
        self.setColumnWidth(2, 130)

    def add_item(self, data=None):
        """
        Adds a new item to the tree.

        :param data: <list> the data for the new item
        """

        if data is None:
            item = QTreeWidgetItem(["String or regex", "(0, 0, 0, 0)", "(255, 255, 255, 255)"])
        else:
            item = QTreeWidgetItem([data[0], data[1], data[2]])

        font = QFont("Courier New")
        item.setFont(0, font)
        item.setFlags(item.flags() | Qt.ItemIsEditable)
        self.addTopLevelItem(item)

    def set_data(self, data):
        """
        Sets the data for the tree.

        :param data: <dict> the data to set
        """

        for name, color_list in data.items():
            self.add_item([name, color_list[0], color_list[1]])

    def get_data(self):
        """
        Gets the data from the tree.

        :return: <dict> the tree's data
        """

        data = {}
        for i in range(self.topLevelItemCount()):
            item = self.topLevelItem(i)
            name = item.text(0)
            background_color = item.text(1)
            foreground_color=  item.text(2)
            data[name] = [background_color, foreground_color]
        return data

    @staticmethod
    def item_double_clicked(item: QTreeWidgetItem, column):
        """
        Handles the itemDoubleClicked signal.

        :param item: <QTreeWidgetItem> the item that was double clicked
        :param column: <int> the column that was double clicked
        """

        if column == 1 or column == 2:
            rgb = eval(item.text(column))
            initial_color = QColor(*rgb)
            color = QColorDialog.getColor(initial=initial_color, options=QColorDialog.ShowAlphaChannel)
            if color.isValid():
                item.setText(column, str(color.getRgb()))

    def keyPressEvent(self, event):
        """
        Handles key press events.

        :param event: <QKeyEvent> the key press event
        """

        if event.key() == Qt.Key_Delete:
            selected_items = self.selectedItems()
            for item in selected_items:
                index = self.indexOfTopLevelItem(item)
                self.takeTopLevelItem(index)
