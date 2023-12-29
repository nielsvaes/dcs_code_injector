from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtCore import Qt

import re

from .lua_syntax_highlighter import SimpleLuaHighlighter


class CodeTextEdit(QPlainTextEdit):
    def __init__(self):
        """
        Constructor for the CodeTextEdit class.
        Initializes the text edit and sets up the syntax highlighter.
        """

        super().__init__()

        self.font_size = 10
        self.line_numbers_padding = 5
        self.highlight_color = QColor(29, 233, 182)
        self.update_document_size()

        self.line_number_area = LineNumberArea(self)

        self.blockCountChanged.connect(self.update_line_number_area_width)
        self.updateRequest.connect(self.update_line_number_area)
        self.cursorPositionChanged.connect(self.highlight_current_line)

        self.update_line_number_area_width()

        SimpleLuaHighlighter(self.document())

        keywords = ['and', 'break', 'do', 'else', 'elseif', 'end', 'false', 'for', 'function', 'if', 'in', 'local', 'nil', 'not', 'or', 'repeat', 'return', 'then', 'true', 'until', 'while']

        completer = QCompleter(keywords)
        completer.activated.connect(self.insert_completion)
        completer.setWidget(self)
        completer.setCompletionMode(QCompleter.CompletionMode.PopupCompletion)
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.completer = completer
        self.completer.popup().setItemDelegate(PopupItemDelegate())
        self.textChanged.connect(self.complete)

    def insert_completion(self, completion):
        tc = self.textCursor()
        tc.select(QTextCursor.WordUnderCursor)
        if self.text_under_cursor == completion:
            return
        extra = len(completion) - len(self.completer.completionPrefix())
        tc.movePosition(QTextCursor.MoveOperation.Left)
        tc.movePosition(QTextCursor.MoveOperation.EndOfWord)
        tc.insertText(completion[-extra:])
        self.setTextCursor(tc)

    @property
    def text_under_cursor(self):
        tc = self.textCursor()
        tc.select(QTextCursor.SelectionType.WordUnderCursor)
        return tc.selectedText()

    def complete(self):
        prefix = self.text_under_cursor
        if prefix in self.completer.model().stringList():
            return
        self.completer.setCompletionPrefix(prefix)
        popup = self.completer.popup()
        cr: QRect = self.cursorRect()
        cr.setX(cr.x() + 50)

        self.completer.complete(cr)

        popup.setCurrentIndex(self.completer.completionModel().index(0, 0))
        if len(prefix) > 1:
            cr.setWidth(
                self.completer.popup().sizeHintForColumn(0)
                + self.completer.popup().verticalScrollBar().sizeHint().width()
            )
            self.completer.complete(cr)
        else:
            self.completer.popup().hide()

    def get_line_number_area_width(self):
        """
        Returns the space needed for the line number area based number of lines
        :return: int
        """
        digits = 1
        max_value = max(1, self.blockCount())
        while max_value >= 10:
            max_value /= 10
            digits += 1

        space = 3 + self.fontMetrics().horizontalAdvance('9') * digits + self.line_numbers_padding
        return space

    def update_line_number_area_width(self):
        """
        Update the viewport margins based on the space needed by the line number widget

        :return:
        """
        self.setViewportMargins(self.get_line_number_area_width(), 0, 0, 0)

    def update_line_number_area(self, rect, dy):
        """

        :param rect:
        :param dy:
        :return:
        """
        if dy:
            self.line_number_area.scroll(0, dy)
        else:
            self.line_number_area.update(0, rect.y(), self.line_number_area.width(), rect.height())

        if rect.contains(self.viewport().rect()):
            self.update_line_number_area_width()

    def line_number_area_paint_event(self, event):
        """
        Paint the numbers widget

        :param event: The QPaintEvent that triggered this function
        :return: None
        """
        # grab the painter of the line number area widget
        painter = QPainter(self.line_number_area)
        painter.fillRect(event.rect(), QColor(49, 54, 59))

        block = self.firstVisibleBlock()
        block_number = block.blockNumber()

        # Get the top and bottom y-coordinates of the first visible block
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()

        # Loop through all visible blocks
        while block.isValid() and (top <= event.rect().bottom()):
            if block.isVisible() and (bottom >= event.rect().top()):
                number = str(block_number + 1)

                # If this block is the current line, set the pen color to the highlight color
                if block_number == self.textCursor().blockNumber():
                    painter.setPen(self.highlight_color)
                else:
                    # Otherwise, set the pen color to a darker color
                    painter.setPen(self.highlight_color.darker(150))

                # Draw the line number text at the correct position
                painter.drawText(0, top, self.line_number_area.width() - self.line_numbers_padding,
                                 self.fontMetrics().height(),
                                 Qt.AlignRight, number)

            # Move to the next block and update the top and bottom y-coordinates
            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            block_number += 1

        # Draw a vertical line to separate line numbers and code
        painter.setPen(self.highlight_color)
        painter.drawLine(self.line_number_area.width() - 1, event.rect().top(),
                         self.line_number_area.width() - 1, event.rect().bottom())

    def highlight_current_line(self):
        """
        Does what it says on the box

        :return:
        """
        extra_selections = []

        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()

            lineColor = QColor(49, 54, 59).lighter(110)

            selection.format.setBackground(lineColor)
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extra_selections.append(selection)

        self.setExtraSelections(extra_selections)

    def update_document_size(self):
        """
        Updates the document size based on the font size.
        """

        self.setStyleSheet(f"font: {self.font_size}pt 'Courier New';")

    def get_selected_text(self):
        """
        Returns the selected text in the text edit.

        :return: <str> the selected text
        """

        return self.textCursor().selectedText()

    def update_keywords(self):
        text = self.toPlainText()
        matches = re.findall(r'\b([a-zA-Z_][a-zA-Z_0-9]*)\s*=', text)
        for variable_name in matches:
            if variable_name not in self.completer.model().stringList():
                self.completer.model().setStringList(self.completer.model().stringList() + [variable_name])


    def __insert_code(self, text, move_back_pos):
        """
        Inserts the given text at the current cursor position.

        :param text: <str> the text to be inserted
        :param move_back_pos: <int> the number of positions to move the cursor back after inserting the text
        """

        cursor = self.textCursor()
        selected_text = cursor.selection().toPlainText()
        self.insertPlainText(text)
        pos = cursor.position() + move_back_pos
        cursor.setPosition(pos)
        self.setTextCursor(cursor)
        self.insertPlainText(selected_text)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        """
        Handles key press events.

        :param event: <QKeyEvent> the key press event
        """
        if self.completer.popup().isVisible() and event.key() in [
            Qt.Key.Key_Enter,
            Qt.Key.Key_Return,
            Qt.Key.Key_Up,
            Qt.Key.Key_Down,
            Qt.Key.Key_Tab,
            Qt.Key.Key_Backtab,
        ]:
            self.completer.popup().close()
            event.ignore()
            return

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

        self.update_keywords()

        super().keyPressEvent(event)

    def resizeEvent(self, event):
        super().resizeEvent(event)

        cr = self.contentsRect()
        self.line_number_area.setGeometry(QRect(cr.left(), cr.top(), self.get_line_number_area_width(), cr.height()))


class LineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.codeEditor = editor

    def paintEvent(self, event):
        self.codeEditor.line_number_area_paint_event(event)


class PopupItemDelegate(QStyledItemDelegate):
    def sizeHint(self, option, index):
        baseSize = super().sizeHint(option, index)
        return QSize(baseSize.width() * 2, baseSize.height())