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
    # loop = qasync.QEventLoop(app)
    # asyncio.set_event_loop(loop)
    loop = asyncio.new_event_loop()

    widget = PyQtClient()
    asyncio.set_event_loop(loop)
    args = init_arguments()
    thread: Optional[threading.Thread] = None
    if not args.internet_real_time and not args.file_internet \
            and not args.bandwidth_real_time and not args.file_bandwidth:
        print("You have to pick at least one of those for options: internet_real_time, file_internet, "
              "bandwidth_real_time and file_bandwidth")
        exit(-1)
    else:
        pass
        thread = threading.Thread(target=main_loop, args=(widget, args, loop))
        thread.start()
        # run_command = asyncio.create_task(main_loop(widget, args, loop))
        # asyncio.run(run_command)

    widget.show()
    loop.stop()
    sys.exit(app.exec())

