from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtCore import Qt

from ez_settings import EZSettings
from functools import partial

from .utils import build_menu_from_action_list

class FavoritesButton(QPushButton):
    exec_code = Signal(str)
    delete = Signal()
    open_tab_with_code = Signal(str, str)
    def __init__(self, label, code):
        """
        Constructor for the FavoritesButton class.

        :param label: <str> the label of the button
        :param code: <str> the code associated with the button
        """

        super().__init__()
        self.label = label
        self.code = code
        self.setText(label)
        self.setMaximumWidth(150)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_menu)

    def show_menu(self):
        """
        Shows the context menu for the button.
        """

        build_menu_from_action_list(
            [
                {"Delete": self.remove},
                {"Open as tab": self.open_as_tab}
            ])

    def remove(self):
        """
        Emits the delete signal that will delete the button in the main window
        """

        self.delete.emit()

    def open_as_tab(self):
        """
        Emits the open_tab_with_code signal with the button's label and code to open a tab in the main window
        """

        self.open_tab_with_code.emit(self.label, self.code)


class FavoritesWidget(QWidget):
    new_button_added = Signal(FavoritesButton)
    def __init__(self):
        """
        Constructor for the FavoritesWidget class.
        """

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
        """
        Adds a new button to the widget.

        :param label: <str> the label of the button
        :param code: <str> the code associated with the button
        """

        button = FavoritesButton(label, code)
        self.layout().addWidget(button)
        EZSettings().set(f"btn_{label}", code)

        self.new_button_added.emit(button)
        button.delete.connect(partial(self.delete_button, button))

    def delete_button(self, button):
        """
        Deletes the given button from the widget.

        :param button: <FavoritesButton> the button to delete
        """

        button.setParent(None)
        # self.lay.removeWidget(button)
        button.deleteLater()
        EZSettings().remove(f"btn_{button.text()}")

    def dragEnterEvent(self, event):
        """
        Handles the drag enter event.

        :param event: <QDragEnterEvent> the drag enter event
        """

        event.accept() if event.mimeData().hasText() else event.ignore()

    def dragMoveEvent(self, event):
        """
        Handles the drag move event.

        :param event: <QDragMoveEvent> the drag move event
        """

        event.accept() if event.mimeData().hasText() else event.ignore()

    def dropEvent(self, event):
        """
        Handles the drop event.

        :param event: <QDropEvent> the drop event
        """

        if event.mimeData().hasText():
            event.setDropAction(Qt.CopyAction)

            label, accepted = QInputDialog().getText(self.parent(), "DCS Code Injector", "Name:")
            if accepted:
                self.add_new_button(label, event.mimeData().text())
            event.accept()
        else:
            event.ignore()