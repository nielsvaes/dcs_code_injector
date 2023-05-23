# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dcs_code_injector_settings_ui.ui'
##
## Created by: Qt User Interface Compiler version 6.5.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDialog, QGridLayout, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QSpinBox,
    QWidget)

class Ui_settings_dialog(object):
    def setupUi(self, settings_dialog):
        if not settings_dialog.objectName():
            settings_dialog.setObjectName(u"settings_dialog")
        settings_dialog.resize(495, 112)
        self.gridLayout = QGridLayout(settings_dialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.txt_log_file = QLineEdit(settings_dialog)
        self.txt_log_file.setObjectName(u"txt_log_file")

        self.gridLayout.addWidget(self.txt_log_file, 0, 1, 1, 1)

        self.temp_folder_3 = QLabel(settings_dialog)
        self.temp_folder_3.setObjectName(u"temp_folder_3")

        self.gridLayout.addWidget(self.temp_folder_3, 0, 0, 1, 1)

        self.temp_folder_4 = QLabel(settings_dialog)
        self.temp_folder_4.setObjectName(u"temp_folder_4")

        self.gridLayout.addWidget(self.temp_folder_4, 1, 0, 1, 1)

        self.btn_browse = QPushButton(settings_dialog)
        self.btn_browse.setObjectName(u"btn_browse")

        self.gridLayout.addWidget(self.btn_browse, 0, 2, 1, 1)

        self.spin_offset_time = QSpinBox(settings_dialog)
        self.spin_offset_time.setObjectName(u"spin_offset_time")
        self.spin_offset_time.setMinimum(-12)
        self.spin_offset_time.setMaximum(12)

        self.gridLayout.addWidget(self.spin_offset_time, 1, 1, 1, 2)


        self.retranslateUi(settings_dialog)

        QMetaObject.connectSlotsByName(settings_dialog)
    # setupUi

    def retranslateUi(self, settings_dialog):
        settings_dialog.setWindowTitle(QCoreApplication.translate("settings_dialog", u"Settings", None))
        self.txt_log_file.setPlaceholderText("")
        self.temp_folder_3.setText(QCoreApplication.translate("settings_dialog", u"Log file path", None))
        self.temp_folder_4.setText(QCoreApplication.translate("settings_dialog", u"Offset log time", None))
        self.btn_browse.setText(QCoreApplication.translate("settings_dialog", u"...", None))
    # retranslateUi

