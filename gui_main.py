import asyncio
import sys
import threading

from PySide6.QtWidgets import QApplication

from pyqt_client import PyQtClient
from utils import init_arguments, main_loop


if __name__ == "__main__":

    app = QApplication(sys.argv)
    widget = PyQtClient()

    args = init_arguments()
    thread: threading.Thread = None
    if not args.internet_real_time and not args.file_internet \
            and not args.bandwidth_real_time and not args.file_bandwidth:
        print("You have to pick at least one of those for options: internet_real_time, file_internet, "
              "bandwidth_real_time and file_bandwidth")
        exit(-1)
    else:
        thread = threading.Thread(target=main_loop, args=(widget, args))
        thread.start()

    widget.show()
    sys.exit(app.exec())

