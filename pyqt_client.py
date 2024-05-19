import datetime
import sys
from typing import Optional, List, Tuple, Dict

from PySide6.QtCharts import QChart, QLineSeries, QDateTimeAxis, QValueAxis
from PySide6.QtCore import QDateTime, Qt

import utils
from bandwidth_statistics import BandwidthStatistics
from client import Client

from PySide6.QtWidgets import QApplication, QWidget

# Important:
# You need to run the following command to generate the qt_client.py file
#     pyside6-uic form.ui -o qt_client.py, or
#     pyside2-uic form.ui -o qt_client.py
from connection_statistics import ConnectionStatistics
from qt_client import Ui_QtClientWidget


# This class loads the pyqt_client into a qt window and takes care of filling it with proper data
class PyQtClient(QWidget, Client):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_QtClientWidget()
        self.ui.setupUi(self)
        self.setWindowTitle("How's the network?")
        self.start_time: Optional[int] = None
        self.end_time: Optional[int] = None
        self.chart = self.ui.view_data.chart()
        self.series: Dict[str, QLineSeries] = {}

        self.chart.setAnimationOptions(QChart.AnimationOption.AllAnimations)

        self.axis_x = QDateTimeAxis()
        self.add_date_axis()
        self.add_timeseries("Ping")
        self.add_ping_y_axis()
        self.add_timeseries("Speed")
        self.add_speed_y_axis()

        # TODO: set an icon or remove the icon from title bar

    def add_ping_y_axis(self):
        axis_y = QValueAxis()
        axis_y.setTickCount(10)
        axis_y.setLabelFormat("%.0f")
        axis_y.setTitleText("Ping (ms)")
        axis_y.setMin(0)
        self.chart.addAxis(axis_y, Qt.AlignmentFlag.AlignLeft)
        self.series["Ping"].attachAxis(axis_y)

    def add_speed_y_axis(self):
        axis_y = QValueAxis()
        axis_y.setTickCount(10)
        axis_y.setLabelFormat("%.0f")
        axis_y.setTitleText("Speed (KBits/s)")
        axis_y.setMin(0)
        self.chart.addAxis(axis_y, Qt.AlignmentFlag.AlignRight)
        self.series["Speed"].attachAxis(axis_y)

    def add_date_axis(self):
        self.axis_x.setTickCount(10)
        self.axis_x.setFormat("dd.MM (h:mm:ss)")
        self.axis_x.setTitleText("Date")
        self.chart.addAxis(self.axis_x, Qt.AlignmentFlag.AlignBottom)

    def add_timeseries(self, name):

        series = QLineSeries()
        series.setName(name)

        self.series[name] = series
        self.chart.addSeries(series)

        series.attachAxis(self.axis_x)

        self.chart.legend().hide()
        self.chart.setTitle("Connection overview")


    def update_time(self, timestamp: int):
        # if the data time is > than the start time or < than the end time, we update them
        if not self.start_time or self.start_time > timestamp:
            self.start_time = timestamp
            self.ui.label_start_time.setText(str(datetime.datetime.fromtimestamp(timestamp)))
        if not self.end_time or self.end_time < timestamp:
            self.end_time = timestamp
            self.ui.label_end_time.setText(str(datetime.datetime.fromtimestamp(timestamp)))

    def update_internet_statistics(self, stats: ConnectionStatistics):

        self.update_time(stats.current_time)

        # TODO: add colors
        if stats.currently_connected:
            self.ui.label_connection_state.setText("Connected")
        else:
            self.ui.label_connection_state.setText("Not connected")

        self.ui.label_longest_duration.setText(f"{stats.longest_duration // 60:.0f}m{stats.longest_duration % 60:.0f}s")
        self.ui.label_average_disconnection_time.setText(f"{stats.average_duration // 60:.0f}m{stats.average_duration % 60:.0f}s")
        self.ui.label_nb_disconnections.setText(str(stats.nb_disconnection))
        self.ui.label_average_nb_disconnection_hour.setText(f"{stats.average_nb_disc_hour:.2f}")

        self.ui.label_ping.setText(f"{stats.current_ping}")
        self.ui.label_lowest_ping.setText(f"{stats.min_ping}")
        self.ui.label_highest_ping.setText(f"{stats.max_ping}")
        self.ui.label_average_ping.setText(f"{stats.average_ping:.0f}")

        self.series["Ping"].append(stats.current_time, stats.current_ping)


    def update_bandwidth_statistics(self, stats: BandwidthStatistics):
        self.update_time(stats.current_time)
        self.ui.label_current_use.setText(f"{stats.current_network_use:.2f}")
        self.ui.label_current_speed.setText(f"{stats.current_network_speed:.2f}")
        self.ui.label_average_use.setText(f"{stats.average_network_use:.2f}")
        self.ui.label_total_use.setText(f"{stats.total_use:.0f}")

        self.series["Speed"].append(stats.current_time, stats.current_network_speed)

