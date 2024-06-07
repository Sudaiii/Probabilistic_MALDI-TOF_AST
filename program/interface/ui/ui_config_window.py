# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ConfigWindow.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QHBoxLayout,
    QLabel, QPushButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

class Ui_Config(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(355, 255)
        self.verticalLayout_6 = QVBoxLayout(Dialog)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_6)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.binning_label = QLabel(Dialog)
        self.binning_label.setObjectName(u"binning_label")
        self.binning_label.setAlignment(Qt.AlignCenter)

        self.verticalLayout_2.addWidget(self.binning_label)

        self.binning_select = QComboBox(Dialog)
        self.binning_select.setObjectName(u"binning_select")

        self.verticalLayout_2.addWidget(self.binning_select)


        self.horizontalLayout_2.addLayout(self.verticalLayout_2)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_5)


        self.verticalLayout_4.addLayout(self.horizontalLayout_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.model_label = QLabel(Dialog)
        self.model_label.setObjectName(u"model_label")
        self.model_label.setEnabled(True)
        self.model_label.setAlignment(Qt.AlignCenter)

        self.verticalLayout_7.addWidget(self.model_label)

        self.model_select = QComboBox(Dialog)
        self.model_select.setObjectName(u"model_select")

        self.verticalLayout_7.addWidget(self.model_select)


        self.horizontalLayout.addLayout(self.verticalLayout_7)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout_4.addLayout(self.horizontalLayout)


        self.verticalLayout_5.addLayout(self.verticalLayout_4)

        self.hiperparameters_label = QLabel(Dialog)
        self.hiperparameters_label.setObjectName(u"hiperparameters_label")
        self.hiperparameters_label.setAlignment(Qt.AlignCenter)

        self.verticalLayout_5.addWidget(self.hiperparameters_label)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_5.addItem(self.verticalSpacer_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.confirm_button = QPushButton(Dialog)
        self.confirm_button.setObjectName(u"confirm_button")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.confirm_button.sizePolicy().hasHeightForWidth())
        self.confirm_button.setSizePolicy(sizePolicy)

        self.horizontalLayout_3.addWidget(self.confirm_button)


        self.verticalLayout_5.addLayout(self.horizontalLayout_3)


        self.verticalLayout_6.addLayout(self.verticalLayout_5)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Configuración", None))
        self.binning_label.setText(QCoreApplication.translate("Dialog", u"Binning", None))
        self.model_label.setText(QCoreApplication.translate("Dialog", u"Algoritmo", None))
        self.confirm_button.setText(QCoreApplication.translate("Dialog", u"Confirmar", None))

        self.binning_select.setToolTip(
"""Cuantas columnas agrupar. \n
Como los datos de espectrometría de masa MALDI-TOF tienen muchas columnas, estos pasan por un proceso donde se reduce 
el número de columnas al obtener la media de cada N columnas del espectro de masa (las cuales pasan a ser las nuevas columnas utilizadas). 
Entre mas alto el N, la espectrometría es menos detallada y los resultados empeoran, pero los modelos son más rapidos. \n
Recomendado: 5."""
        )
        self.model_select.setToolTip("Algoritmo de Machine Learning a utilizar para las predicciones. \nRecomendado: MLP.")
    
    # retranslateUi

