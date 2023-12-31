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
from PySide6.QtWidgets import (QApplication, QCheckBox, QDialog, QFrame,
    QGridLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QSpacerItem, QSpinBox,
    QVBoxLayout, QWidget)

class Ui_settings_dialog(object):
    def setupUi(self, settings_dialog):
        if not settings_dialog.objectName():
            settings_dialog.setObjectName(u"settings_dialog")
        settings_dialog.resize(1357, 755)
        self.gridLayout = QGridLayout(settings_dialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.btn_browse = QPushButton(settings_dialog)
        self.btn_browse.setObjectName(u"btn_browse")

        self.gridLayout.addWidget(self.btn_browse, 0, 4, 1, 1)

        self.label = QLabel(settings_dialog)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 3, 0, 1, 1)

        self.code_completion_layout = QVBoxLayout()
        self.code_completion_layout.setObjectName(u"code_completion_layout")
        self.label_3 = QLabel(settings_dialog)
        self.label_3.setObjectName(u"label_3")

        self.code_completion_layout.addWidget(self.label_3)

        self.chk_enable_code_completion = QCheckBox(settings_dialog)
        self.chk_enable_code_completion.setObjectName(u"chk_enable_code_completion")
        self.chk_enable_code_completion.setChecked(True)

        self.code_completion_layout.addWidget(self.chk_enable_code_completion)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.txt_mist_url = QLineEdit(settings_dialog)
        self.txt_mist_url.setObjectName(u"txt_mist_url")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.txt_mist_url.sizePolicy().hasHeightForWidth())
        self.txt_mist_url.setSizePolicy(sizePolicy)
        self.txt_mist_url.setMinimumSize(QSize(650, 0))

        self.horizontalLayout_5.addWidget(self.txt_mist_url)

        self.btn_update_mist_data = QPushButton(settings_dialog)
        self.btn_update_mist_data.setObjectName(u"btn_update_mist_data")

        self.horizontalLayout_5.addWidget(self.btn_update_mist_data)

        self.btn_clear_mist = QPushButton(settings_dialog)
        self.btn_clear_mist.setObjectName(u"btn_clear_mist")

        self.horizontalLayout_5.addWidget(self.btn_clear_mist)


        self.code_completion_layout.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.txt_moose_url = QLineEdit(settings_dialog)
        self.txt_moose_url.setObjectName(u"txt_moose_url")
        sizePolicy.setHeightForWidth(self.txt_moose_url.sizePolicy().hasHeightForWidth())
        self.txt_moose_url.setSizePolicy(sizePolicy)
        self.txt_moose_url.setMinimumSize(QSize(650, 0))

        self.horizontalLayout_4.addWidget(self.txt_moose_url)

        self.btn_update_MOOSE_data = QPushButton(settings_dialog)
        self.btn_update_MOOSE_data.setObjectName(u"btn_update_MOOSE_data")

        self.horizontalLayout_4.addWidget(self.btn_update_MOOSE_data)

        self.btn_clear_MOOSE = QPushButton(settings_dialog)
        self.btn_clear_MOOSE.setObjectName(u"btn_clear_MOOSE")

        self.horizontalLayout_4.addWidget(self.btn_clear_MOOSE)


        self.code_completion_layout.addLayout(self.horizontalLayout_4)


        self.gridLayout.addLayout(self.code_completion_layout, 11, 0, 1, 5)

        self.line_2 = QFrame(settings_dialog)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.gridLayout.addWidget(self.line_2, 6, 0, 1, 5)

        self.log_highlighting_rules_layout = QVBoxLayout()
        self.log_highlighting_rules_layout.setObjectName(u"log_highlighting_rules_layout")
        self.btn_add_item = QPushButton(settings_dialog)
        self.btn_add_item.setObjectName(u"btn_add_item")

        self.log_highlighting_rules_layout.addWidget(self.btn_add_item)


        self.gridLayout.addLayout(self.log_highlighting_rules_layout, 8, 0, 1, 5)

        self.verticalSpacer_2 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.gridLayout.addItem(self.verticalSpacer_2, 5, 0, 1, 1)

        self.verticalSpacer_4 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.gridLayout.addItem(self.verticalSpacer_4, 9, 0, 1, 1)

        self.line = QFrame(settings_dialog)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.gridLayout.addWidget(self.line, 13, 0, 1, 5)

        self.temp_folder_4 = QLabel(settings_dialog)
        self.temp_folder_4.setObjectName(u"temp_folder_4")

        self.gridLayout.addWidget(self.temp_folder_4, 1, 0, 1, 1)

        self.txt_log_file = QLineEdit(settings_dialog)
        self.txt_log_file.setObjectName(u"txt_log_file")

        self.gridLayout.addWidget(self.txt_log_file, 0, 1, 1, 3)

        self.spin_offset_time = QSpinBox(settings_dialog)
        self.spin_offset_time.setObjectName(u"spin_offset_time")
        self.spin_offset_time.setMinimum(-12)
        self.spin_offset_time.setMaximum(12)

        self.gridLayout.addWidget(self.spin_offset_time, 1, 1, 1, 1)

        self.temp_folder_3 = QLabel(settings_dialog)
        self.temp_folder_3.setObjectName(u"temp_folder_3")

        self.gridLayout.addWidget(self.temp_folder_3, 0, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.gridLayout.addItem(self.verticalSpacer, 12, 1, 1, 1)

        self.btn_cancel = QPushButton(settings_dialog)
        self.btn_cancel.setObjectName(u"btn_cancel")

        self.gridLayout.addWidget(self.btn_cancel, 14, 3, 1, 1)

        self.btn_save = QPushButton(settings_dialog)
        self.btn_save.setObjectName(u"btn_save")

        self.gridLayout.addWidget(self.btn_save, 14, 4, 1, 1)

        self.chk_play_sound_on_mission_scripting_errors = QCheckBox(settings_dialog)
        self.chk_play_sound_on_mission_scripting_errors.setObjectName(u"chk_play_sound_on_mission_scripting_errors")
        self.chk_play_sound_on_mission_scripting_errors.setChecked(True)
        self.chk_play_sound_on_mission_scripting_errors.setTristate(False)

        self.gridLayout.addWidget(self.chk_play_sound_on_mission_scripting_errors, 3, 1, 1, 1)

        self.label_2 = QLabel(settings_dialog)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 7, 0, 1, 4)

        self.line_3 = QFrame(settings_dialog)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.HLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.gridLayout.addWidget(self.line_3, 10, 0, 1, 5)


        self.retranslateUi(settings_dialog)

        QMetaObject.connectSlotsByName(settings_dialog)
    # setupUi

    def retranslateUi(self, settings_dialog):
        settings_dialog.setWindowTitle(QCoreApplication.translate("settings_dialog", u"Settings", None))
        self.btn_browse.setText(QCoreApplication.translate("settings_dialog", u"Browse ...", None))
        self.label.setText(QCoreApplication.translate("settings_dialog", u"Play sound on mission scripting errors", None))
        self.label_3.setText(QCoreApplication.translate("settings_dialog", u"Code completion", None))
        self.chk_enable_code_completion.setText(QCoreApplication.translate("settings_dialog", u"Enable code completion", None))
        self.txt_mist_url.setText(QCoreApplication.translate("settings_dialog", u"https://raw.githubusercontent.com/mrSkortch/MissionScriptingTools/master/mist.lua", None))
        self.btn_update_mist_data.setText(QCoreApplication.translate("settings_dialog", u"Update Mist data", None))
        self.btn_clear_mist.setText(QCoreApplication.translate("settings_dialog", u"Clear", None))
        self.txt_moose_url.setText(QCoreApplication.translate("settings_dialog", u"https://raw.githubusercontent.com/FlightControl-Master/MOOSE_INCLUDE/master/Moose_Include_Static/Moose_.lua", None))
        self.btn_update_MOOSE_data.setText(QCoreApplication.translate("settings_dialog", u"Update MOOSE  data", None))
        self.btn_clear_MOOSE.setText(QCoreApplication.translate("settings_dialog", u"Clear", None))
        self.btn_add_item.setText(QCoreApplication.translate("settings_dialog", u"Add highlighting item", None))
        self.temp_folder_4.setText(QCoreApplication.translate("settings_dialog", u"Offset log time (hours)", None))
        self.txt_log_file.setPlaceholderText("")
        self.temp_folder_3.setText(QCoreApplication.translate("settings_dialog", u"Log file path", None))
        self.btn_cancel.setText(QCoreApplication.translate("settings_dialog", u"Cancel", None))
        self.btn_save.setText(QCoreApplication.translate("settings_dialog", u"Save", None))
        self.chk_play_sound_on_mission_scripting_errors.setText("")
        self.label_2.setText(QCoreApplication.translate("settings_dialog", u"Log highlighting rules", None))
    # retranslateUi

