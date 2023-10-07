from PySide6.QtCore import *
from PySide6.QtGui import *
from ez_settings import EZSettings

class LogHighlighter(QSyntaxHighlighter):
    def __init__(self, doc):
        # self.rules = {
        #     r"^.*\b(SCRIPTING)\b.*$": self.make_format(foreground_color=Qt.cyan),
        #     r"^.*\b(WARNING)\b.*$": self.make_format(foreground_color=Qt.yellow),
        #     r"^.*\b(ERROR|stack traceback|in function|in main chunk)\b.*$": self.make_format(Qt.red),
        #     r"^.*(\/E:).*$": self.make_format(Qt.red),
        #     r"^.*\b(ERROR_ONCE)\b.*$": self.make_format(QColor(255, 139, 30)),
        #     r"^.*\b(MOOSE INCLUDE END|MOOSE STATIC INCLUDE START)\b.*$": self.make_format(QColor(54, 194, 72)),
        # }

        self.rules = {}

        for regex, color_list in EZSettings().get("log_highlight_rules").items():
            self.rules[regex] = self.make_format(background_color=QColor(*eval(color_list[0])), foreground_color=QColor(*eval(color_list[1])))

        super().__init__(doc)

    def highlightBlock(self, text: str) -> None:
        for regex, format in self.rules.items():
            i = QRegularExpression(regex).globalMatch(text)
            while i.hasNext():
                match = i.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), format)

    def make_format(self, background_color=Qt.transparent, foreground_color=Qt.white):
        if background_color.alpha() == 0:
            background_color = Qt.transparent
        format = QTextCharFormat()
        format.setBackground(background_color)
        format.setForeground(foreground_color)
        return format
