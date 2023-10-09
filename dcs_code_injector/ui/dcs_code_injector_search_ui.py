# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dcs_code_injector_search_ui.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLineEdit, QPushButton,
    QSizePolicy, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(400, 50)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMinimumSize(QSize(400, 50))
        Form.setMaximumSize(QSize(400, 50))
        self.horizontalLayout = QHBoxLayout(Form)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.txt_search = QLineEdit(Form)
        self.txt_search.setObjectName(u"txt_search")
        self.txt_search.setClearButtonEnabled(True)

        self.horizontalLayout.addWidget(self.txt_search)

        self.btn_case_sensitive = QPushButton(Form)
        self.btn_case_sensitive.setObjectName(u"btn_case_sensitive")
        sizePolicy.setHeightForWidth(self.btn_case_sensitive.sizePolicy().hasHeightForWidth())
        self.btn_case_sensitive.setSizePolicy(sizePolicy)
        self.btn_case_sensitive.setMaximumSize(QSize(22, 22))
        self.btn_case_sensitive.setCheckable(True)

        self.horizontalLayout.addWidget(self.btn_case_sensitive)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.btn_case_sensitive.setText(QCoreApplication.translate("Form", u"cC", None))
    # retranslateUi

