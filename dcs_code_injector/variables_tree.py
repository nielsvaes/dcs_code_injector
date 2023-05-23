from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
import json
from ez_utils import io_utils
from ez_qt import tree_widget

VARIABLES_FILE = "C:/temp/watch_variables.json"

class VariablesTree(QTreeWidget):
    def __init__(self):
        super(VariablesTree, self).__init__()
        self.setHeaderLabels(["Var", "Value"])
        self.__previous_values = {}

        # self.timer = QTimer()
        # self.timer.setInterval(250)
        # self.timer.timeout.connect(self.update_view)
        # self.timer.start()

    def update_view(self):
        info_dict = io_utils.read_json(VARIABLES_FILE)
        to_remove = []

        for var_name, var_value in self.__previous_values.items():
            if not var_name in info_dict:
                to_remove.append(self.get_item_with_text(var_name, 0))

            new_value = info_dict.get(var_name)
            item = self.get_item_with_text(var_name, 0)
            if item is None:
                item = QTreeWidgetItem()
                item.setText(0, var_name)
                item.setText(1, str(new_value))
                self.addTopLevelItem(item)

            if var_value != new_value:
                item.setText(1, str(new_value))

        self.remove_items(to_remove)
        self.__previous_values = info_dict
        self.resize_columns()

    def get_item_with_text(self, text, column_index):
        """
        Returns a QTreeWidgetItem that matches the selected text for the selected column

        :param tree_widget: QTreeWidget you want to search in
        :param text: <string> text
        :param column_index: <int> column number
        :return: QTreeWidgetItem if found or None if not found
        """
        try:
            iterator = QTreeWidgetItemIterator(self)
            while iterator:
                if iterator.value().text(column_index) == text:
                    return iterator.value()
                iterator += 1
        except:
            return None

        return None

    def remove_items(self, items=[], selected=False):
        """
        Removes the passed items from the tree widget

        :param tree_widget: QTreeWidget to remove items from
        :param items: <list> items you want to remove
        :param selected: <bool> if set to True, will remove the selected items
        :return:
        """
        if selected:
            items = self.selectedItems()

        root = self.invisibleRootItem()
        for item in items:
            (item.parent() or root).removeChild(item)

    def resize_columns(self, columns="all"):
        """
        Sets the column size to the minimal amount needed

        :param tree_widget: QTreeWidget you want to restructure
        :param columns: <string> | <list> either the string "all" or a list with specific column numbers
        :return:
        """
        if columns == "all":
            for column in range(self.columnCount()):
                self.resizeColumnToContents(column)
        else:
            for column in columns:
                self.resizeColumnToContents(column)