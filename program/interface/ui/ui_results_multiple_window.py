# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ResultsMultipleWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.6.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt, QSignalMapper, Slot)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QLayout,
    QMainWindow, QMenuBar, QPushButton, QSizePolicy,
    QSpacerItem, QStatusBar, QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem)



class Ui_Results_Multi(object):
    def setupUi(self, ResultsMulti, results):
        if not ResultsMulti.objectName():
            ResultsMulti.setObjectName(u"Results")
        ResultsMulti.resize(1200, 700)

        self.centralwidget = QWidget(ResultsMulti)
        self.centralwidget.setObjectName(u"centralwidget")

        self.horizontalLayout_2 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)

        self.bacteria_label = QLabel(ResultsMulti)
        self.bacteria_label.setObjectName(u"bacteria_label")
        self.bacteria_label.setProperty("class", "bold_text")

        self.horizontalLayout_3.addWidget(self.bacteria_label)

        self.bacteria_name_label = QLabel(ResultsMulti)
        self.bacteria_name_label.setObjectName(u"bacteria_name_label")

        self.horizontalLayout_3.addWidget(self.bacteria_name_label)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.results_table = QTableWidget(ResultsMulti)
        if (self.results_table.columnCount() < 1):
            self.results_table.setColumnCount(1)
        __qtablewidgetitem = QTableWidgetItem()
        self.results_table.setHorizontalHeaderItem(0, __qtablewidgetitem)
        self.__setup_table(results)
        self.results_table.setObjectName(u"results_table")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.results_table.sizePolicy().hasHeightForWidth())
        self.results_table.setSizePolicy(sizePolicy)
        self.results_table.setMinimumSize(QSize(500, 0))
        self.results_table.setSizeIncrement(QSize(100, 0))
        self.results_table.setBaseSize(QSize(100, 0))

        self.verticalLayout.addWidget(self.results_table)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(-1, 0, -1, -1)
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_3)

        self.report_button = QPushButton(ResultsMulti)
        self.report_button.setObjectName(u"report_button")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.report_button.sizePolicy().hasHeightForWidth())
        self.report_button.setSizePolicy(sizePolicy1)

        self.horizontalLayout_5.addWidget(self.report_button)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_5)


        self.verticalLayout.addLayout(self.horizontalLayout_5)


        self.horizontalLayout.addLayout(self.verticalLayout)


        self.horizontalLayout_2.addLayout(self.horizontalLayout)

        ResultsMulti.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(ResultsMulti)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 814, 22))
        ResultsMulti.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(ResultsMulti)
        self.statusbar.setObjectName(u"statusbar")
        ResultsMulti.setStatusBar(self.statusbar)
        self.retranslateUi(ResultsMulti)

        QMetaObject.connectSlotsByName(ResultsMulti)
    # setupUi

    def __setup_table(self, results):
        # Set size
        self.results_table.setRowCount(len(results))
        self.results_table.setColumnCount(len(results[0])+2) 

        # Create columns
        i = 1
        for antibiotic in results[0]:
            __qtablewidgetitem = QTableWidgetItem()
            self.results_table.setHorizontalHeaderItem(i, __qtablewidgetitem)
            __qtablewidgetitem.setText(QCoreApplication.translate("Results", antibiotic, None))
            i += 1
        self.results_table.resizeColumnsToContents()

        __qtablewidgetitem = QTableWidgetItem()
        self.results_table.setHorizontalHeaderItem(i, __qtablewidgetitem)
        __qtablewidgetitem.setText(QCoreApplication.translate("Results", "Visualizar", None))

        # Resize columns to name
        for col in range(i):
            self.results_table.setColumnWidth(col, self.results_table.columnWidth(col)+10)

        self.results_table.setColumnWidth(0, 300)
        self.results_table.setColumnWidth(i, 130)

    def retranslateUi(self, Results):
        Results.setWindowTitle(QCoreApplication.translate("Results", u"Dialog", None))
        self.bacteria_label.setText(QCoreApplication.translate("Results", u"Bacteria:", None))
        self.bacteria_name_label.setText(QCoreApplication.translate("Results", u"name", None))
        ___qtablewidgetitem = self.results_table.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Results", u"File", None));
        self.report_button.setText(QCoreApplication.translate("Results", u"Exportar", None))

