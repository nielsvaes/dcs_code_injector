from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtCore import Qt

import os
import json
import pathlib

from functools import partial
from ez_settings import EZSettings
from datetime import datetime, timedelta

from .settings_dialog import SettingsDialog
from .server import Server
from .code_editor import CodeTextEdit
from .favorites import FavoritesWidget
from .log_view import LogView
from .log_highlighter import LogHighlighter
from .ui.dcs_code_injector_window_ui import Ui_MainWindow

from .constants import sk
from . import versioner

ICON = os.path.join(os.path.dirname(__file__), "ui", "icons", "icon.png")

WINSOUND_OK = False
try:
    import winsound
    WINSOUND_OK = True
except:
    WINSOUND_OK = False



class CodeInjectorWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        """
        Constructor for the CodeInjectorWindow class.
        Initializes the UI and sets up the necessary connections.
        """
        self.init_done = False

        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(ICON))
        self.resize(EZSettings().get(sk.main_win_width, 1280), EZSettings().get(sk.main_win_height, 800))
        self.move(EZSettings().get(sk.main_win_pos_x, 0), EZSettings().get(sk.main_win_pos_y, 0))
        self.setWindowTitle("DCS Code Injector")

        self.favorites_widget = FavoritesWidget()
        self.favorites_layout.addWidget(self.favorites_widget)

        self.last_log_file_size = 0

        self.txt_log = LogView()
        self.txt_log_layout.addWidget(self.txt_log)
        self.log_file = EZSettings().get(sk.log_file, "")
        self.previous = []
        LogHighlighter(self.txt_log.document())
        self.read_log()

        self.connect_ui_signals()
        self.load()

        self.txt_log.setStyleSheet(f"font: {EZSettings().get('log_font_size', 10)}pt 'Courier New';")
        for i in range(self.tab_widget.count()):
            self.tab_widget.widget(i).font_size = EZSettings().get(sk.code_font_size, 10)
            self.tab_widget.widget(i).update_document_size()

        self.server = Server()
        self.server_thread = QThread()
        self.server.moveToThread(self.server_thread)
        self.server_thread.started.connect(self.server.start)
        self.server.connected.connect(self.on_connected)
        self.server.received.connect(self.on_received)
        self.server.disconnected.connect(self.on_disconnected)
        self.server.port_bind_error.connect(self.server_port_bind_error)
        self.server_thread.start()

        self.timer = QTimer()
        self.timer.setInterval(500)
        self.timer.timeout.connect(self.read_log)
        self.timer.start()

        QCoreApplication.instance().aboutToQuit.connect(self.stop_server)

        self.connection_label = QLabel()
        self.statusbar.addWidget(self.connection_label)
        self.on_disconnected()

        self.back_up_settings_file()

        self.show()
        self.init_done = True

    def read_log(self):
        """
        Reads the log file and updates the log view.
        Handles the time shifting for the log entries.
        """

        if not os.path.isfile(self.log_file):
            self.show_settings()
            self.log_file = EZSettings().get(sk.log_file, "")

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
                    shift_hours = EZSettings().get(sk.shift_hours, 0)
                    time += timedelta(hours=shift_hours)
                    shifted_time_str = time.strftime("%Y-%m-%d %H:%M:%S.%f")[:-4]
                    line = line.replace(time_str, shifted_time_str)
                    lines.append(line)
                except:
                    pass

            diff = len(lines) - len(self.previous)
            if diff > 0:
                if diff == len(lines):
                    new_lines = lines
                else:
                    new_lines = lines[-diff:]

                for line in new_lines:
                    line = line.replace("                    ", "   ")
                    time_str = line[0:22]
                    print("new time str", time_str)
                    time = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S.%f")

                    diff = datetime.now() - time
                    print(diff)
                    if ("mission script error" in line.lower() and
                            diff.total_seconds() > 0.7 and
                            self.init_done and
                            EZSettings().get(sk.play_sound_on_mission_scripting_error, True)):
                        self.play_error_sound()

                new_text = "".join(new_lines)
                self.add_text_to_log(new_text)
            self.previous = lines
        self.last_log_file_size = file_size

    def connect_ui_signals(self):
        """
        Connects the UI signals to their respective slots.
        """

        self.tab_widget.tabBarDoubleClicked.connect(self.rename_tab)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        self.action_settings.triggered.connect(self.show_settings)
        self.action_back_up_settings_file.triggered.connect(self.back_up_settings_file)
        self.action_clear_log.triggered.connect(self.clear_log)
        self.action_search.triggered.connect(self.txt_log.toggle_search)
        self.action_add_new_tab.triggered.connect(lambda _: self.add_new_tab(name="UNNAMED", code="-- add code here"))
        self.action_copy_hook_file.triggered.connect(self.copy_hook_file)
        self.action_increase_code_font_size.triggered.connect(lambda _: self.adjust_font_size(self.tab_widget.currentWidget(), True))
        self.action_decrease_code_font_size.triggered.connect(lambda _: self.adjust_font_size(self.tab_widget.currentWidget(), False))
        self.action_increase_log_font_size.triggered.connect(lambda _: self.adjust_font_size(self.txt_log, True))
        self.action_decrease_log_font_size.triggered.connect(lambda _: self.adjust_font_size(self.txt_log, False))

        self.favorites_widget.new_button_added.connect(self.connect_favorite_button)

    def adjust_font_size(self, widget, increase):
        """
        Adjusts the font size of the given widget.

        :param widget: <QWidget> the widget to adjust the font size for
        :param increase: <bool> whether to increase or decrease the font size
        """

        if widget == self.tab_widget.currentWidget():
            size = EZSettings().get(sk.code_font_size, 10)
            if increase:
                size += 1
            else:
                size -= 1
            self.tab_widget.currentWidget().font_size = size
            self.tab_widget.currentWidget().update_document_size()
            EZSettings().set(sk.code_font_size, size)

        elif widget == self.txt_log:
            size = EZSettings().get(sk.log_font_size, 10)
            if increase:
                size += 1
            else:
                size -= 1
            self.txt_log.setStyleSheet(f"font: {size}pt 'Courier New';")
            EZSettings().set(sk.log_font_size, size)

    def on_connected(self):
        """
        Called when the server is connected.
        Updates the connection status in the UI.
        """

        pixmap = QPixmap(os.path.join(os.path.dirname(__file__), "ui", "icons", "cloud_done.png"))
        pixmap = pixmap.scaledToWidth(20, Qt.SmoothTransformation)
        self.connection_label.setPixmap(pixmap)
        self.statusbar.showMessage("Connected to DCS", 2500)

    def on_disconnected(self):
        """
        Called when the server is disconnected.
        Updates the connection status in the UI.
        """

        pixmap = QPixmap(os.path.join(os.path.dirname(__file__), "ui", "icons", "cloud_off.png"))
        pixmap = pixmap.scaledToWidth(20, Qt.SmoothTransformation)
        self.connection_label.setPixmap(pixmap)
        self.statusbar.showMessage("Disconnected from DCS", 2500)

    def stop_server(self):
        """
        Stops the server and waits for the server thread to finish.
        """

        print("killing server")
        self.server.exit = True
        self.server_thread.quit()
        self.server_thread.wait()

    def clear_log(self):
        """
        "Clears" the log view by just adding 60 newlines to push everything up
        """

        self.add_text_to_log("\n" * 60)

    def connect_favorite_button(self, favorite_button):
        """
        Connects the favorite button to its respective slots.

        :param favorite_button: <FavoritesButton> the favorite button to connect
        """

        favorite_button.clicked.connect(partial(self.set_server_response, favorite_button.code))
        favorite_button.open_tab_with_code.connect(partial(self.add_new_tab))

    def close_tab(self, tab_index):
        """
        This closes the tab at index tab_index

        :param tab_index: <int> number of the tab to close
        """
        answer = QMessageBox.question(self, 'Close', "Are you sure you want to remove this tab?", QMessageBox.Yes, QMessageBox.No)
        if answer == QMessageBox.Yes:
            setting_name = f"code__{self.tab_widget.tabText(tab_index)}"
            if tab_index > 0:
                new_index = tab_index - 1
            else:
                new_index = 0

            self.tab_widget.setCurrentIndex(new_index)
            self.tab_widget.removeTab(tab_index)
            EZSettings().remove(setting_name)

    def add_new_tab(self, name=None, code=None):
        """
        Adds a new tab to the tab widget.

        :param name: <str> the name of the new tab
        :param code: <str> the code to be displayed in the new tab
        """

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
        """
        Renames the current tab.
        """

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
        """
        Loads the settings and initializes the UI accordingly.
        """

        for setting in EZSettings().get_all_settings():
            if setting.startswith("code__"):
                self.add_new_tab(name=setting.replace("code__", ""), code=EZSettings().get(setting))
            if setting.startswith("btn_"):
                self.favorites_widget.add_new_button(setting.replace("btn_", ""), EZSettings().get(setting))

    def save_code(self):
        """
        Saves the code in the current tab to the settings.
        """

        tab_name = self.tab_widget.tabText(self.tab_widget.currentIndex())
        code = self.tab_widget.currentWidget().toPlainText()
        if code != "" and not tab_name == "UNNAMED":
            EZSettings().set(f"code__{tab_name}", code)

    def add_code_to_log(self, text):
        """
        Adds the given as a code block to the log view.

        :param text: <str> the text to be added to the log
        """

        line_number = 1
        numbered_lines = ["\n------------------- CODE BLOCK -------------------"]
        for line in text.split("\n"):
            line = f"{str(line_number).zfill(2)}          {line}"
            numbered_lines.append(line)
            line_number += 1
        numbered_lines.append("\n------------------ /CODE BLOCK -------------------\n")
        complete_text = "\n".join(numbered_lines)
        self.add_text_to_log(complete_text)

    def add_text_to_log(self, complete_text):
        """
        Adds the given text to the log view.

        :param complete_text: <str> the text to be added to the log
        """

        self.txt_log.moveCursor(QTextCursor.End)
        self.txt_log.insertPlainText(complete_text)
        self.txt_log.verticalScrollBar().setValue(self.txt_log.verticalScrollBar().maximum())

    def set_server_response(self, code):
        """
        Sets the server response and adds the code to the log. The server response is what's being sent back
        to DCS.

        :param code: <str> the code to be set as the server response
        """

        self.add_code_to_log(code)
        self.server.response = code

    @staticmethod
    def play_error_sound():
        """
        Plays an error sound
        """
        winsound.PlaySound("SystemExit", winsound.SND_ALIAS | winsound.SND_ASYNC)


    def server_port_bind_error(self):
        """
        Is triggered if the server can't bind itself to the port
        """
        self.play_error_sound()
        QMessageBox.critical(self, "DCS Code Injector",
                             f"Can't bind the server on its default port (40322). Is there another instance of DCS Code Injector Running?")

    @staticmethod
    def copy_hook_file():
        """
        Copies the hook file to the Hooks folder.
        """

        from .hook_string import hook_string

        saved_games_hooks_folder = pathlib.Path(EZSettings().get(sk.log_file)).parent.parent / "Scripts" / "Hooks"
        if saved_games_hooks_folder.exists():
            with open(saved_games_hooks_folder / "dcs-code-injector-hook.lua", "w") as writefile:
                writefile.write(hook_string)
        else:
            QMessageBox.warning(None, "DCS Code Injector", "Can't find the Hooks folder! Did you set the path to your dcs.log file in the Settings?")

    @staticmethod
    def on_received(data):
        """
        Handles the data received from the server. This is basically tells the server that the client is still active

        :param data: <str> the data received from the server
        """

        try:
            data = json.loads(data.strip())
            if data.get("connection", "") == "not_active":
                print("connection closed!")

        except json.decoder.JSONDecodeError as err:
            print(err)

    @staticmethod
    def back_up_settings_file():
        """
        Copies the current settings file to a back-up file
        """
        versioner.auto_backup_file(EZSettings().get_file_location())


    @staticmethod
    def show_settings():
        """
        Shows the settings dialog.
        """

        dlg = SettingsDialog()
        dlg.exec_()

    def keyPressEvent(self, event: QKeyEvent) -> None:
        """
        Handles key press events.

        :param event: <QKeyEvent> the key press event
        """

        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return and event.modifiers() == Qt.ControlModifier:
            text = self.tab_widget.currentWidget().textCursor().selection().toPlainText()
            if text == "":
                text = self.tab_widget.currentWidget().toPlainText()
            self.set_server_response(text)

    def closeEvent(self, event):
        """
        Handles the close event of the window, saves the window's position and size before closing

        :param event: <QCloseEvent> the close event
        """

        EZSettings().set(sk.main_win_width, self.width())
        EZSettings().set(sk.main_win_height, self.height())
        EZSettings().set(sk.main_win_pos_x, self.pos().x())
        EZSettings().set(sk.main_win_pos_y, self.pos().y())
        super().closeEvent(event)






