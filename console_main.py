import curses

from console_client import ConsoleClient
from utils import *

if __name__ == "__main__":

    args = init_arguments()

    if not args.internet_real_time and not args.file_internet \
            and not args.bandwidth_real_time and not args.file_bandwidth:
        print("You have to pick at least one of those for options: internet_real_time, file_internet, "
              "bandwidth_real_time and file_bandwidth")
    else:
        curses.wrapper(main_loop(ConsoleClient(args.internet_real_time, args.bandwidth_real_time), args))
