from PySide6.QtWidgets import *
from PySide6.QtGui import *

import os
import random
import json
import shutil
from ez_settings import EZSettings
from qt_material import apply_stylesheet

from .dcs_code_injector_window import CodeInjectorWindow
from .constants import sk, DEFAULT_HIGHLIGHTING_RULES

SETTINGS_DIR = os.path.join(os.path.expanduser('~'),'Documents', "dcs_code_injector")
SETTINGS_PATH = os.path.join(SETTINGS_DIR, "settings.json")
SPLASH_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ui", "splashscreens")

application = QApplication()

def convert_old_settings():
    if not os.path.isfile(SETTINGS_PATH):
        return

    with open(SETTINGS_PATH, "r") as read_file:
        old_data = json.load(read_file)

    if old_data.get(sk.version, -1) < 0:
        print("Converting old settings")
        shutil.copy(SETTINGS_PATH, f"{SETTINGS_PATH}__.OLD")

        new_data = {
            sk.version: 1
        }
        for key, value in old_data.items():
            if not key in dir(sk) and not key.startswith("btn_"):
                new_data[f"code__{key}"] = old_data.get(key)
            else:
                new_data[key] = old_data.get(key)

        with open(SETTINGS_PATH, "w") as write_file:
            json.dump(new_data, write_file, indent=4)

        EZSettings(SETTINGS_PATH)

def check_highlight_rules():
    if not len(EZSettings().get(sk.log_highlight_rules, {})):
        EZSettings().set(sk.log_highlight_rules, DEFAULT_HIGHLIGHTING_RULES)

def main():
    convert_old_settings()

    EZSettings(SETTINGS_PATH)
    check_highlight_rules()

    splashscreens = [os.path.join(SPLASH_DIR, file) for file in os.listdir(SPLASH_DIR) if file.endswith(".png")]
    splash = QSplashScreen(QPixmap(splashscreens[random.randint(0, len(splashscreens) - 1)]))
    splash.show()

    application.processEvents()
    apply_stylesheet(application, "dark_teal.xml")
    win = CodeInjectorWindow()

    splash.finish(win)
    application.exec_()

if __name__ == '__main__':
    main()