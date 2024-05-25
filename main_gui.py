import asyncio
import sys
import threading
from typing import Optional

from PySide2.QtWidgets import QApplication

from pyqt_client import PyQtClient
from utils import init_arguments, main_loop

if __name__ == "__main__":

    app = QApplication(sys.argv)

    widget = PyQtClient()

    args = init_arguments()
    thread: Optional[threading.Thread] = None
    if not args.internet_real_time and not args.internet_file \
            and not args.bandwidth_real_time and not args.bandwidth_file \
            and not args.read_internet_file and not args.read_bandwidth_file:
        print("You have to pick at least one of those options: internet_real_time, file_internet, "
              "bandwidth_real_time, file_bandwidth, read_internet_file, read_bandwidth_file")
        exit(-1)
    else:
        thread = threading.Thread(target=main_loop, args=(widget, args, asyncio.get_event_loop()))
        thread.start()

    widget.show()
    ret = app.exec_()

    asyncio.get_event_loop().stop()
    sys.exit(ret)

