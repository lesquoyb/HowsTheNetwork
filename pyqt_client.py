import datetime
from typing import Optional, List, Tuple, Dict

from PySide6.QtCharts import QChart, QLineSeries, QDateTimeAxis, QValueAxis
from PySide6.QtCore import QDateTime, Qt
from PySide6.QtGui import QColor

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
from utils import duration_to_str, kbits_to_str, check_internet_loop, check_bandwidth_usage


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

        self.chart.setAnimationOptions(QChart.AnimationOption.NoAnimation)

        self.axis_x = QDateTimeAxis()
        self.add_date_axis()
        self.add_timeseries("Ping")
        self.add_ping_y_axis()
        self.add_timeseries("Speed")
        self.add_speed_y_axis()
        # TODO: set an icon or remove the icon from title bar

    # def run_internet_loop(self, args):
    #     loop = asyncio.new_event_loop()
    #     asyncio.set_event_loop(loop)
    #
    #     loop.run_until_complete(check_internet_loop(self, args.host, args.port, args.timeout, args.internet_real_time,
    #                                                     args.delay_internet, args.file_internet, args.datetime))
    #     loop.close()

    #
    # def run_bandwidth_loop(self, args):
    #     loop = asyncio.new_event_loop()
    #     asyncio.set_event_loop(loop)
    #
    #     loop.run_until_complete(check_bandwidth_usage(self, args.delay_bandwidth, args.bandwidth_real_time,
    #                                                args.file_bandwidth, args.datetime))
    #     loop.close()

    #
    # def start_main_loop_thread(self, args):
    #
    #     if args.internet_real_time or args.file_internet:
    #         self.thread_internet = threading.Thread(target=self.run_internet_loop, args=(args,))
    #         self.thread_internet.start()
    #
    #     if args.bandwidth_real_time or args.file_bandwidth:
    #         self.thread_bandwidth = threading.Thread(target=self.run_bandwidth_loop, args=(args, ))
    #         self.thread_bandwidth.start()

    def add_ping_y_axis(self):
        self.ping_axis_y = QValueAxis()
        self.ping_axis_y.setTickCount(10)
        self.ping_axis_y.setLabelFormat("%.0f")
        self.ping_axis_y.setTitleText("Ping (ms)")
        self.ping_axis_y.setTitleBrush(QColor(255,0,0))
        self.ping_axis_y.setMin(0)
        self.chart.addAxis(self.ping_axis_y, Qt.AlignmentFlag.AlignLeft)
        self.series["Ping"].attachAxis(self.ping_axis_y)
        self.series["Ping"].setColor(QColor(255,0,0))

    def add_speed_y_axis(self):
        self.speed_axis_y = QValueAxis()
        self.speed_axis_y.setTickCount(10)
        self.speed_axis_y.setLabelFormat("%.0f")
        self.speed_axis_y.setTitleText("Speed (KBits/s)")
        self.speed_axis_y.setTitleBrush(QColor(0,255,0))
        self.speed_axis_y.setMin(0)
        self.chart.addAxis(self.speed_axis_y, Qt.AlignmentFlag.AlignRight)
        self.series["Speed"].attachAxis(self.speed_axis_y)
        self.series["Speed"].setColor(QColor(0,255,0))

    def add_date_axis(self):
        self.axis_x.setTickCount(7)
        self.axis_x.setFormat("dd-MM h:mm:ss")
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
            self.axis_x.setMin(QDateTime.fromSecsSinceEpoch(timestamp))
        if not self.end_time or self.end_time < timestamp:
            self.end_time = timestamp
            self.ui.label_end_time.setText(str(datetime.datetime.fromtimestamp(timestamp)))
            self.axis_x.setMax(QDateTime.fromSecsSinceEpoch(timestamp))

    def update_internet_statistics(self, stats: ConnectionStatistics):

        self.update_time(stats.current_time)

        # TODO: add colors
        if stats.currently_connected:
            self.ui.label_connection_state.setText("Connected")
        else:
            self.ui.label_connection_state.setText("Not connected")

        self.ui.label_longest_duration.setText(f"{duration_to_str(stats.longest_duration)}")
        self.ui.label_duration_state.setText(f"{duration_to_str(stats.current_duration)}")
        self.ui.label_average_disconnection_time.setText(f"{duration_to_str(stats.average_duration)}")
        self.ui.label_nb_disconnections.setText(str(stats.nb_disconnection))
        self.ui.label_average_nb_disconnection_hour.setText(f"{stats.average_nb_disc_hour:.2f}")

        self.ui.label_ping.setText(f"{stats.current_ping}")
        self.ui.label_lowest_ping.setText(f"{stats.min_ping}")
        self.ui.label_highest_ping.setText(f"{stats.max_ping}")
        self.ui.label_average_ping.setText(f"{stats.average_ping:.0f}")

        self.series["Ping"].append(stats.current_time, stats.current_ping)
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
        self.speed_axis_y.setMax(max(self.ping_axis_y.max(), stats.current_network_speed))
        self.chart.removeSeries(self.series["Speed"])
        self.chart.addSeries(self.series["Speed"])

