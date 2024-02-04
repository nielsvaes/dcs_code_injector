from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtCore import Qt

import re
from ez_settings import EZSettings
from .constants import sk, lua_keywords
from .lua_syntax_highlighter import SimpleLuaHighlighter


class CodeTextEdit(QPlainTextEdit):
    def __init__(self):
        """
        Constructor for the CodeTextEdit class.
        Initializes the text edit and sets up the syntax highlighter.
        """

        super().__init__()

        self.font_size = EZSettings().get(sk.code_font_size, 10)
        self.font = EZSettings().get(sk.code_font, sk.default_font)
        self.update_font()

        self.line_numbers_padding = 5
        self.highlight_color = QColor(29, 233, 182)

        self.line_number_area = LineNumberArea(self)

        self.blockCountChanged.connect(self.update_line_number_area_width)
        self.updateRequest.connect(self.update_line_number_area)
        self.cursorPositionChanged.connect(self.highlight_current_line)

        self.update_line_number_area_width()

        SimpleLuaHighlighter(self.document())

        keywords = EZSettings().get(sk.MOOSE_autocomplete, []) + EZSettings().get(sk.mist_autocomplete, []) + lua_keywords


        self.completer = CustomCompleter(keywords)
        self.completer.activated.connect(self.insert_completion)
        self.completer.setWidget(self)
        self.completer.setCompletionMode(QCompleter.CompletionMode.PopupCompletion)
        self.completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.completer.popup().setItemDelegate(PopupItemDelegate())
        self.completer.popup().setStyleSheet("""
                                                QListView::item {
                                                    min-height: 18px;
                                                    max-height: 18px;
                                                    font: 'Courier New'
                                                },
                                            """)
        self.textChanged.connect(self.complete)
        self.previous_block_number = -1

    def insert_completion(self, completion):
        """
        Inserts the autocompletion text into the document at the cursor's position.

        Parameters:
        completion (str): The autocompletion text to be inserted.
        """

        tc: QTextCursor = self.textCursor()

        # Get the length of the text that has been typed by the user
        length_of_typed_text = len(self.completer.completionPrefix())

        # Move the cursor backwards by the length of the typed text
        tc.movePosition(QTextCursor.Left, QTextCursor.KeepAnchor, length_of_typed_text)

        # Replace the selected text (the typed text) with the completion
        tc.insertText(completion)

        self.setTextCursor(tc)

    def get_word_before_cursor(self):
        """
        Returns the word before the cursor.
        The word is determined by moving the cursor backwards until a whitespace, newline, or the start of the document is encountered.
        """

        cursor_pos = self.textCursor().position()  # get current cursor position
        text_up_to_cursor = self.toPlainText()[:cursor_pos]  # get text up to cursor

        # split the text into words by spaces, newline characters or non-alphanumeric characters
        words = re.split(r'[\s{\[\("\'|\\]+', text_up_to_cursor)

        # the last word in the list will be the word you want
        if words:
            selected_word = words[-1]
        else:
            selected_word = ""
        return selected_word

    def complete(self):
        """
        Performs autocompletion based on the current word under the cursor.

        If the word under the cursor is in the completer's list, it does nothing.
        Otherwise, it sets the completion prefix to the word under the cursor and opens the completer's popup
        at the current cursor's rectangle. If the completion prefix length is greater than 1, it also adjusts
        the width of the completer's popup based on the size hint of the first column and the vertical scrollbar.
        """

        if not EZSettings().get(sk.enable_code_completion, True):
            return

        prefix = self.get_word_before_cursor()
        if prefix in self.completer.model().stringList():
            return

        # Check if the cursor is at the end of the document or on a new line
        cursor = self.textCursor()
        if cursor.block().length() <= 1:
            return

        self.completer.setCompletionPrefix(prefix)
        self.completer.popup().hide()
        popup = self.completer.popup()
        rect: QRect = self.cursorRect()
        rect.setX(rect.x() + 55)
        self.completer.complete(rect)

        if len(prefix) > 1:
            popup.setCurrentIndex(self.completer.completionModel().index(0, 0))
            rect.setWidth(
                self.completer.popup().sizeHintForColumn(0)
                + self.completer.popup().verticalScrollBar().sizeHint().width()
            )
            self.completer.complete(rect)
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

    def get_selected_text(self):
        """
        Returns the selected text in the text edit.

        :return: <str> the selected text
        """

        return self.textCursor().selectedText()

    def update_keywords(self):
        text = self.toPlainText()
        matches = re.findall(r'\b([a-zA-Z_][a-zA-Z_0-9]*)\s*=|function\s+(.*)', text)
        for match in matches:
            # match is a tuple where the first item is the variable name before "=" (if any)
            # and the second item is everything after "function " until the end of the line (if any)
            variable_name, function_signature = match
            if variable_name and variable_name not in self.completer.model().stringList():
                self.completer.model().setStringList(list(set(self.completer.model().stringList() + [variable_name])))
            if function_signature and function_signature not in self.completer.model().stringList():
                self.completer.model().setStringList(
                    list(set(self.completer.model().stringList() + [function_signature])))

    def set_font(self, font):
        self.font = font
        EZSettings().set(sk.code_font, font)

    def set_font_size(self, font_size):
        self.font_size = font_size
        EZSettings().set(sk.code_font_size, font_size)

    def update_font(self):
        self.setStyleSheet(f"font: {self.font_size}pt '{self.font}';")

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

    def check_cursor_position(self):
        cursor = self.textCursor()
        block_number = cursor.blockNumber()
        if block_number != self.previous_block_number:
            self.previous_block_number = block_number
            self.update_keywords()

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self.check_cursor_position()

    def keyPressEvent(self, event: QKeyEvent) -> None:
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
            self.handle_control_slash()
        elif event.key() == Qt.Key_Up and event.modifiers() == Qt.ControlModifier:
            self.handle_control_up()
        elif event.key() == Qt.Key_Down and event.modifiers() == Qt.ControlModifier:
            self.handle_control_down()
        elif event.key() == Qt.Key_P and event.modifiers() == Qt.ControlModifier:
            self.handle_control_p()
        elif event.key() == Qt.Key_Tab:
            self.handle_tab()
        elif event.key() == Qt.Key_Backtab:
            self.handle_backtab()
        elif event.key() in (Qt.Key_Up, Qt.Key_Down):
            super().keyPressEvent(event)
            self.check_cursor_position()
        elif event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            cursor = self.textCursor()
            current_line = cursor.block().text()
            indentation = re.match(r"\s*", current_line).group()  # Capture leading whitespace
            super().keyPressEvent(event)  # Call the parent method to insert the newline
            self.insertPlainText(indentation)  # Insert the captured indentation
            self.check_cursor_position()
        elif event.key() == Qt.Key_Backspace:
            cursor = self.textCursor()
            text_up_to_cursor = self.toPlainText()[:cursor.position()]
            if text_up_to_cursor.endswith('    '):  # Check if the cursor is preceded by 4 spaces
                cursor.movePosition(QTextCursor.Left, QTextCursor.KeepAnchor, 4)
                cursor.removeSelectedText()
                return  # Prevent calling super().keyPressEvent(event) to avoid deleting an extra character
            else:
                super().keyPressEvent(event)
        else:
            super().keyPressEvent(event)

    def handle_control_slash(self):
        cursor = self.textCursor()
        selected_text = cursor.selection().toPlainText()
        lines = selected_text.split("\n")
        commented_lines = []
        for line in lines:
            if line.startswith("-- "):
                line = line.replace("-- ", "", 1)  # only replace the first occurrence
            else:
                line = "-- " + line
            commented_lines.append(line)

        # replace the selected text with the commented lines
        cursor.insertText("\n".join(commented_lines))

    def handle_control_up(self):
        self.font_size += 1
        self.update_document_size()

    def handle_control_down(self):
        self.font_size -= 1
        self.update_document_size()

    def handle_control_p(self):
        self.__insert_code("BASE:I()", -1)

    def handle_special_characters(self, event):
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.Right, QTextCursor.KeepAnchor)
        if cursor.selectedText() == event.text():
            cursor.movePosition(QTextCursor.MoveOperation.Right)
            self.setTextCursor(cursor)
            return

        if event.key() == Qt.Key_QuoteDbl:
            self.__insert_code('"' * 2, -1)
        elif event.key() == Qt.Key_Apostrophe:
            self.__insert_code("'" * 2, -1)
        elif event.key() == Qt.Key_BraceLeft:
            self.__insert_code("}" * 2, -1)
        elif event.key() == Qt.Key_BracketLeft:
            self.__insert_code("]" * 2, -1)
        elif event.key() == Qt.Key_ParenLeft:
            self.__insert_code(")" * 2, -1)

    def handle_tab(self):
        cursor = self.textCursor()
        start = cursor.selectionStart()
        end = cursor.selectionEnd()

        # Swap start and end if start is greater than end
        if start > end:
            start, end = end, start

        selected_text = self.document().toPlainText()[start:end]
        if selected_text.strip() == '':
            # If the selected text is empty or contains only spaces, insert 4 spaces
            cursor.insertText('    ')
        else:
            # Otherwise, indent each line
            lines = selected_text.split("\n")
            indented_lines = ['    ' + line for line in lines]
            cursor.setPosition(start)
            cursor.setPosition(end, QTextCursor.KeepAnchor)
            cursor.insertText("\n".join(indented_lines))

            cursor.setPosition(start)
            cursor.setPosition(start + len("\n".join(indented_lines)), QTextCursor.KeepAnchor)
            self.setTextCursor(cursor)

    def handle_backtab(self):
        cursor = self.textCursor()
        start = cursor.selectionStart()
        end = cursor.selectionEnd()

        # Swap start and end if start is greater than end
        if start > end:
            start, end = end, start

        selected_text = self.document().toPlainText()[start:end]
        if selected_text.strip() == '':
            # If the selected text is empty or contains only spaces, remove 4 spaces if they exist
            text_up_to_cursor = self.toPlainText()[:start]
            if text_up_to_cursor.endswith(' ' * 4):
                cursor.setPosition(start - 4)
                cursor.setPosition(start, QTextCursor.KeepAnchor)
                cursor.removeSelectedText()
        else:
            # Otherwise, unindent each line
            lines = selected_text.split("\n")
            unindented_lines = [line[4:] if line.startswith('    ') else line for line in lines]
            cursor.setPosition(start)
            cursor.setPosition(end, QTextCursor.KeepAnchor)
            cursor.insertText("\n".join(unindented_lines))

            cursor.setPosition(start)
            cursor.setPosition(start + len("\n".join(unindented_lines)), QTextCursor.KeepAnchor)
            self.setTextCursor(cursor)

    def resizeEvent(self, event):
        super().resizeEvent(event)

        content_rect = self.contentsRect()
        self.line_number_area.setGeometry(
            QRect(content_rect.left(), content_rect.top(), self.get_line_number_area_width(), content_rect.height()))


class LineNumberArea(QWidget):
    """
    A custom QWidget that displays line numbers for a CodeTextEdit.
    """

    def __init__(self, editor):
        super().__init__(editor)
        self.codeEditor = editor

    def paintEvent(self, event):
        """
        Handles the paint event for the line number area. Draws line numbers and highlights the current line.

        Parameters:
        event (QPaintEvent): The paint event.
        """
        self.codeEditor.line_number_area_paint_event(event)


class PopupItemDelegate(QStyledItemDelegate):
    """
    A custom QStyledItemDelegate that provides custom size hint for QCompleter popup items.
    """

    def paint(self, painter, option, index):
        font = QFont("Courier New")
        font.setPointSize(10)
        option.font = font

        super().paint(painter, option, index)

    def sizeHint(self, option, index):
        """
        Returns the size hint for the given index and style option.

        Parameters:
        option (QStyleOptionViewItem): The style option for the item.
        index (QModelIndex): The model index for the item.

        Returns:
        QSize: The size hint for the item.
        """

        base_size = super().sizeHint(option, index)
        return QSize(base_size.width() * 2, base_size.height())


class CustomCompleter(QCompleter):
    def splitPath(self, path):
        return [path]
