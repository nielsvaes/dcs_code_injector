import re

from PySide6.QtWidgets import QMenu
from PySide6.QtGui import QCursor

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