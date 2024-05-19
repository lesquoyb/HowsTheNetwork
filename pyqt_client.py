import datetime
import sys
from typing import Optional

from PySide6.QtCharts import QChart, QLineSeries
from PySide6.QtCore import QDateTime

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
from utils import init_arguments, main_loop


class PyQtClient(QWidget, Client):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_QtClientWidget()
        self.ui.setupUi(self)
        self.setWindowTitle("How's the network?")
        self.start_time: Optional[int] = None
        self.end_time: Optional[int] = None
        self.chart = QChart()

        self.chart.setAnimationOptions(QChart.AnimationOption.AllAnimations)

        #self.add_series("Magnitude (Column 1)", [0, 1])
        # TODO: set an icon or remove the icon from title bar

    def add_series(self, name, columns):

        # Create QLineSeries

        self.series = QLineSeries()

        self.series.setName(name)

        # Filling QLineSeries
        for i in range(self.model.rowCount()):

            # Getting the data
            t = self.model.index(i, 0).data()

            date_fmt = "yyyy-MM-dd HH:mm:ss.zzz"

            x = QDateTime().fromString(t, date_fmt).toSecsSinceEpoch()

            y = float(self.model.index(i, 1).data())

            if x > 0 and y > 0:
                self.series.append(x, y)

        self.chart.addSeries(self.series)

        # Setting X-axis

        self.axis_x = QDateTimeAxis()

        self.axis_x.setTickCount(10)

        self.axis_x.setFormat("dd.MM (h:mm)")

        self.axis_x.setTitleText("Date")

        self.chart.addAxis(self.axis_x, Qt.AlignBottom)

        self.series.attachAxis(self.axis_x)

        # Setting Y-axis

        self.axis_y = QValueAxis()

        self.axis_y.setTickCount(10)

        self.axis_y.setLabelFormat("%.2f")

        self.axis_y.setTitleText("Magnitude")

        self.chart.addAxis(self.axis_y, Qt.AlignLeft)

        self.series.attachAxis(self.axis_y)

        # Getting the color from the QChart to use it on the QTableView

        color_name = self.series.pen().color().name()

        self.model.color = f"{color_name}"

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

        self.ui.label_longest_duration.setText(f"{stats.longest_duration // 60}m{stats.longest_duration % 60:.0f}")
        self.ui.label_average_disconnection_time.setText(f"{stats.average_duration // 60}m{stats.average_duration % 60:.0f}")
        self.ui.label_nb_disconnections.setText(str(stats.nb_disconnection))
        self.ui.label_average_nb_disconnection_hour.setText(f"{stats.average_nb_disc_hour:.2f}")

        self.ui.label_ping.setText(f"{stats.current_ping}")
        self.ui.label_lowest_ping.setText(f"{stats.min_ping}")
        self.ui.label_highest_ping.setText(f"{stats.max_ping}")
        self.ui.label_average_ping.setText(f"{stats.average_ping:.0f}")

    def update_bandwidth_statistics(self, stats: BandwidthStatistics):
        self.update_time(stats.current_time)
        self.ui.label_current_use.setText(f"{stats.current_network_use:.2f}")
        self.ui.label_current_speed.setText(f"{stats.current_network_speed:.2f}")
        self.ui.label_average_use.setText(f"{stats.average_network_use:.2f}")
        self.ui.label_total_use.setText(f"{stats.total_use:.0f}")


