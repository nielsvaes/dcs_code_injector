from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtCore import Qt

from .ui.dcs_code_injector_search_ui import Ui_Form

class LogView(QPlainTextEdit):
    def __init__(self):
        """
        Constructor for the LogView class.
        """

        super().__init__()
        self.search_widget = SearchBox()
        self.search_widget.txt_search.returnPressed.connect(self.search_text)

        self.last_search_position = 0

        self.grid_layout = QGridLayout(self)
        self.grid_layout.setContentsMargins(0, 10 , 15, 0)
        self.grid_layout.addWidget(self.search_widget, 0, 0, 0, 0, Qt.AlignTop | Qt.AlignRight)
        self.setReadOnly(True)


    def toggle_search(self):
        """
        Toggles the visibility of the search widget.
        """

        self.search_widget.setVisible(not self.search_widget.isVisible())
        self.search_widget.txt_search.clear()
        self.search_widget.txt_search.setFocus()

    def search_text(self):
        """
        Searches the text in the log view based on the query in the search widget. Highlights the text when found
        """

        search_query = self.search_widget.txt_search.text()

        if self.search_widget.btn_case_sensitive.isChecked():
            cursor = self.document().find(search_query, self.last_search_position, QTextDocument.FindFlag.FindCaseSensitively)
        else:
            cursor = self.document().find(search_query, self.last_search_position)

        if not cursor.isNull():
            self.last_search_position = cursor.position()
            self.setTextCursor(cursor)
        else:
            self.last_search_position = 0


class SearchBox(QWidget, Ui_Form):
    def __init__(self):
        """
        Constructor for the SearchBox class.
        """

        super().__init__()
        self.setupUi(self)
        self.setVisible(False)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        """
        Handles key press events.

        :param event: <QKeyEvent> the key press event
        """

        if event.key() == Qt.Key_Escape:
            self.setVisible(False)