# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ResultsWindow.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QLayout,
    QMainWindow, QMenuBar, QPushButton, QSizePolicy,
    QSpacerItem, QStatusBar, QVBoxLayout, QWidget)
import pyqtgraph as pg


class Ui_Results(object):
    def setupUi(self, Start, results):
        if not Start.objectName():
            Start.setObjectName(u"Start")
        Start.resize(600, 600)
        self.centralwidget = QWidget(Start)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout_3 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalSpacer_4 = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout_2.addItem(self.verticalSpacer_4)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalSpacer_12 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_10.addItem(self.horizontalSpacer_12)


        self.file_label = QLabel(self.centralwidget)
        self.file_label.setObjectName(u"file_label")

        self.horizontalLayout_10.addWidget(self.file_label)

        self.horizontalSpacer_13 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_10.addItem(self.horizontalSpacer_13)

        self.bacteria_label = QLabel(self.centralwidget)
        self.bacteria_label.setObjectName(u"bacteria_label")

        self.horizontalLayout_10.addWidget(self.bacteria_label)

        self.horizontalSpacer_11 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_10.addItem(self.horizontalSpacer_11)


        self.verticalLayout_2.addLayout(self.horizontalLayout_10)

        self.verticalSpacer = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")

        self.spectrometry_label = pg.PlotWidget()
        self.spectrometry_label.setBackground("#31363B")
        axis_styles = {"font-size": "14px", "text-align": "left", "font-family": "roboto", "color": "#ffffff", "font-weight": "normal"}
        self.spectrometry_label.setLabel("left", "Intensidad", **axis_styles)
        self.spectrometry_label.setLabel("bottom", "Masa (Da)", **axis_styles)

        self.spectrometry_label.setObjectName(u"spectrometry_label")
        self.horizontalLayout_9.addWidget(self.spectrometry_label)


        self.verticalLayout_2.addLayout(self.horizontalLayout_9)

        self.verticalSpacer_6 = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout_2.addItem(self.verticalSpacer_6)

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
        self.probability_title_label = QLabel(self.centralwidget)
        self.probability_title_label.setObjectName(u"probability_title_label")
        self.probability_title_label.setEnabled(True)

        self.probability_title_label.setAlignment(Qt.AlignCenter)
        self.probability_title_label.setProperty("class", "big_text")

        self.verticalLayout_4.addWidget(self.probability_title_label)


        self.horizontalLayout_8.addLayout(self.verticalLayout_4)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_2)


        self.verticalLayout_3.addLayout(self.horizontalLayout_8)


        self.horizontalLayout.addLayout(self.verticalLayout_3)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")

        self.verticalLayout_2.addLayout(self.horizontalLayout_6)

        ################
        self.results_layout = QHBoxLayout()
        self.results_layout.setObjectName(u"results_layout")
        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        
        self.results_layout.addItem(self.horizontalSpacer_5)
        
        self.addProba(results)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.results_layout.addItem(self.horizontalSpacer_6)

        self.verticalLayout_2.addLayout(self.results_layout)
        ################

        self.verticalSpacer_3 = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout_2.addItem(self.verticalSpacer_3)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_7)

        font = QFont()
        font.setPointSize(12)
        
        self.binning_label = QLabel(self.centralwidget)
        self.binning_label.setObjectName(u"binning_label")
        self.binning_label.setFont(font)

        self.horizontalLayout_5.addWidget(self.binning_label)

        horizontal_spacer = QSpacerItem(30, 30, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        self.horizontalLayout_5.addItem(horizontal_spacer)

        self.model_label = QLabel(self.centralwidget)
        self.model_label.setObjectName(u"model_label")
        self.model_label.setFont(font)

        self.horizontalLayout_5.addWidget(self.model_label)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_8)


        self.verticalLayout_2.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setSpacing(0)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.horizontalLayout_7.setContentsMargins(-1, 0, -1, -1)
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_3)

        self.export_button = QPushButton(self.centralwidget)
        self.export_button.setObjectName(u"export_button")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.export_button.sizePolicy().hasHeightForWidth())
        self.export_button.setSizePolicy(sizePolicy)

        self.horizontalLayout_7.addWidget(self.export_button)

        self.export_image = QLabel(self.centralwidget)
        self.export_image.setObjectName(u"export_image")
        self.export_image.setEnabled(True)
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(2)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.export_image.sizePolicy().hasHeightForWidth())
        self.export_image.setSizePolicy(sizePolicy1)
        self.export_image.setMinimumSize(QSize(24, 24))
        self.export_image.setMaximumSize(QSize(24, 24))
        self.export_image.setPixmap(QPixmap(u"../../AndryATA/Resources/Images/configuration.png"))
        self.export_image.setScaledContents(True)

        self.horizontalLayout_7.addWidget(self.export_image)

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

    def addProba(self, results):
        max = list(results.values())[0]
        for antibiotic in results:
            base_result_layout = QVBoxLayout()
            base_result_layout.setObjectName(u"base_result_layout_"+antibiotic)

            # Probability Label
            s_proba_label = QLabel(self.centralwidget)
            s_proba_label.setObjectName(u"label_proba_"+antibiotic)
        
            s_proba_label.setAlignment(Qt.AlignCenter)
            s_proba_label.setProperty("class", "big_text")

            if results[antibiotic] == max:
                s_proba_label.setStyleSheet("color: green;")

            s_proba_label.setText(f"{results[antibiotic]*100:.2f}%")

            base_result_layout.addWidget(s_proba_label)

            # Antibiotic Label
            s_antibiotic_label = QLabel(self.centralwidget)
            s_antibiotic_label.setObjectName(u"label_"+antibiotic)

            s_antibiotic_label.setAlignment(Qt.AlignCenter)

            s_antibiotic_label.setText(antibiotic)

            base_result_layout.addWidget(s_antibiotic_label)

            
            # Adding to layout
            self.results_layout.addLayout(base_result_layout)
            
            horizontal_spacer = QSpacerItem(30, 30, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
            self.results_layout.addItem(horizontal_spacer)

        

    def retranslateUi(self, Start):
        Start.setWindowTitle(QCoreApplication.translate("Start", u"MainWindow", None))
        self.file_label.setText(QCoreApplication.translate("Start", u"TextLabel", None))
        self.bacteria_label.setText(QCoreApplication.translate("Start", u"TextLabel", None))
        self.probability_title_label.setText(QCoreApplication.translate("Start", u"Probabilidad de susceptibilidad", None))
        self.binning_label.setText(QCoreApplication.translate("Start", u"Binning: []", None))
        self.model_label.setText(QCoreApplication.translate("Start", u"Modelo: []", None))
        self.export_button.setText(QCoreApplication.translate("Start", u"Exportar", None))
        self.export_image.setText("")
    # retranslateUi

