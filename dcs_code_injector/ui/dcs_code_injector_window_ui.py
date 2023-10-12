# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dcs_code_injector_window_ui.ui'
##
## Created by: Qt User Interface Compiler version 6.5.3
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
    QMenu, QMenuBar, QSizePolicy, QSplitter,
    QStatusBar, QTabWidget, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(981, 665)
        self.action_settings = QAction(MainWindow)
        self.action_settings.setObjectName(u"action_settings")
        self.action_clear_execution_file = QAction(MainWindow)
        self.action_clear_execution_file.setObjectName(u"action_clear_execution_file")
        self.action_clear_log = QAction(MainWindow)
        self.action_clear_log.setObjectName(u"action_clear_log")
        self.action_add_new_tab = QAction(MainWindow)
        self.action_add_new_tab.setObjectName(u"action_add_new_tab")
        self.action_search = QAction(MainWindow)
        self.action_search.setObjectName(u"action_search")
        self.action_copy_hook_file = QAction(MainWindow)
        self.action_copy_hook_file.setObjectName(u"action_copy_hook_file")
        self.action_increase_log_font_size = QAction(MainWindow)
        self.action_increase_log_font_size.setObjectName(u"action_increase_log_font_size")
        self.action_decrease_log_font_size = QAction(MainWindow)
        self.action_decrease_log_font_size.setObjectName(u"action_decrease_log_font_size")
        self.action_increase_code_font_size = QAction(MainWindow)
        self.action_increase_code_font_size.setObjectName(u"action_increase_code_font_size")
        self.action_decrease_code_font_size = QAction(MainWindow)
        self.action_decrease_code_font_size.setObjectName(u"action_decrease_code_font_size")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.favorites_layout = QHBoxLayout()
        self.favorites_layout.setObjectName(u"favorites_layout")

        self.gridLayout.addLayout(self.favorites_layout, 1, 0, 1, 1)

        self.main_splitter = QSplitter(self.centralwidget)
        self.main_splitter.setObjectName(u"main_splitter")
        self.main_splitter.setOrientation(Qt.Horizontal)
        self.splitter = QSplitter(self.main_splitter)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Vertical)
        self.horizontalLayoutWidget = QWidget(self.splitter)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.txt_log_layout = QHBoxLayout(self.horizontalLayoutWidget)
        self.txt_log_layout.setObjectName(u"txt_log_layout")
        self.txt_log_layout.setContentsMargins(0, 0, 0, 0)
        self.splitter.addWidget(self.horizontalLayoutWidget)
        self.tab_widget = QTabWidget(self.splitter)
        self.tab_widget.setObjectName(u"tab_widget")
        self.tab_widget.setAutoFillBackground(True)
        self.tab_widget.setTabsClosable(True)
        self.splitter.addWidget(self.tab_widget)
        self.main_splitter.addWidget(self.splitter)
        self.variables_splitter = QSplitter(self.main_splitter)
        self.variables_splitter.setObjectName(u"variables_splitter")
        self.variables_splitter.setOrientation(Qt.Vertical)
        self.variablesLayoutWidget = QWidget(self.variables_splitter)
        self.variablesLayoutWidget.setObjectName(u"variablesLayoutWidget")
        self.variables_layout = QVBoxLayout(self.variablesLayoutWidget)
        self.variables_layout.setObjectName(u"variables_layout")
        self.variables_layout.setContentsMargins(0, 0, 0, 0)
        self.variables_splitter.addWidget(self.variablesLayoutWidget)
        self.main_splitter.addWidget(self.variables_splitter)

        self.gridLayout.addWidget(self.main_splitter, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 981, 22))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuTools = QMenu(self.menubar)
        self.menuTools.setObjectName(u"menuTools")
        self.menuView = QMenu(self.menubar)
        self.menuView.setObjectName(u"menuView")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuTools.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menuFile.addAction(self.action_settings)
        self.menuTools.addAction(self.action_add_new_tab)
        self.menuTools.addSeparator()
        self.menuTools.addAction(self.action_clear_log)
        self.menuTools.addAction(self.action_search)
        self.menuTools.addSeparator()
        self.menuTools.addAction(self.action_copy_hook_file)
        self.menuView.addAction(self.action_increase_log_font_size)
        self.menuView.addAction(self.action_decrease_log_font_size)
        self.menuView.addSeparator()
        self.menuView.addAction(self.action_increase_code_font_size)
        self.menuView.addAction(self.action_decrease_code_font_size)

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
        self.action_add_new_tab.setText(QCoreApplication.translate("MainWindow", u"Add new tab", None))
#if QT_CONFIG(shortcut)
        self.action_add_new_tab.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+N", None))
#endif // QT_CONFIG(shortcut)
        self.action_search.setText(QCoreApplication.translate("MainWindow", u"Search Log", None))
#if QT_CONFIG(shortcut)
        self.action_search.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+F", None))
#endif // QT_CONFIG(shortcut)
        self.action_copy_hook_file.setText(QCoreApplication.translate("MainWindow", u"Copy hook file", None))
        self.action_increase_log_font_size.setText(QCoreApplication.translate("MainWindow", u"Increase log font size", None))
#if QT_CONFIG(shortcut)
        self.action_increase_log_font_size.setShortcut(QCoreApplication.translate("MainWindow", u"Shift+Num++", None))
#endif // QT_CONFIG(shortcut)
        self.action_decrease_log_font_size.setText(QCoreApplication.translate("MainWindow", u"Decrease log font size", None))
#if QT_CONFIG(shortcut)
        self.action_decrease_log_font_size.setShortcut(QCoreApplication.translate("MainWindow", u"Shift+Num+-", None))
#endif // QT_CONFIG(shortcut)
        self.action_increase_code_font_size.setText(QCoreApplication.translate("MainWindow", u"Increase code font size", None))
#if QT_CONFIG(shortcut)
        self.action_increase_code_font_size.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl++", None))
#endif // QT_CONFIG(shortcut)
        self.action_decrease_code_font_size.setText(QCoreApplication.translate("MainWindow", u"Decrease code font size", None))
#if QT_CONFIG(shortcut)
        self.action_decrease_code_font_size.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+-", None))
#endif // QT_CONFIG(shortcut)
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuTools.setTitle(QCoreApplication.translate("MainWindow", u"Tools", None))
        self.menuView.setTitle(QCoreApplication.translate("MainWindow", u"View", None))
    # retranslateUi

