# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'qt_client.ui'
##
## Created by: Qt User Interface Compiler version 6.7.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCharts import QChartView
from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QLabel,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

class Ui_QtClientWidget(object):
    def setupUi(self, QtClientWidget):
        if not QtClientWidget.objectName():
            QtClientWidget.setObjectName(u"QtClientWidget")
        QtClientWidget.resize(800, 600)
        self.verticalLayout = QVBoxLayout(QtClientWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.layout_header = QHBoxLayout()
        self.layout_header.setObjectName(u"layout_header")
        self.label_9 = QLabel(QtClientWidget)
        self.label_9.setObjectName(u"label_9")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_9.sizePolicy().hasHeightForWidth())
        self.label_9.setSizePolicy(sizePolicy)

        self.layout_header.addWidget(self.label_9)

        self.label_connection_state = QLabel(QtClientWidget)
        self.label_connection_state.setObjectName(u"label_connection_state")
        sizePolicy.setHeightForWidth(self.label_connection_state.sizePolicy().hasHeightForWidth())
        self.label_connection_state.setSizePolicy(sizePolicy)

        self.layout_header.addWidget(self.label_connection_state)

        self.label_22 = QLabel(QtClientWidget)
        self.label_22.setObjectName(u"label_22")
        sizePolicy.setHeightForWidth(self.label_22.sizePolicy().hasHeightForWidth())
        self.label_22.setSizePolicy(sizePolicy)

        self.layout_header.addWidget(self.label_22)

        self.label_duration_state = QLabel(QtClientWidget)
        self.label_duration_state.setObjectName(u"label_duration_state")

        self.layout_header.addWidget(self.label_duration_state)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.layout_header.addItem(self.horizontalSpacer)

        self.label_17 = QLabel(QtClientWidget)
        self.label_17.setObjectName(u"label_17")
        sizePolicy.setHeightForWidth(self.label_17.sizePolicy().hasHeightForWidth())
        self.label_17.setSizePolicy(sizePolicy)

        self.layout_header.addWidget(self.label_17)

        self.label_ping = QLabel(QtClientWidget)
        self.label_ping.setObjectName(u"label_ping")
        self.label_ping.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.layout_header.addWidget(self.label_ping)

        self.label_19 = QLabel(QtClientWidget)
        self.label_19.setObjectName(u"label_19")
        sizePolicy.setHeightForWidth(self.label_19.sizePolicy().hasHeightForWidth())
        self.label_19.setSizePolicy(sizePolicy)

        self.layout_header.addWidget(self.label_19)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.layout_header.addItem(self.horizontalSpacer_3)

        self.label_start_time = QLabel(QtClientWidget)
        self.label_start_time.setObjectName(u"label_start_time")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_start_time.sizePolicy().hasHeightForWidth())
        self.label_start_time.setSizePolicy(sizePolicy1)

        self.layout_header.addWidget(self.label_start_time)

        self.label_15 = QLabel(QtClientWidget)
        self.label_15.setObjectName(u"label_15")
        sizePolicy.setHeightForWidth(self.label_15.sizePolicy().hasHeightForWidth())
        self.label_15.setSizePolicy(sizePolicy)

        self.layout_header.addWidget(self.label_15)

        self.label_end_time = QLabel(QtClientWidget)
        self.label_end_time.setObjectName(u"label_end_time")

        self.layout_header.addWidget(self.label_end_time)


        self.verticalLayout.addLayout(self.layout_header)

        self.view_data = QChartView(QtClientWidget)
        self.view_data.setObjectName(u"view_data")

        self.verticalLayout.addWidget(self.view_data)

        self.layout_stats = QHBoxLayout()
        self.layout_stats.setObjectName(u"layout_stats")
        self.layout_connection_stats = QGridLayout()
        self.layout_connection_stats.setObjectName(u"layout_connection_stats")
        self.label_14 = QLabel(QtClientWidget)
        self.label_14.setObjectName(u"label_14")

        self.layout_connection_stats.addWidget(self.label_14, 3, 0, 1, 1)

        self.label_average_nb_disconnection_hour = QLabel(QtClientWidget)
        self.label_average_nb_disconnection_hour.setObjectName(u"label_average_nb_disconnection_hour")
        self.label_average_nb_disconnection_hour.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.layout_connection_stats.addWidget(self.label_average_nb_disconnection_hour, 3, 1, 1, 1)

        self.label_12 = QLabel(QtClientWidget)
        self.label_12.setObjectName(u"label_12")

        self.layout_connection_stats.addWidget(self.label_12, 2, 0, 1, 1)

        self.label_nb_disconnections = QLabel(QtClientWidget)
        self.label_nb_disconnections.setObjectName(u"label_nb_disconnections")
        self.label_nb_disconnections.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.layout_connection_stats.addWidget(self.label_nb_disconnections, 2, 1, 1, 1)

        self.label_average_disconnection_time = QLabel(QtClientWidget)
        self.label_average_disconnection_time.setObjectName(u"label_average_disconnection_time")
        self.label_average_disconnection_time.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.layout_connection_stats.addWidget(self.label_average_disconnection_time, 1, 1, 1, 1)

        self.label_10 = QLabel(QtClientWidget)
        self.label_10.setObjectName(u"label_10")

        self.layout_connection_stats.addWidget(self.label_10, 1, 0, 1, 1)

        self.label_longest_duration = QLabel(QtClientWidget)
        self.label_longest_duration.setObjectName(u"label_longest_duration")
        self.label_longest_duration.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.layout_connection_stats.addWidget(self.label_longest_duration, 0, 1, 1, 1)

        self.label_11 = QLabel(QtClientWidget)
        self.label_11.setObjectName(u"label_11")

        self.layout_connection_stats.addWidget(self.label_11, 0, 0, 1, 1)


        self.layout_stats.addLayout(self.layout_connection_stats)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.layout_stats.addItem(self.horizontalSpacer_2)

        self.layout_bandwidth_stats = QGridLayout()
        self.layout_bandwidth_stats.setObjectName(u"layout_bandwidth_stats")
        self.label_5 = QLabel(QtClientWidget)
        self.label_5.setObjectName(u"label_5")

        self.layout_bandwidth_stats.addWidget(self.label_5, 2, 0, 1, 1)

        self.label_3 = QLabel(QtClientWidget)
        self.label_3.setObjectName(u"label_3")

        self.layout_bandwidth_stats.addWidget(self.label_3, 0, 0, 1, 1)

        self.label_2 = QLabel(QtClientWidget)
        self.label_2.setObjectName(u"label_2")

        self.layout_bandwidth_stats.addWidget(self.label_2, 1, 0, 1, 1)

        self.label_6 = QLabel(QtClientWidget)
        self.label_6.setObjectName(u"label_6")

        self.layout_bandwidth_stats.addWidget(self.label_6, 3, 0, 1, 1)

        self.label_average_use = QLabel(QtClientWidget)
        self.label_average_use.setObjectName(u"label_average_use")
        self.label_average_use.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.layout_bandwidth_stats.addWidget(self.label_average_use, 2, 1, 1, 1)

        self.label_total_use = QLabel(QtClientWidget)
        self.label_total_use.setObjectName(u"label_total_use")
        self.label_total_use.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.layout_bandwidth_stats.addWidget(self.label_total_use, 3, 1, 1, 1)

        self.label_current_use = QLabel(QtClientWidget)
        self.label_current_use.setObjectName(u"label_current_use")
        self.label_current_use.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.layout_bandwidth_stats.addWidget(self.label_current_use, 0, 1, 1, 1)

        self.label_current_speed = QLabel(QtClientWidget)
        self.label_current_speed.setObjectName(u"label_current_speed")
        self.label_current_speed.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.layout_bandwidth_stats.addWidget(self.label_current_speed, 1, 1, 1, 1)


        self.layout_stats.addLayout(self.layout_bandwidth_stats)


        self.verticalLayout.addLayout(self.layout_stats)

        self.layout_ping = QHBoxLayout()
        self.layout_ping.setObjectName(u"layout_ping")
        self.label_8 = QLabel(QtClientWidget)
        self.label_8.setObjectName(u"label_8")
        sizePolicy.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy)

        self.layout_ping.addWidget(self.label_8)

        self.label_lowest_ping = QLabel(QtClientWidget)
        self.label_lowest_ping.setObjectName(u"label_lowest_ping")
        sizePolicy1.setHeightForWidth(self.label_lowest_ping.sizePolicy().hasHeightForWidth())
        self.label_lowest_ping.setSizePolicy(sizePolicy1)
        self.label_lowest_ping.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.layout_ping.addWidget(self.label_lowest_ping)

        self.label_18 = QLabel(QtClientWidget)
        self.label_18.setObjectName(u"label_18")
        sizePolicy.setHeightForWidth(self.label_18.sizePolicy().hasHeightForWidth())
        self.label_18.setSizePolicy(sizePolicy)

        self.layout_ping.addWidget(self.label_18)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.layout_ping.addItem(self.horizontalSpacer_4)

        self.label_13 = QLabel(QtClientWidget)
        self.label_13.setObjectName(u"label_13")
        sizePolicy.setHeightForWidth(self.label_13.sizePolicy().hasHeightForWidth())
        self.label_13.setSizePolicy(sizePolicy)

        self.layout_ping.addWidget(self.label_13)

        self.label_highest_ping = QLabel(QtClientWidget)
        self.label_highest_ping.setObjectName(u"label_highest_ping")
        sizePolicy1.setHeightForWidth(self.label_highest_ping.sizePolicy().hasHeightForWidth())
        self.label_highest_ping.setSizePolicy(sizePolicy1)
        self.label_highest_ping.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.layout_ping.addWidget(self.label_highest_ping)

        self.label_20 = QLabel(QtClientWidget)
        self.label_20.setObjectName(u"label_20")
        sizePolicy.setHeightForWidth(self.label_20.sizePolicy().hasHeightForWidth())
        self.label_20.setSizePolicy(sizePolicy)

        self.layout_ping.addWidget(self.label_20)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.layout_ping.addItem(self.horizontalSpacer_5)

        self.label_16 = QLabel(QtClientWidget)
        self.label_16.setObjectName(u"label_16")
        sizePolicy.setHeightForWidth(self.label_16.sizePolicy().hasHeightForWidth())
        self.label_16.setSizePolicy(sizePolicy)

        self.layout_ping.addWidget(self.label_16)

        self.label_average_ping = QLabel(QtClientWidget)
        self.label_average_ping.setObjectName(u"label_average_ping")
        sizePolicy1.setHeightForWidth(self.label_average_ping.sizePolicy().hasHeightForWidth())
        self.label_average_ping.setSizePolicy(sizePolicy1)
        self.label_average_ping.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.layout_ping.addWidget(self.label_average_ping)

        self.label_21 = QLabel(QtClientWidget)
        self.label_21.setObjectName(u"label_21")
        sizePolicy.setHeightForWidth(self.label_21.sizePolicy().hasHeightForWidth())
        self.label_21.setSizePolicy(sizePolicy)

        self.layout_ping.addWidget(self.label_21)


        self.verticalLayout.addLayout(self.layout_ping)


        self.retranslateUi(QtClientWidget)

        QMetaObject.connectSlotsByName(QtClientWidget)
    # setupUi

    def retranslateUi(self, QtClientWidget):
        QtClientWidget.setWindowTitle(QCoreApplication.translate("QtClientWidget", u"Widget", None))
        self.label_9.setText(QCoreApplication.translate("QtClientWidget", u"Currently:", None))
        self.label_connection_state.setText(QCoreApplication.translate("QtClientWidget", u"not connected", None))
        self.label_22.setText(QCoreApplication.translate("QtClientWidget", u"for", None))
        self.label_duration_state.setText(QCoreApplication.translate("QtClientWidget", u"...", None))
        self.label_17.setText(QCoreApplication.translate("QtClientWidget", u"Ping:", None))
        self.label_ping.setText(QCoreApplication.translate("QtClientWidget", u"...", None))
        self.label_19.setText(QCoreApplication.translate("QtClientWidget", u"ms", None))
        self.label_start_time.setText(QCoreApplication.translate("QtClientWidget", u"2024-05-19 14:12:00", None))
        self.label_15.setText(QCoreApplication.translate("QtClientWidget", u"-", None))
        self.label_end_time.setText(QCoreApplication.translate("QtClientWidget", u"2024-05-19 14:12:00", None))
        self.label_14.setText(QCoreApplication.translate("QtClientWidget", u"Average number of disconnection per hour", None))
        self.label_average_nb_disconnection_hour.setText(QCoreApplication.translate("QtClientWidget", u"...", None))
        self.label_12.setText(QCoreApplication.translate("QtClientWidget", u"Total number of disconnections", None))
        self.label_nb_disconnections.setText(QCoreApplication.translate("QtClientWidget", u"...", None))
        self.label_average_disconnection_time.setText(QCoreApplication.translate("QtClientWidget", u"...", None))
        self.label_10.setText(QCoreApplication.translate("QtClientWidget", u"Average disconnection duration", None))
        self.label_longest_duration.setText(QCoreApplication.translate("QtClientWidget", u"...", None))
        self.label_11.setText(QCoreApplication.translate("QtClientWidget", u"Longest duration offline", None))
        self.label_5.setText(QCoreApplication.translate("QtClientWidget", u"Average network use", None))
        self.label_3.setText(QCoreApplication.translate("QtClientWidget", u"Real network use since last update", None))
        self.label_2.setText(QCoreApplication.translate("QtClientWidget", u"Real network speed since last update", None))
        self.label_6.setText(QCoreApplication.translate("QtClientWidget", u"Total network use", None))
        self.label_average_use.setText(QCoreApplication.translate("QtClientWidget", u"...", None))
        self.label_total_use.setText(QCoreApplication.translate("QtClientWidget", u"...", None))
        self.label_current_use.setText(QCoreApplication.translate("QtClientWidget", u"...", None))
        self.label_current_speed.setText(QCoreApplication.translate("QtClientWidget", u"...", None))
        self.label_8.setText(QCoreApplication.translate("QtClientWidget", u"Lowest ping", None))
        self.label_lowest_ping.setText(QCoreApplication.translate("QtClientWidget", u"...", None))
        self.label_18.setText(QCoreApplication.translate("QtClientWidget", u"ms", None))
        self.label_13.setText(QCoreApplication.translate("QtClientWidget", u"Highest ping", None))
        self.label_highest_ping.setText(QCoreApplication.translate("QtClientWidget", u"...", None))
        self.label_20.setText(QCoreApplication.translate("QtClientWidget", u"ms", None))
        self.label_16.setText(QCoreApplication.translate("QtClientWidget", u"Average ping", None))
        self.label_average_ping.setText(QCoreApplication.translate("QtClientWidget", u"..", None))
        self.label_21.setText(QCoreApplication.translate("QtClientWidget", u"ms", None))
    # retranslateUi

