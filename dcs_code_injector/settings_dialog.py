from PySide6.QtWidgets import *
from PySide6.QtGui import *
from ez_settings import EZSettings
from functools import partial
import ez_icons
import os
from .ui.dcs_code_injector_settings_ui import Ui_settings_dialog
from . import utils
ICON = os.path.join(os.path.dirname(__file__), "ui", "icons", "icon.png")


DEFAULT_HIGHLIGHTING_RULES = {
        "^.*\\b(SCRIPTING)\\b.*$": [
            "(0, 0, 0, 0)",
            "(85, 255, 255, 255)"
        ],
        "^.*\\b(WARNING)\\b.*$": [
            "(0, 0, 0, 0)",
            "(255, 255, 0, 255)"
        ],
        "^.*\\b(ERROR|stack traceback|in function|in main chunk)\\b.*$": [
            "(255, 0, 0, 255)",
            "(255, 255, 255, 255)"
        ],
        "^.*(\\/E:).*$": [
            "(255, 0, 0, 255)",
            "(255, 255, 255, 255)"
        ],
        "^.*\\b(ERROR_ONCE)\\b.*$": [
            "(255, 139, 30, 255)",
            "(255, 255, 255, 255)"
        ],
        "^.*\\b(MOOSE INCLUDE END|MOOSE STATIC INCLUDE START)\\b.*$": [
            "(0, 0, 0, 0)",
            "(54, 194, 72, 255)"
        ]
}

class SettingsDialog(QDialog, Ui_settings_dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(ICON))

        self.tree_hilite_rules = LogHighlightingRulesTree()
        self.log_highlighting_rules_layout.insertWidget(0, self.tree_hilite_rules)

        self.btn_browse.clicked.connect(self.open_file_browser)
        self.btn_add_item.clicked.connect(partial(self.tree_hilite_rules.add_item, None))
        self.btn_save.clicked.connect(self.save)
        self.btn_cancel.clicked.connect(self.close)


        self.load()

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
        hl_rules = EZSettings().get("log_highlight_rules", {})
        if len(hl_rules):
            self.tree_hilite_rules.set_data(hl_rules)
        else:
            self.tree_hilite_rules.set_data(DEFAULT_HIGHLIGHTING_RULES)

    def save(self):
        EZSettings().set("log_file", self.txt_log_file.text())
        EZSettings().set("shift_hours", self.spin_offset_time.value())
        EZSettings().set("log_highlight_rules", self.tree_hilite_rules.get_data())
        self.close()


class LogHighlightingRulesTree(QTreeWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setColumnCount(3)
        self.setHeaderLabels(["String or regex", "Back color", "Text color"])
        self.itemDoubleClicked.connect(self.item_double_clicked)
        self.itemChanged.connect(self.item_changed)
        self.setRootIsDecorated(False)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setColumnWidth(0, 350)
        self.setColumnWidth(1, 130)
        self.setColumnWidth(2, 130)

        self.previous_text = {}

    def add_item(self, data=None):
        if data is None:
            item = QTreeWidgetItem(["STRING OR REGEX", "(0, 0, 0, 0)", "(255, 255, 255, 255)"])
            item.setIcon(0, QIcon(ez_icons.get(ez_icons.c.white, ez_icons.i.color_lens)))
        else:
            item = QTreeWidgetItem([data[0], data[1], data[2]])

        item.setFlags(item.flags() | Qt.ItemIsEditable)
        item.setCheckState(0, Qt.Unchecked)
        item.setIcon(0, QIcon(ez_icons.get(ez_icons.c.white, ez_icons.i.color_lens)))
        self.addTopLevelItem(item)

        self.previous_text[item] = item.text(0)

    def set_data(self, data):
        for name, color_list in data.items():
            self.add_item([name, color_list[0], color_list[1]])

    def get_data(self):
        data = {}
        for i in range(self.topLevelItemCount()):
            item = self.topLevelItem(i)
            name = item.text(0)
            background_color = item.text(1)
            foreground_color=  item.text(2)
            data[name] = [background_color, foreground_color]
        return data

    def item_changed(self, item: QTreeWidgetItem, column):
        if column == 0 and self.previous_text.get(item) != item.text(0):
            self.blockSignals(True)

            if item.checkState() == Qt.Checked:
                is_regex = utils.check_regex(item.text(0))
                if is_regex:
                    item.setIcon(0, QIcon(ez_icons.get(ez_icons.c.white, ez_icons.i.developer_mode)))
                else:
                    item.setIcon(0, QIcon(ez_icons.get(ez_icons.c.white, ez_icons.i.text_format)))

            self.previous_text[item] = item.text(0)
            self.blockSignals(False)

    def item_double_clicked(self, item: QTreeWidgetItem, column):
        if column == 1 or column == 2:
            rgb = eval(item.text(column))
            initial_color = QColor(*rgb)
            color = QColorDialog.getColor(initial=initial_color, options=QColorDialog.ShowAlphaChannel)
            if color.isValid():
                item.setText(column, str(color.getRgb()))

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete:
            selected_items = self.selectedItems()
            for item in selected_items:
                index = self.indexOfTopLevelItem(item)
                self.takeTopLevelItem(index)
