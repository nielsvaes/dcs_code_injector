from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
import os
import json
from functools import partial
from ez_settings import EZSettings
from datetime import datetime, timedelta
# import ez_icons
# from ez_icons import i, c

from .settings_dialog import SettingsDialog

from .server import Server
from .lua_syntax_highlighter import SimpleLuaHighlighter
from .log_highlighter import LogHighlighter
# from .variables_tree import VariablesTree
from .ui.dcs_code_injector_window_ui import Ui_MainWindow
ICON = os.path.join(os.path.dirname(__file__), "ui", "icons", "icon.png")

CODE_INSERTS = {
    "base": ["BASE:I()", -1],
    "msg_to_all": ["MessageToAll()", -1]
}

class CodeInjectorWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(ICON))
        self.resize(1280, 800)
        self.setWindowTitle("DCS Code Injector")

        self.favorites_widget = FavoritesWidget()
        self.favorites_layout.addWidget(self.favorites_widget)

        # self.variables_tree = VariablesTree()
        # self.variables_layout.addWidget(self.variables_tree)

        self.last_log_file_size = 0

        self.log_file = EZSettings().get("log_file", "")
        self.previous = []
        LogHighlighter(self.txt_log.document())
        self.read_log()

        self.load()

        self.log_font_size = 10
        self.update_log_font_size()

        self.server = Server()
        self.server_thread = QThread()
        self.server.moveToThread(self.server_thread)

        self.timer = QTimer()
        self.timer.setInterval(500)
        self.timer.timeout.connect(self.read_log)
        self.timer.start()

        self.connect_signals()

        QCoreApplication.instance().aboutToQuit.connect(self.stop_server)

        self.connection_label = QLabel()
        self.statusbar.addWidget(self.connection_label)
        self.on_disconnected()

        self.show()

    def read_log(self):
        if not os.path.isfile(self.log_file):
            self.show_settings()
            self.log_file = EZSettings().get("log_file", "")

        file_size = os.path.getsize(self.log_file)
        if file_size > self.last_log_file_size:
            with open(self.log_file, "r", encoding="utf-8") as read_file:
                original_lines = read_file.readlines()
            lines = []

            for line in original_lines:
                try:
                    line = line.replace("                    ", "   ")
                    time_str = line[0:22]
                    time = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S.%f")
                    shift_hours = EZSettings().get("shift_hours", 0)
                    time += timedelta(hours=shift_hours)
                    shifted_time_str = time.strftime("%Y-%m-%d %H:%M:%S.%f")[:-4]
                    line = line.replace(time_str, shifted_time_str)
                    lines.append(line)
                except:
                    pass

            diff = len(lines) - len(self.previous)
            if diff > 0:
                if diff == len(lines):
                    new_text = "".join(lines)
                else:
                    new_lines = lines[-diff:]
                    new_text = "".join(new_lines)
                self.add_text_to_log(new_text)
            self.previous = lines
        self.last_log_file_size = file_size

    def connect_signals(self):
        self.tab_widget.tabBarDoubleClicked.connect(self.rename_tab)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        self.action_settings.triggered.connect(self.show_settings)
        self.action_clear_log.triggered.connect(self.clear_log)
        self.favorites_widget.new_button_added.connect(self.connect_favorite_button)

        self.server_thread.started.connect(self.server.start)
        self.server.connected.connect(self.on_connected)
        self.server.received.connect(self.on_received)
        self.server.disconnected.connect(self.on_disconnected)
        self.server_thread.start()

    def on_received(self, data):
        try:
            data = json.loads(data.strip())
            if data.get("connection", "") == "not_active":
                print("connection closed!")

        except json.decoder.JSONDecodeError as err:
            print(err)

    def on_connected(self):
        pixmap = QPixmap(os.path.join(os.path.dirname(__file__), "ui", "icons", "cloud_done.png"))
        pixmap = pixmap.scaledToWidth(20, Qt.SmoothTransformation)
        self.connection_label.setPixmap(pixmap)
        self.statusbar.showMessage("Connected to DCS", 2500)

    def on_disconnected(self):
        pixmap = QPixmap(os.path.join(os.path.dirname(__file__), "ui", "icons", "cloud_off.png"))
        pixmap = pixmap.scaledToWidth(20, Qt.SmoothTransformation)
        self.connection_label.setPixmap(pixmap)
        self.statusbar.showMessage("Disconnected from DCS", 2500)

    def stop_server(self):
        print("killing server")
        self.server.exit = True
        self.server_thread.quit()
        self.server_thread.wait()

    def clear_log(self):
        self.add_text_to_log("\n" * 60)

    def update_log_font_size(self):
        self.txt_log.setStyleSheet(f"font: {self.log_font_size}pt 'Courier New';")

    def connect_favorite_button(self, favorite_button):
        favorite_button.clicked.connect(partial(self.set_server_response, favorite_button.code))
        favorite_button.open_tab_with_code.connect(partial(self.add_new_tab))

    def close_tab(self, tab_index):
        answer = QMessageBox.question(self, 'Close', "Are you sure you want to remove this tab?", QMessageBox.Yes, QMessageBox.No)
        if answer == QMessageBox.Yes:
            setting_name = self.tab_widget.tabText(tab_index)
            if tab_index > 0:
                new_index = tab_index - 1
            else:
                new_index = 0

            self.tab_widget.setCurrentIndex(new_index)
            self.tab_widget.removeTab(tab_index)
            EZSettings().remove(setting_name)

    def add_new_tab(self, name=None, code=None):
        code_text_edit = CodeTextEdit()
        code_text_edit.textChanged.connect(self.save_code)
        self.tab_widget.insertTab(self.tab_widget.count() - 1, code_text_edit, "UNNAMED")

        self.tab_widget.setCurrentIndex(self.tab_widget.count() - 2)
        if name is not None:
            self.tab_widget.setTabText(self.tab_widget.currentIndex(), name)
        if code is not None:
            self.tab_widget.currentWidget().setPlainText(code)
        else:
            self.tab_widget.currentWidget().setPlainText("log.write(\"DCS Code Injector\", log.INFO, \"Hello, DCS!\")\n")

    def rename_tab(self):
        name, accepted = QInputDialog().getText(self, "DCS Code Injector", "Enter a name for this tab: ", QLineEdit.Normal, "")
        if not accepted:
            return

        for index in range(self.tab_widget.count()):
            tab_name = self.tab_widget.tabText(index)
            if tab_name == name:
                name = name + "_01"

        self.tab_widget.setTabText(self.tab_widget.currentIndex(), name)
        self.save_code()

    def load(self):
        for setting in EZSettings().get_all_settings():
            if setting != "log_file" and setting != "shift_hours" and not setting.startswith("btn_"):
                self.add_new_tab(name=setting, code=EZSettings().get(setting))
            if setting.startswith("btn_"):
                self.favorites_widget.add_new_button(setting.replace("btn_", ""), EZSettings().get(setting))

    def save_code(self):
        tab_name = self.tab_widget.tabText(self.tab_widget.currentIndex())
        code = self.tab_widget.currentWidget().toPlainText()
        if code != "" and not tab_name == "UNNAMED":
            EZSettings().set(tab_name, code)

    def show_settings(self):
        dlg = SettingsDialog()
        dlg.exec_()
        self.setWindowTitle(f"DCS Code Injector - {dlg.txt_log_file.text()}")

    def add_code_to_log(self, text):
        line_number = 1
        numbered_lines = []
        numbered_lines.append("\n------------------- CODE BLOCK -------------------")
        for line in text.split("\n"):
            line = f"{str(line_number).zfill(2)}          {line}"
            numbered_lines.append(line)
            line_number += 1
        numbered_lines.append("\n------------------ /CODE BLOCK -------------------\n")
        complete_text = "\n".join(numbered_lines)
        self.add_text_to_log(complete_text)

    def add_text_to_log(self, complete_text):
        self.txt_log.moveCursor(QTextCursor.End)
        self.txt_log.insertPlainText(complete_text)
        self.txt_log.verticalScrollBar().setValue(self.txt_log.verticalScrollBar().maximum())

    def set_server_response(self, code):
        self.add_code_to_log(code)
        self.server.response = code

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return and event.modifiers() == Qt.ControlModifier:
            text = self.tab_widget.currentWidget().textCursor().selection().toPlainText()
            self.set_server_response(text)

        if event.key() == Qt.Key_F5:
            self.read_log()

        if event.key() == Qt.Key_N and event.modifiers() == Qt.ControlModifier:
            self.add_new_tab(name="UNNAMED", code="-- add code here")

        if event.key() == Qt.Key_Up and event.modifiers() == Qt.ControlModifier:
            self.tab_widget.currentWidget().font_size += 1
            self.tab_widget.currentWidget().update_document_size()
            self.log_font_size = self.tab_widget.currentWidget().font_size
            self.update_log_font_size()
        if event.key() == Qt.Key_Down and event.modifiers() == Qt.ControlModifier:
            self.tab_widget.currentWidget().font_size -= 1
            self.tab_widget.currentWidget().update_document_size()
            self.log_font_size = self.tab_widget.currentWidget().font_size
            self.update_log_font_size()


class CodeTextEdit(QPlainTextEdit):
    def __init__(self):
        super().__init__()

        self.font_size = 10
        self.update_document_size()
        SimpleLuaHighlighter(self.document())

    def update_document_size(self):
        self.setStyleSheet(f"font: {self.font_size}pt 'Courier New';")

    def get_selected_text(self):
        return self.textCursor().selectedText()

    def __insert_code(self, text, move_back_pos):
        cursor = self.textCursor()
        selected_text = cursor.selection().toPlainText()
        self.insertPlainText(text)
        pos = cursor.position() + move_back_pos
        cursor.setPosition(pos)
        self.setTextCursor(cursor)
        self.insertPlainText(selected_text)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key_Slash and event.modifiers() == Qt.ControlModifier:
            cursor = self.textCursor()
            selected_text = cursor.selection().toPlainText()
            lines = selected_text.split("\n")
            commented_lines = []
            for line in lines:
                if line.startswith("-- "):
                    line = line.replace("-- ", "")
                else:
                    line = "-- " + line
                commented_lines.append(line)

            self.insertPlainText("\n".join(commented_lines))
        if event.key() == Qt.Key_Up and event.modifiers() == Qt.ControlModifier:
            self.font_size += 1
            self.update_document_size()
        if event.key() == Qt.Key_Down and event.modifiers() == Qt.ControlModifier:
            self.font_size -= 1
            self.update_document_size()
        if event.key() == Qt.Key_P and event.modifiers() == Qt.ControlModifier:
            self.__insert_code("BASE:I()", -1)
        if event.key() == Qt.Key_M and event.modifiers() == Qt.ControlModifier:
            self.__insert_code("MessageToAll()", -1)
        if event.key() == Qt.Key_QuoteDbl:
            self.__insert_code('"', -1)
        if event.key() == Qt.Key_BraceLeft:
            self.__insert_code("}", -1)
        if event.key() == Qt.Key_BracketLeft:
            self.__insert_code("]", -1)
        if event.key() == Qt.Key_ParenLeft:
            self.__insert_code(")", -1)

        super().keyPressEvent(event)


class FavoritesButton(QPushButton):
    exec_code = Signal(str)
    delete = Signal()
    open_tab_with_code = Signal(str, str)
    def __init__(self, label, code):
        super().__init__()
        self.label = label
        self.code = code
        self.setText(label)
        self.setMaximumWidth(150)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_menu)

    def show_menu(self):
        build_menu_from_action_list(
            [
                {"Delete": self.remove},
                {"Open as tab": self.open_as_tab}
            ])

    def remove(self):
        self.delete.emit()

    def open_as_tab(self):
        self.open_tab_with_code.emit(self.label, self.code)


class FavoritesWidget(QWidget):
    new_button_added = Signal(FavoritesButton)
    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        self.lay = QHBoxLayout()
        self.lay.setSpacing(2)
        self.lay.setContentsMargins(0, 0, 10, 10)
        self.setLayout(self.lay)
        self.layout().setAlignment(Qt.AlignLeft)
        self.setMaximumHeight(35)
        self.setAttribute(Qt.WA_StyledBackground, True)
        # self.setStyleSheet("background-color: white;")

    def add_new_button(self, label, code):
        button = FavoritesButton(label, code)
        self.layout().addWidget(button)
        EZSettings().set(f"btn_{label}", code)

        self.new_button_added.emit(button)
        button.delete.connect(partial(self.delete_button, button))

    def delete_button(self, button):
        button.setParent(None)
        # self.lay.removeWidget(button)
        button.deleteLater()
        EZSettings().remove(f"btn_{button.text()}")

    def dragEnterEvent(self, event):
        event.accept() if event.mimeData().hasText() else event.ignore()

    def dragMoveEvent(self, event):
        event.accept() if event.mimeData().hasText() else event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasText():
            event.setDropAction(Qt.CopyAction)

            label, accepted = QInputDialog().getText(self.parent(), "DCS Code Injector", "Name:")
            if accepted:
                self.add_new_button(label, event.mimeData().text())
            event.accept()
        else:
            event.ignore()


def build_menu_from_action_list(actions, menu=None, is_sub_menu=False):
    if not menu:
        menu = QMenu()

    for action in actions:
        if action == "-":
            menu.addSeparator()
            continue

        for action_title, action_command in action.items():
            if isinstance(action_command, list):
                sub_menu = menu.addMenu(action_title)
                build_menu_from_action_list(action_command, menu=sub_menu, is_sub_menu=True)
                continue

            atn = menu.addAction(action_title)
            atn.triggered.connect(action_command)

    if not is_sub_menu:
        cursor = QCursor()
        menu.exec_(cursor.pos())

    return menu