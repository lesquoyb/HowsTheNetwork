import asyncio
import sys
import threading
from typing import Optional

from PySide6.QtWidgets import QApplication

from pyqt_client import PyQtClient
from utils import init_arguments, main_loop
import qasync

if __name__ == "__main__":

    app = QApplication(sys.argv)

    widget = PyQtClient()
    args = init_arguments()
    if not args.internet_real_time and not args.file_internet \
            and not args.bandwidth_real_time and not args.file_bandwidth:
        print("You have to pick at least one of those for options: internet_real_time, file_internet, "
              "bandwidth_real_time and file_bandwidth")
        exit(-1)
        # run_command = asyncio.create_task(main_loop(widget, args, loop))
        # asyncio.run(run_command)
    widget.start_main_loop_thread(args)
    widget.show()
    sys.exit(app.exec())

