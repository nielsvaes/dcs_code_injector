from PySide6.QtCore import QAbstractItemModel, QModelIndex, Qt, QTimer
from PySide6.QtWidgets import QApplication, QTreeView, QVBoxLayout, QWidget
import sys
import json

class Node:
    def __init__(self, data, parent=None):
        self._data = data
        self._children = []
        self._parent = parent
        if parent is not None:
            parent.add_child(self)

    def add_child(self, child):
        self._children.append(child)

    def child(self, row):
        return self._children[row]

    def child_count(self):
        return len(self._children)

    def column_count(self):
        return 2

    def data(self, column):
        if column == 0:
            return self._data[0]
        if column == 1:
            return self._data[1]
        return None

    def parent(self):
        return self._parent

    def row(self):
        if self._parent is not None:
            return self._parent._children.index(self)
        return 0

class VariablesModel(QAbstractItemModel):
    def __init__(self, root, parent=None):
        super().__init__(parent)
        self._rootNode = root

    def update_root(self, root):
        self.beginResetModel()
        self._rootNode = root
        self.endResetModel()

    def rowCount(self, parent=QModelIndex()):
        if parent.column() > 0:
            return 0
        if not parent.isValid():
            parentNode = self._rootNode
        else:
            parentNode = parent.internalPointer()
        return parentNode.child_count()

    def columnCount(self, parent=QModelIndex()):
        return 2

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None
        node = index.internalPointer()
        if role == Qt.DisplayRole:
            return node.data(index.column())
        return None

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            if section == 0:
                return "Variable"
            if section == 1:
                return "Value"
        return None

    def index(self, row, column, parent):
        if not self.hasIndex(row, column, parent):
            return QModelIndex()
        parentNode = parent.internalPointer() if parent.isValid() else self._rootNode
        childItem = parentNode.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        return QModelIndex()

    def parent(self, index):
        if not index.isValid():
            return QModelIndex()
        childNode = index.internalPointer()
        parentNode = childNode.parent()
        if parentNode == self._rootNode:
            return QModelIndex()
        return self.createIndex(parentNode.row(), 0, parentNode)


class VariablesTreeView(QTreeView):
    def __init__(self, parent=None):
        super().__init__(parent)
        # self.setAlternatingRowColors(True)
        self.setStyleSheet("QTreeView::item { padding-top: -3px; padding-bottom: -3px; }")

    def update_json(self, json_str):
        json_obj = json.loads(json_str)
        root_node = parse_json(json_obj)
        if self.model() is None:
            model = VariablesModel(root_node)
            self.setModel(model)
        else:
            self.model().update_root(root_node)
        self.expandAll()
        self.setRootIsDecorated(False)

    def start_updates(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_random_json)
        self.timer.start(100)  # update every 0.1 seconds

    def update_random_json(self):
        import random
        json_str = json.dumps({
            "random_number": random.randint(1, 100),
            "more_data": {
                "nested_number": random.randint(1, 100),
                "nested_list": [random.randint(1, 100) for _ in range(3)]
            }
        })
        self.update_json(json_str)

    def drawBranches(self, painter, rect, index) -> None:
        pass


def parse_json(data, parent=None):
    if parent is None:
        parent = Node(("root", "root"))
    if type(data) is dict:
        for key, value in data.items():
            if type(value) is dict or type(value) is list:
                new_parent = Node((key, ""), parent)
                parse_json(value, new_parent)
            else:
                Node((key, value), parent)
    elif type(data) is list:
        Node((parent.data(0), ', '.join(map(str, data))), parent)
    else:
        Node((parent.data(0), data), parent)
    return parent



# app = QApplication(sys.argv)
# widget = JsonTreeView()
# widget.show()
# widget.start_updates()
#
json_str = """
{
    "name": "John",
    "age": 30,
    "cars": {
        "car1" : "Ford",
        "car2" : "BMW",
        "car3" : "Fiat",
        "bugatti": {
            "driver": "Mikey",
            "tires" : 4

        }
     },
    "pets": ["Dog", "Cat"]
}
"""
# # widget.update_json(json_str)
# sys.exit(app.exec())
