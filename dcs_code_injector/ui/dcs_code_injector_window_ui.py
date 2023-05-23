# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dcs_code_injector_window_ui.ui'
##
## Created by: Qt User Interface Compiler version 6.5.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QMainWindow,
    QMenu, QMenuBar, QPlainTextEdit, QSizePolicy,
    QSplitter, QStatusBar, QTabWidget, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(863, 665)
        self.action_settings = QAction(MainWindow)
        self.action_settings.setObjectName(u"action_settings")
        self.action_clear_execution_file = QAction(MainWindow)
        self.action_clear_execution_file.setObjectName(u"action_clear_execution_file")
        self.action_clear_log = QAction(MainWindow)
        self.action_clear_log.setObjectName(u"action_clear_log")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.log_code_splitter = QSplitter(self.centralwidget)
        self.log_code_splitter.setObjectName(u"log_code_splitter")
        self.log_code_splitter.setOrientation(Qt.Vertical)
        self.log_variables_splitter = QSplitter(self.log_code_splitter)
        self.log_variables_splitter.setObjectName(u"log_variables_splitter")
        self.log_variables_splitter.setOrientation(Qt.Horizontal)
        self.txt_log = QPlainTextEdit(self.log_variables_splitter)
        self.txt_log.setObjectName(u"txt_log")
        self.txt_log.setEnabled(True)
        self.log_variables_splitter.addWidget(self.txt_log)
        self.log_code_splitter.addWidget(self.log_variables_splitter)
        self.tab_widget = QTabWidget(self.log_code_splitter)
        self.tab_widget.setObjectName(u"tab_widget")
        self.tab_widget.setAutoFillBackground(True)
        self.tab_widget.setTabsClosable(True)
        self.log_code_splitter.addWidget(self.tab_widget)

        self.gridLayout.addWidget(self.log_code_splitter, 0, 0, 1, 1)

        self.favorites_layout = QHBoxLayout()
        self.favorites_layout.setObjectName(u"favorites_layout")

        self.gridLayout.addLayout(self.favorites_layout, 1, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 863, 22))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuTools = QMenu(self.menubar)
        self.menuTools.setObjectName(u"menuTools")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuTools.menuAction())
        self.menuFile.addAction(self.action_settings)
        self.menuTools.addAction(self.action_clear_log)

        self.retranslateUi(MainWindow)

        self.tab_widget.setCurrentIndex(-1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.action_settings.setText(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.action_clear_execution_file.setText(QCoreApplication.translate("MainWindow", u"Clear execution file", None))
#if QT_CONFIG(shortcut)
        self.action_clear_execution_file.setShortcut(QCoreApplication.translate("MainWindow", u"Alt+X", None))
#endif // QT_CONFIG(shortcut)
        self.action_clear_log.setText(QCoreApplication.translate("MainWindow", u"Clear log", None))
#if QT_CONFIG(shortcut)
        self.action_clear_log.setShortcut(QCoreApplication.translate("MainWindow", u"Alt+L", None))
#endif // QT_CONFIG(shortcut)
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuTools.setTitle(QCoreApplication.translate("MainWindow", u"Tools", None))
    # retranslateUi

