# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'StartWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.6.3
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
from PySide6.QtWidgets import (QApplication, QComboBox, QHBoxLayout, QLabel,
    QLayout, QLineEdit, QMainWindow, QMenuBar,
    QPushButton, QSizePolicy, QSpacerItem, QStatusBar,
    QVBoxLayout, QWidget)
from PySide6 import QtCore
import pyqtgraph as pg



class Ui_Start(object):
    def setupUi(self, Start):
        if not Start.objectName():
            Start.setObjectName(u"Start")
        Start.resize(700, 700)
        self.centralwidget = QWidget(Start)
        self.centralwidget.setObjectName(u"centralwidget")

        self.horizontalLayout_3 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalSpacer_4 = QSpacerItem(20, 50, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_4)

        # self.microscope_image = QLabel(self.centralwidget)
        # self.microscope_image.setObjectName(u"microscope_image")
        # self.microscope_image.setPixmap(QPixmap(u"resources/images/icons8-microscope-50"))
        # self.microscope_image.setAlignment(Qt.AlignCenter)

        # self.verticalLayout_2.addWidget(self.microscope_image)

        self.title = QLabel(self.centralwidget)
        self.title.setObjectName(u"title")
        font = QFont()
        font.setPointSize(34)
        self.title.setFont(font)
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setProperty("class", "title_text")

        self.verticalLayout_2.addWidget(self.title)

        self.verticalSpacer = QSpacerItem(20, 70, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")

        self.ms_image = pg.PlotWidget()
        self.ms_image.setBackground("#31363B")

        axis_styles = {"font-size": "14px", "text-align": "left", "font-family": "roboto", "color": "#ffffff", "font-weight": "normal"}
        self.ms_image.setLabel("left", "Intensidad", **axis_styles)
        self.ms_image.setLabel("bottom", "Masa (Da)", **axis_styles)


        self.ms_image.setObjectName(u"ms_image")

        self.horizontalLayout_9.addWidget(self.ms_image)


        self.verticalLayout_2.addLayout(self.horizontalLayout_9)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        # self.bacteria_image = QLabel(self.centralwidget)
        # self.bacteria_image.setObjectName(u"bacteria_image")
        # self.bacteria_image.setPixmap(QPixmap(u"resources/images/icons8-bacteria-50.png"))
        # self.bacteria_image.setAlignment(Qt.AlignCenter)

        # self.verticalLayout_4.addWidget(self.bacteria_image)

        self.bacteria_header = QLabel(self.centralwidget)
        self.bacteria_header.setObjectName(u"bacteria_header")
        self.bacteria_header.setEnabled(True)
        self.bacteria_header.setAlignment(Qt.AlignCenter)

        self.verticalLayout_4.addWidget(self.bacteria_header)

        self.bacteria_select = QComboBox(self.centralwidget)
        self.bacteria_select.setObjectName(u"bacteria_select")
        self.bacteria_select.setEnabled(True)
        self.bacteria_select.setEditable(False)

        self.verticalLayout_4.addWidget(self.bacteria_select)


        self.horizontalLayout_8.addLayout(self.verticalLayout_4)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_2)


        self.verticalLayout_3.addLayout(self.horizontalLayout_8)


        self.horizontalLayout.addLayout(self.verticalLayout_3)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")

        self.verticalLayout_2.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_5)

        self.file_name = QLineEdit(self.centralwidget)
        self.file_name.setObjectName(u"file_name")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.file_name.sizePolicy().hasHeightForWidth())
        self.file_name.setSizePolicy(sizePolicy)
        self.file_name.setMinimumSize(QSize(250, 0))
        self.file_name.setBaseSize(QSize(200, 20))
        self.file_name.setReadOnly(True)

        self.horizontalLayout_2.addWidget(self.file_name)

        self.browse_button = QPushButton(self.centralwidget)
        self.browse_button.setObjectName(u"browse_button")
        sizePolicy.setHeightForWidth(self.browse_button.sizePolicy().hasHeightForWidth())
        self.browse_button.setSizePolicy(sizePolicy)

        self.horizontalLayout_2.addWidget(self.browse_button)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_6)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.verticalSpacer_3 = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout_2.addItem(self.verticalSpacer_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.start_button = QPushButton(self.centralwidget)
        self.start_button.setObjectName(u"start_button")
        sizePolicy.setHeightForWidth(self.start_button.sizePolicy().hasHeightForWidth())
        self.start_button.setSizePolicy(sizePolicy)

        self.horizontalLayout_4.addWidget(self.start_button)


        self.verticalLayout_2.addLayout(self.horizontalLayout_4)

        self.loading_label = QLabel(self.centralwidget)
        self.loading_label.setObjectName(u"loading_label")
        self.loading_label.setAlignment(Qt.AlignCenter)

        self.verticalLayout_2.addWidget(self.loading_label)

        self.verticalSpacer_5 = QSpacerItem(10, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout_2.addItem(self.verticalSpacer_5)


        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setSpacing(0)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.horizontalLayout_7.setContentsMargins(-1, 0, -1, -1)
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_3)

        self.config_button = QPushButton(self.centralwidget)
        self.config_button.setObjectName(u"config_button")
        sizePolicy.setHeightForWidth(self.config_button.sizePolicy().hasHeightForWidth())
        self.config_button.setSizePolicy(sizePolicy)

        self.horizontalLayout_7.addWidget(self.config_button)

        self.config_image = QLabel(self.centralwidget)
        self.config_image.setObjectName(u"config_image")
        self.config_image.setEnabled(True)
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(2)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.config_image.sizePolicy().hasHeightForWidth())
        self.config_image.setSizePolicy(sizePolicy1)
        self.config_image.setMinimumSize(QSize(24, 24))
        self.config_image.setMaximumSize(QSize(24, 24))
        self.config_image.setPixmap(QPixmap(u"resources/images/icons8-config-50.png"))
        self.config_image.setScaledContents(True)

        self.horizontalLayout_7.addWidget(self.config_image)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_4)


        self.verticalLayout_2.addLayout(self.horizontalLayout_7)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_2)


        self.horizontalLayout_3.addLayout(self.verticalLayout_2)

        Start.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(Start)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 814, 22))
        Start.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(Start)
        self.statusbar.setObjectName(u"statusbar")
        Start.setStatusBar(self.statusbar)

        self.retranslateUi(Start)

        QMetaObject.connectSlotsByName(Start)
    # setupUi

    def retranslateUi(self, Start):
        Start.setWindowTitle(QCoreApplication.translate("Start", u"MainWindow", None))
        self.title.setText(QCoreApplication.translate("Start", u"MALDI-TOF MS AST", None))
        self.bacteria_header.setText(QCoreApplication.translate("Start", u"Bacteria", None))
        self.bacteria_select.setCurrentText("")
        self.file_name.setText(QCoreApplication.translate("Start", u"[Direcci\u00f3n Archivo]", None))
        self.browse_button.setText(QCoreApplication.translate("Start", u"Buscar", None))
        self.start_button.setText(QCoreApplication.translate("Start", u"Empezar", None))
        self.loading_label.setText("")
        self.config_button.setText(QCoreApplication.translate("Start", u"Configuraci\u00f3n", None))
        self.config_image.setText("")
    # retranslateUi

