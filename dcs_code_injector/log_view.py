from datetime import datetime, timedelta

from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtCore import Qt

import os

from pygtail import Pygtail

from .log_highlighter import LogHighlighter
from .ui.dcs_code_injector_search_ui import Ui_Form
from .constants import sk

from ez_settings import EZSettings

class LogView(QPlainTextEdit):
    showSettings = Signal()
    playErrorSound = Signal()
    def __init__(self):
        """
        Constructor for the LogView class.
        """
        self.init_done = False

        super().__init__()
        self.font = EZSettings().get(sk.log_font, sk.default_font)
        self.font_size = EZSettings().get(sk.log_font_size, 10)
        self.__update_font()

        # make search widget
        self.search_widget = SearchBox()
        self.search_widget.txt_search.returnPressed.connect(self.search_text)
        self.grid_layout = QGridLayout(self)
        self.grid_layout.setContentsMargins(0, 10 , 15, 0)
        self.grid_layout.addWidget(self.search_widget, 0, 0, 0, 0, Qt.AlignTop | Qt.AlignRight)


        self.last_search_position = 0

        self.log_file = EZSettings().get(sk.log_file, "")
        if not os.path.isfile(self.log_file):
            self.showSettings.emit()
            self.log_file = EZSettings().get(sk.log_file, "")

        self.timer = QTimer()
        self.timer.setInterval(500)
        self.timer.timeout.connect(self.read_log)
        if EZSettings().get(sk.update_log_view, True):
            self.timer.start()

        LogHighlighter(self.document())

        self.setReadOnly(True)
        self.init_done = True

    def set_font(self, font):
        self.font = font
        EZSettings().set(sk.log_font, font)
        self.__update_font()

    def set_font_size(self, font_size):
        self.font_size = font_size
        EZSettings().set(sk.log_font_size, font_size)
        self.__update_font()

    def enable_updating(self, value):
        EZSettings().set(sk.update_log_view, value)
        if value:
            self.timer.start()
        else:
            self.timer.stop()

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

    def add_text(self, complete_text):
        self.moveCursor(QTextCursor.End)
        self.insertPlainText(complete_text)
        self.verticalScrollBar().setValue(self.verticalScrollBar().maximum())

    def clear(self):
        self.add_text("\n" * 60)

    def read_log(self):
        if not os.path.isfile(self.log_file):
            self.showSettings.emit()
            self.log_file = EZSettings().get(sk.log_file, "")

        if not self.init_done:
            with open(self.log_file, "r") as readfile:
                self.add_text(readfile.read())

        for line in Pygtail(self.log_file):
            try:
                line = line.replace("                    ", "   ")
                time_str = line[0:22]
                time = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S.%f")
                shift_hours = EZSettings().get(sk.shift_hours, 0)
                time += timedelta(hours=shift_hours)
                shifted_time_str = time.strftime("%Y-%m-%d %H:%M:%S.%f")[:-4]
                line = line.replace(time_str, shifted_time_str)

                diff = datetime.now() - time
                if ("mission script error" in line.lower() and
                        diff.total_seconds() > 0.7 and
                        self.init_done and
                        EZSettings().get(sk.play_sound_on_mission_scripting_error, True)):
                    self.playErrorSound.emit()

                self.add_text(line)
            except ValueError as err:
                self.add_text(line)

    def __update_font(self):
        self.setStyleSheet(f"font: {self.font_size}pt '{self.font}';")


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