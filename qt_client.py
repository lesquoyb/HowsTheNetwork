# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'qt_client.ui'
##
## Created by: Qt User Interface Compiler version 6.7.0
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
from PySide6.QtWidgets import (QApplication, QGraphicsView, QGridLayout, QHBoxLayout,
    QLabel, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_QtClientWidget(object):
    def setupUi(self, QtClientWidget):
        if not QtClientWidget.objectName():
            QtClientWidget.setObjectName(u"QtClientWidget")
        QtClientWidget.resize(800, 600)
        self.verticalLayout = QVBoxLayout(QtClientWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_9 = QLabel(QtClientWidget)
        self.label_9.setObjectName(u"label_9")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_9.sizePolicy().hasHeightForWidth())
        self.label_9.setSizePolicy(sizePolicy)

        self.horizontalLayout_2.addWidget(self.label_9)

        self.label_connection_state = QLabel(QtClientWidget)
        self.label_connection_state.setObjectName(u"label_connection_state")
        sizePolicy.setHeightForWidth(self.label_connection_state.sizePolicy().hasHeightForWidth())
        self.label_connection_state.setSizePolicy(sizePolicy)

        self.horizontalLayout_2.addWidget(self.label_connection_state)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.label_start_time = QLabel(QtClientWidget)
        self.label_start_time.setObjectName(u"label_start_time")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_start_time.sizePolicy().hasHeightForWidth())
        self.label_start_time.setSizePolicy(sizePolicy1)

        self.horizontalLayout_2.addWidget(self.label_start_time)

        self.label_15 = QLabel(QtClientWidget)
        self.label_15.setObjectName(u"label_15")
        sizePolicy.setHeightForWidth(self.label_15.sizePolicy().hasHeightForWidth())
        self.label_15.setSizePolicy(sizePolicy)

        self.horizontalLayout_2.addWidget(self.label_15)

        self.label_end_time = QLabel(QtClientWidget)
        self.label_end_time.setObjectName(u"label_end_time")

        self.horizontalLayout_2.addWidget(self.label_end_time)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.view_data = QGraphicsView(QtClientWidget)
        self.view_data.setObjectName(u"view_data")

        self.verticalLayout.addWidget(self.view_data)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.layout_connection_stats = QGridLayout()
        self.layout_connection_stats.setObjectName(u"layout_connection_stats")
        self.label_average_nb_disconnection_hour = QLabel(QtClientWidget)
        self.label_average_nb_disconnection_hour.setObjectName(u"label_average_nb_disconnection_hour")

        self.layout_connection_stats.addWidget(self.label_average_nb_disconnection_hour, 3, 1, 1, 1)

        self.label_10 = QLabel(QtClientWidget)
        self.label_10.setObjectName(u"label_10")

        self.layout_connection_stats.addWidget(self.label_10, 1, 0, 1, 1)

        self.label_average_disconnection_time = QLabel(QtClientWidget)
        self.label_average_disconnection_time.setObjectName(u"label_average_disconnection_time")

        self.layout_connection_stats.addWidget(self.label_average_disconnection_time, 1, 1, 1, 1)

        self.label_11 = QLabel(QtClientWidget)
        self.label_11.setObjectName(u"label_11")

        self.layout_connection_stats.addWidget(self.label_11, 0, 0, 1, 1)

        self.label_12 = QLabel(QtClientWidget)
        self.label_12.setObjectName(u"label_12")

        self.layout_connection_stats.addWidget(self.label_12, 2, 0, 1, 1)

        self.label_14 = QLabel(QtClientWidget)
        self.label_14.setObjectName(u"label_14")

        self.layout_connection_stats.addWidget(self.label_14, 3, 0, 1, 1)

        self.label_longest_duration = QLabel(QtClientWidget)
        self.label_longest_duration.setObjectName(u"label_longest_duration")

        self.layout_connection_stats.addWidget(self.label_longest_duration, 0, 1, 1, 1)

        self.label_nb_disconnections = QLabel(QtClientWidget)
        self.label_nb_disconnections.setObjectName(u"label_nb_disconnections")

        self.layout_connection_stats.addWidget(self.label_nb_disconnections, 2, 1, 1, 1)

        self.label_17 = QLabel(QtClientWidget)
        self.label_17.setObjectName(u"label_17")

        self.layout_connection_stats.addWidget(self.label_17, 4, 0, 1, 1)

        self.label_ping = QLabel(QtClientWidget)
        self.label_ping.setObjectName(u"label_ping")

        self.layout_connection_stats.addWidget(self.label_ping, 4, 1, 1, 1)


        self.horizontalLayout.addLayout(self.layout_connection_stats)

        self.layout_bandwidth_stats = QGridLayout()
        self.layout_bandwidth_stats.setObjectName(u"layout_bandwidth_stats")
        self.label_average_use = QLabel(QtClientWidget)
        self.label_average_use.setObjectName(u"label_average_use")

        self.layout_bandwidth_stats.addWidget(self.label_average_use, 2, 1, 1, 1)

        self.label_current_speed = QLabel(QtClientWidget)
        self.label_current_speed.setObjectName(u"label_current_speed")

        self.layout_bandwidth_stats.addWidget(self.label_current_speed, 1, 1, 1, 1)

        self.label_2 = QLabel(QtClientWidget)
        self.label_2.setObjectName(u"label_2")

        self.layout_bandwidth_stats.addWidget(self.label_2, 1, 0, 1, 1)

        self.label_3 = QLabel(QtClientWidget)
        self.label_3.setObjectName(u"label_3")

        self.layout_bandwidth_stats.addWidget(self.label_3, 0, 0, 1, 1)

        self.label_total_use = QLabel(QtClientWidget)
        self.label_total_use.setObjectName(u"label_total_use")

        self.layout_bandwidth_stats.addWidget(self.label_total_use, 3, 1, 1, 1)

        self.label_5 = QLabel(QtClientWidget)
        self.label_5.setObjectName(u"label_5")

        self.layout_bandwidth_stats.addWidget(self.label_5, 2, 0, 1, 1)

        self.label_current_use = QLabel(QtClientWidget)
        self.label_current_use.setObjectName(u"label_current_use")

        self.layout_bandwidth_stats.addWidget(self.label_current_use, 0, 1, 1, 1)

        self.label_6 = QLabel(QtClientWidget)
        self.label_6.setObjectName(u"label_6")

        self.layout_bandwidth_stats.addWidget(self.label_6, 3, 0, 1, 1)


        self.horizontalLayout.addLayout(self.layout_bandwidth_stats)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.layout_stats = QHBoxLayout()
        self.layout_stats.setObjectName(u"layout_stats")

        self.verticalLayout.addLayout(self.layout_stats)


        self.retranslateUi(QtClientWidget)

        QMetaObject.connectSlotsByName(QtClientWidget)
    # setupUi

    def retranslateUi(self, QtClientWidget):
        QtClientWidget.setWindowTitle(QCoreApplication.translate("QtClientWidget", u"Widget", None))
        self.label_9.setText(QCoreApplication.translate("QtClientWidget", u"Currently:", None))
        self.label_connection_state.setText(QCoreApplication.translate("QtClientWidget", u"not connected", None))
        self.label_start_time.setText(QCoreApplication.translate("QtClientWidget", u"2024-05-19 14:12:00", None))
        self.label_15.setText(QCoreApplication.translate("QtClientWidget", u"-", None))
        self.label_end_time.setText(QCoreApplication.translate("QtClientWidget", u"2024-05-19 14:12:00", None))
        self.label_average_nb_disconnection_hour.setText(QCoreApplication.translate("QtClientWidget", u"TextLabel", None))
        self.label_10.setText(QCoreApplication.translate("QtClientWidget", u"Average disconnection duration", None))
        self.label_average_disconnection_time.setText(QCoreApplication.translate("QtClientWidget", u"TextLabel", None))
        self.label_11.setText(QCoreApplication.translate("QtClientWidget", u"Longest duration offline", None))
        self.label_12.setText(QCoreApplication.translate("QtClientWidget", u"Total number of disconnections", None))
        self.label_14.setText(QCoreApplication.translate("QtClientWidget", u"Average number of disconnection per hour", None))
        self.label_longest_duration.setText(QCoreApplication.translate("QtClientWidget", u"TextLabel", None))
        self.label_nb_disconnections.setText(QCoreApplication.translate("QtClientWidget", u"TextLabel", None))
        self.label_17.setText(QCoreApplication.translate("QtClientWidget", u"Ping", None))
        self.label_ping.setText(QCoreApplication.translate("QtClientWidget", u"TextLabel", None))
        self.label_average_use.setText(QCoreApplication.translate("QtClientWidget", u"TextLabel", None))
        self.label_current_speed.setText(QCoreApplication.translate("QtClientWidget", u"TextLabel", None))
        self.label_2.setText(QCoreApplication.translate("QtClientWidget", u"Real network speed since last update", None))
        self.label_3.setText(QCoreApplication.translate("QtClientWidget", u"Real network use since last update", None))
        self.label_total_use.setText(QCoreApplication.translate("QtClientWidget", u"TextLabel", None))
        self.label_5.setText(QCoreApplication.translate("QtClientWidget", u"Average network use since the beginning", None))
        self.label_current_use.setText(QCoreApplication.translate("QtClientWidget", u"TextLabel", None))
        self.label_6.setText(QCoreApplication.translate("QtClientWidget", u"Total network use", None))
    # retranslateUi

