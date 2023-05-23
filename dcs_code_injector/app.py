from PySide6.QtWidgets import *
from PySide6.QtGui import *
import os
import random
import time
from ez_settings import EZSettings
from qt_material import apply_stylesheet
from .dcs_code_injector_window import CodeInjectorWindow


SETTINGS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "settings.json")
SPLASH_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ui", "splashscreens")
EZSettings(SETTINGS_PATH)

application = QApplication()

def main():
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