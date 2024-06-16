from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *

import json
import pathlib
import socket
import time

from functools import partial
from ez_settings import EZSettings

from .settings_dialog import SettingsDialog
from .version_dialog import AboutDialog
from .code_editor import CodeTextEdit
from .favorites import FavoritesWidget
from .log_view import LogView
from .ui.dcs_code_injector_window_ui import Ui_MainWindow

from .constants import sk
from . import versioner

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
        self.resize(EZSettings().get(sk.main_win_width, 1280), EZSettings().get(sk.main_win_height, 800))
        self.move(EZSettings().get(sk.main_win_pos_x, 0), EZSettings().get(sk.main_win_pos_y, 0))
        self.setWindowTitle("DCS Code Injector")

        self.favorites_widget = FavoritesWidget()
        self.favorites_layout.addWidget(self.favorites_widget)

        self.about_dialog = AboutDialog()

        self.txt_log = LogView()
        self.txt_log.showSettings.connect(self.show_settings)
        self.txt_log.playErrorSound.connect(self.play_error_sound)
        self.txt_log_layout.addWidget(self.txt_log)

        self.connect_ui_signals()
        self.load()

        self.back_up_settings_file()
        if EZSettings().get(sk.copy_hook_on_startup, False):
            self.copy_hook_file()

        self.show()
        self.init_done = True

    def connect_ui_signals(self):
        """
        Connects the UI signals to their respective slots.
        """

        self.tab_widget.tabBarDoubleClicked.connect(self.rename_tab)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)

        self.action_settings.triggered.connect(self.show_settings)
        self.action_back_up_settings_file.triggered.connect(self.back_up_settings_file)
        self.action_clear_log.triggered.connect(self.txt_log.clear)
        self.action_search.triggered.connect(self.txt_log.toggle_search)
        self.action_add_new_tab.triggered.connect(lambda _: self.add_new_tab(name="UNNAMED", code="-- add code here"))
        self.action_copy_hook_file.triggered.connect(self.copy_hook_file)
        self.action_increase_code_font_size.triggered.connect(lambda _: self.adjust_font_size(self.tab_widget.currentWidget(), True))
        self.action_decrease_code_font_size.triggered.connect(lambda _: self.adjust_font_size(self.tab_widget.currentWidget(), False))
        self.action_log_view_enabled.toggled.connect(self.enabled_log_view)
        self.action_pick_log_font.triggered.connect(lambda _: self.pick_font("log"))
        self.action_increase_log_font_size.triggered.connect(lambda _: self.adjust_font_size(self.txt_log, True))
        self.action_decrease_log_font_size.triggered.connect(lambda _: self.adjust_font_size(self.txt_log, False))
        self.action_pick_code_font.triggered.connect(lambda _: self.pick_font("code"))
        self.action_material_neon.triggered.connect(lambda: self.set_application_style(sk.theme_material_neon))
        self.action_fusion_dark.triggered.connect(lambda: self.set_application_style(sk.theme_fusion_dark))
        self.action_about.triggered.connect(lambda: self.about_dialog.exec_())

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

    def connect_favorite_button(self, favorite_button):
        """
        Connects the favorite button to its respective slots.

        :param favorite_button: <FavoritesButton> the favorite button to connect
        """

        favorite_button.clicked.connect(partial(self.send_code, favorite_button.code))
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
        code_text_edit.execute_code.connect(self.send_code)
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

    def enabled_log_view(self):
        enable = self.action_log_view_enabled.isChecked()
        self.txt_log.enable_updating(enable)
        if enable:
            self.splitter.setSizes([500, 200])
        else:
            self.splitter.setSizes([0, 4000])

    def load(self):
        """
        Loads the settings and initializes the UI accordingly.
        """

        for setting in EZSettings().get_all_settings():
            if setting.startswith("code__"):
                self.add_new_tab(name=setting.replace("code__", ""), code=EZSettings().get(setting))
            if setting.startswith("btn_"):
                self.favorites_widget.add_new_button(setting.replace("btn_", ""), EZSettings().get(setting))

        self.action_log_view_enabled.setChecked(EZSettings().get(sk.update_log_view, True))

    def save_code(self):
        """
        Saves the code in the current tab to the settings.
        """

        tab_name = self.tab_widget.tabText(self.tab_widget.currentIndex())
        code = self.tab_widget.currentWidget().toPlainText()
        if code != "" and not tab_name == "UNNAMED":
            EZSettings().set(f"code__{tab_name}", code)

    def add_code_to_log(self, text, header_text="CODE BLOCK"):
        """
        Adds the given as a code block to the log view.

        :param text: <str> the text to be added to the log
        :param header_text: <str> text for the header that wraps the code
        """

        line_number = 1
        numbered_lines = [f"\n------------------- {header_text} -------------------"]
        for line in text.split("\n"):
            line = f"{str(line_number).zfill(2)}          {line}"
            numbered_lines.append(line)
            line_number += 1
        numbered_lines.append(f"\n------------------ /{header_text} -------------------\n")
        complete_text = "\n".join(numbered_lines)
        self.txt_log.add_text(complete_text)

    def send_code(self, code):
        self.add_code_to_log(code)
        self.statusbar.showMessage("Trying to send data...")
        self.stop_button = QPushButton("Stop")
        self.statusbar.addPermanentWidget(self.stop_button)
        self.stop_button.clicked.connect(self.stop_sending)

        self.thread = QThread()  # Create a new QThread
        self.worker = CodeSenderWorker(code)  # Create a worker object
        self.worker.moveToThread(self.thread)  # Move the worker to the thread

        # Connect signals
        self.thread.started.connect(self.worker.send_code)
        self.worker.finished.connect(self.on_send_finished)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.update_status.connect(self.add_code_to_log)

        self.thread.start()

    def stop_sending(self):
        self.worker.stop()  # Stop the worker
        self.statusbar.clearMessage()
        self.statusbar.removeWidget(self.stop_button)

    def on_send_finished(self, success, message):
        if success:
            self.statusbar.showMessage(message, 5000)
        else:
            self.add_code_to_log(message, "CODE INJECTOR ERROR")
        self.statusbar.removeWidget(self.stop_button)
        self.statusbar.clearMessage()

    def pick_font(self, view):
        font: QFont
        ok, font = QFontDialog.getFont()
        if ok:
            if view == "log":
                self.txt_log.set_font(font.family())
                self.txt_log.set_font_size(font.pointSize())
            elif view == "code":
                for i in range(self.tab_widget.count()):
                    self.tab_widget.widget(i).set_font(font.family())
                    self.tab_widget.widget(i).set_font_size(font.pointSize())
                    self.tab_widget.widget(i).update_font()

    @staticmethod
    def set_application_style(style):
        EZSettings().set(sk.theme, style)
        QMessageBox().information(None, "Info",
                                  "Restart the application to apply the new theme")

    @staticmethod
    def play_error_sound():
        """
        Plays an error sound
        """
        winsound.PlaySound("SystemExit", winsound.SND_ALIAS | winsound.SND_ASYNC)

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



class CodeSenderWorker(QObject):
    finished = Signal(bool, str)  # Signal to indicate the operation is finished
    update_status = Signal(str)   # Signal to update the status bar message

    def __init__(self, code):
        super().__init__()
        self.code = code
        self.is_running = True

    def send_code(self):
        start_time = time.time()
        while self.is_running and (time.time() - start_time) < 3:
            try:
                s = socket.socket()
                # s.settimeout(0.5)
                s.connect(('localhost', 45221))
                s.sendall(self.code.encode())
                response = s.recv(1024).decode()
                if "MSG_OK" in response:
                    self.finished.emit(True, "Data sent successfully")
                    return
                else:
                    self.update_status.emit(f"ERROR: Received unexpected response from server: {response}")
            except (ConnectionRefusedError, TimeoutError, socket.error) as err:
                pass
                # self.update_status.emit(f"ERROR: {err}\nIs DCS running?")
            finally:
                s.close()
                if not self.is_running:
                    break
                time.sleep(0.1)

        self.finished.emit(False, "Failed to connect within 3 seconds")

    def stop(self):
        self.is_running = False



