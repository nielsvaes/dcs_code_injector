import re

from PySide6.QtWidgets import *
from PySide6.QtGui import *

from qt_material import apply_stylesheet

from time import time
from functools import wraps

def check_regex(s):
    try:
        re.compile(s)
    except re.error:
        return False
    return True

def build_menu_from_action_list(actions, menu=None, is_sub_menu=False):
    """
    Builds a menu from a list of actions.

    :param actions: <list> the list of actions
    :param menu: <QMenu> the menu to add the actions to
    :param is_sub_menu: <bool> whether the menu is a sub-menu
    :return: <QMenu> the menu with the added actions
    """

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

def create_dark_palette():
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, Qt.white)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, Qt.black)
    return palette


def set_application_style(style):
    if style == "Material Neon":
        apply_stylesheet(qApp, "dark_teal.xml")
    elif style == "Fusion Dark":
        qApp.setStyle("Fusion")
        qApp.setPalette(create_dark_palette())

def timeit(func):
    @wraps(func)
    def wrap_func(*args, **kwargs):
        t1 = time()
        result = func(*args, **kwargs)
        t2 = time()
        print(f'Function {func.__name__!r} executed in {(t2-t1):.4f}s')
        return result
    return wrap_func