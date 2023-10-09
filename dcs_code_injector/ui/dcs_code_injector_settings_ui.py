# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dcs_code_injector_settings_ui.ui'
##
## Created by: Qt User Interface Compiler version 6.5.3
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
from PySide6.QtWidgets import (QApplication, QDialog, QFrame, QGridLayout,
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QSpacerItem, QSpinBox, QVBoxLayout, QWidget)

class Ui_settings_dialog(object):
    def setupUi(self, settings_dialog):
        if not settings_dialog.objectName():
            settings_dialog.setObjectName(u"settings_dialog")
        settings_dialog.resize(944, 544)
        self.gridLayout = QGridLayout(settings_dialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.temp_folder_4 = QLabel(settings_dialog)
        self.temp_folder_4.setObjectName(u"temp_folder_4")

        self.gridLayout.addWidget(self.temp_folder_4, 1, 0, 1, 1)

        self.btn_cancel = QPushButton(settings_dialog)
        self.btn_cancel.setObjectName(u"btn_cancel")

        self.gridLayout.addWidget(self.btn_cancel, 8, 3, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.gridLayout.addItem(self.verticalSpacer, 6, 1, 1, 1)

        self.temp_folder_3 = QLabel(settings_dialog)
        self.temp_folder_3.setObjectName(u"temp_folder_3")

        self.gridLayout.addWidget(self.temp_folder_3, 0, 0, 1, 1)

        self.line = QFrame(settings_dialog)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.gridLayout.addWidget(self.line, 7, 0, 1, 5)

        self.label_2 = QLabel(settings_dialog)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 4, 0, 1, 4)

        self.spin_offset_time = QSpinBox(settings_dialog)
        self.spin_offset_time.setObjectName(u"spin_offset_time")
        self.spin_offset_time.setMinimum(-12)
        self.spin_offset_time.setMaximum(12)

        self.gridLayout.addWidget(self.spin_offset_time, 1, 1, 1, 1)

        self.btn_browse = QPushButton(settings_dialog)
        self.btn_browse.setObjectName(u"btn_browse")

        self.gridLayout.addWidget(self.btn_browse, 0, 4, 1, 1)

        self.btn_save = QPushButton(settings_dialog)
        self.btn_save.setObjectName(u"btn_save")

        self.gridLayout.addWidget(self.btn_save, 8, 4, 1, 1)

        self.txt_log_file = QLineEdit(settings_dialog)
        self.txt_log_file.setObjectName(u"txt_log_file")

        self.gridLayout.addWidget(self.txt_log_file, 0, 1, 1, 3)

        self.log_highlighting_rules_layout = QVBoxLayout()
        self.log_highlighting_rules_layout.setObjectName(u"log_highlighting_rules_layout")
        self.btn_add_item = QPushButton(settings_dialog)
        self.btn_add_item.setObjectName(u"btn_add_item")

        self.log_highlighting_rules_layout.addWidget(self.btn_add_item)


        self.gridLayout.addLayout(self.log_highlighting_rules_layout, 5, 0, 1, 5)

        self.verticalSpacer_2 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.gridLayout.addItem(self.verticalSpacer_2, 3, 0, 1, 1)


        self.retranslateUi(settings_dialog)

        QMetaObject.connectSlotsByName(settings_dialog)
    # setupUi

    def retranslateUi(self, settings_dialog):
        settings_dialog.setWindowTitle(QCoreApplication.translate("settings_dialog", u"Settings", None))
        self.temp_folder_4.setText(QCoreApplication.translate("settings_dialog", u"Offset log time (hours)", None))
        self.btn_cancel.setText(QCoreApplication.translate("settings_dialog", u"Cancel", None))
        self.temp_folder_3.setText(QCoreApplication.translate("settings_dialog", u"Log file path", None))
        self.label_2.setText(QCoreApplication.translate("settings_dialog", u"Log highlighting rules", None))
        self.btn_browse.setText(QCoreApplication.translate("settings_dialog", u"Browse ...", None))
        self.btn_save.setText(QCoreApplication.translate("settings_dialog", u"Save", None))
        self.txt_log_file.setPlaceholderText("")
        self.btn_add_item.setText(QCoreApplication.translate("settings_dialog", u"Add highlighting item", None))
    # retranslateUi

