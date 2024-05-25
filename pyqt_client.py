import datetime
from typing import Optional, Dict

from PySide2.QtCharts import *
from PySide2.QtCore import QDateTime, Qt
from PySide2.QtGui import QColor, QPalette

from bandwidth_statistics import BandwidthStatistics
from client import Client

from PySide2.QtWidgets import QWidget

# Important:
# You need to run the following command to generate the qt_client.py file
#     pyside6-uic form.ui -o qt_client.py, or
#     pyside2-uic form.ui -o qt_client.py
from connection_statistics import ConnectionStatistics
from qt_client import Ui_QtClientWidget


# This class loads the pyqt_client into a qt window and takes care of filling it with proper data
from utils import duration_to_str, kbits_to_str, check_internet_loop, check_bandwidth_usage, ping_to_str


class PyQtClient(QWidget, Client):

    PING_COLOR = QColor(0, 0, 0)
    SPEED_COLOR = QColor(0, 255, 0)
    CONNECTED_COLOR = QColor(0, 255, 0)
    NOT_CONNECTED_COLOR = QColor(255, 0, 0)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_QtClientWidget()
        self.ui.setupUi(self)
        self.setWindowTitle("How's the network?")
        self.start_time: Optional[int] = None
        self.end_time: Optional[int] = None
        self.chart = self.ui.view_data.chart()
        self.series: Dict[str, QtCharts.QLineSeries] = {}

        #self.chart.setAnimationOptions(QtCharts.AnimationOption.NoAnimation)

        self.axis_x = QtCharts.QDateTimeAxis()
        self.add_date_axis()
        self.add_timeseries("Ping")
        self.add_ping_y_axis()
        self.add_timeseries("Speed")
        self.add_speed_y_axis()
        self.min_speed = -1
        self.min_ping = -1
        # TODO: set an icon or remove the icon from title bar


    def add_ping_y_axis(self):
        self.ping_axis_y = QtCharts.QValueAxis()
        self.ping_axis_y.setTickCount(10)
        self.ping_axis_y.setLabelFormat("%.0f")
        self.ping_axis_y.setTitleText("Ping (ms)")
        self.ping_axis_y.setTitleBrush(self.PING_COLOR)
        self.ping_axis_y.setTitleBrush(self.PING_COLOR)
        self.chart.addAxis(self.ping_axis_y, Qt.AlignmentFlag.AlignLeft)
        self.series["Ping"].attachAxis(self.ping_axis_y)
        self.series["Ping"].setColor(self.PING_COLOR)

    def add_speed_y_axis(self):
        self.speed_axis_y = QtCharts.QValueAxis() #TODO: removing it temporarely because it doesn't work QLogValueAxis()
        self.speed_axis_y.setLabelFormat("%.0f")
        self.ping_axis_y.setTickCount(10)
        self.speed_axis_y.setTitleText("Speed (Kbits/s)")
        self.speed_axis_y.setTitleBrush(self.SPEED_COLOR)
        #TODO: uncomment when log axis is fixed self.speed_axis_y.setBase(10)
        self.speed_axis_y.setGridLineColor(self.SPEED_COLOR)
        self.chart.addAxis(self.speed_axis_y, Qt.AlignmentFlag.AlignRight)
        self.series["Speed"].attachAxis(self.speed_axis_y)
        self.series["Speed"].setColor(self.SPEED_COLOR)

    def add_date_axis(self):
        self.axis_x.setTickCount(7)
        self.axis_x.setFormat("dd-MM h:mm:ss")
        self.chart.addAxis(self.axis_x, Qt.AlignmentFlag.AlignBottom)

    def add_timeseries(self, name):

        series = QtCharts.QLineSeries()
        series.setName(name)

        self.series[name] = series
        self.chart.addSeries(series)

        series.attachAxis(self.axis_x)

        self.chart.legend().hide()

    def update_time(self, timestamp: int):
        # if the data time is > than the start time or < than the end time, we update them
        if not self.start_time or self.start_time > timestamp:
            self.start_time = timestamp
            self.ui.label_start_time.setText(str(datetime.datetime.fromtimestamp(timestamp)))
            self.axis_x.setMin(QDateTime.fromSecsSinceEpoch(timestamp))
        if not self.end_time or self.end_time < timestamp:
            self.end_time = timestamp
            self.ui.label_end_time.setText(str(datetime.datetime.fromtimestamp(timestamp)))
            self.axis_x.setMax(QDateTime.fromSecsSinceEpoch(timestamp))


    def update_internet_statistics(self, stats: ConnectionStatistics):

        self.update_time(stats.current_time)

        connected_palette = QPalette()
        if stats.currently_connected:
            self.ui.label_connection_state.setText("Connected")
            connected_palette.setColor(self.ui.label_connection_state.foregroundRole(), self.CONNECTED_COLOR)
        else:
            self.ui.label_connection_state.setText("Not connected")
            connected_palette.setColor(self.ui.label_connection_state.foregroundRole(), self.NOT_CONNECTED_COLOR)
        self.ui.label_connection_state.setPalette(connected_palette)

        self.ui.label_longest_duration.setText(f"{duration_to_str(stats.longest_duration)}")
        self.ui.label_duration_state.setText(f"{duration_to_str(stats.current_duration)}")
        self.ui.label_average_disconnection_time.setText(f"{duration_to_str(stats.average_duration)}")
        self.ui.label_nb_disconnections.setText(str(stats.nb_disconnection))
        self.ui.label_average_nb_disconnection_hour.setText(f"{stats.average_nb_disc_hour:.2f}")

        self.ui.label_ping.setText(f"{ping_to_str(stats.current_ping)}")
        self.ui.label_lowest_ping.setText(f"{ping_to_str(stats.min_ping)}")
        self.ui.label_highest_ping.setText(f"{ping_to_str(stats.max_ping)}")
        self.ui.label_average_ping.setText(f"{ping_to_str(stats.average_ping)}")

        self.series["Ping"].append(stats.current_time, stats.current_ping if stats.current_ping > 0 else 0)
        if self.min_ping < 0:
            self.min_ping = max(0, stats.current_ping)
        self.min_ping = min(self.min_ping, max(0, stats.current_ping))
        self.ping_axis_y.setMin(self.min_ping)
        self.ping_axis_y.setMax(max(self.ping_axis_y.max(), stats.current_ping))
        self.chart.removeSeries(self.series["Ping"])
        self.chart.addSeries(self.series["Ping"])

    def update_bandwidth_statistics(self, stats: BandwidthStatistics):
        self.update_time(stats.current_time)
        self.ui.label_current_use.setText(f"{kbits_to_str(stats.current_network_use)}")
        self.ui.label_current_speed.setText(f"{kbits_to_str(stats.current_network_speed)}/second")
        self.ui.label_average_use.setText(f"{kbits_to_str(stats.average_network_use)}/second")
        self.ui.label_total_use.setText(f"{kbits_to_str(stats.total_use)}")
        self.series["Speed"].append(stats.current_time, stats.current_network_speed)
        if self.min_speed < 0:
            self.min_speed = max(0.0, stats.current_network_speed)
        self.min_speed = min(self.min_speed, stats.current_network_speed)
        self.speed_axis_y.setMin(self.min_speed)
        self.speed_axis_y.setMax(max(self.speed_axis_y.max(), stats.current_network_speed))
        self.chart.removeSeries(self.series["Speed"])
        self.chart.addSeries(self.series["Speed"])
