import sys

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
        #TODO: set an icon or remove the icon from title bar

    def update_internet_statistics(self, stats: ConnectionStatistics):
        pass

    def update_bandwidth_statistics(self, stats: BandwidthStatistics):
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = PyQtClient()
    widget.show()
    sys.exit(app.exec())

