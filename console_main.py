import asyncio
import curses

from console_client import ConsoleClient
from utils import *

if __name__ == "__main__":

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    args = init_arguments()

    if not args.internet_real_time and not args.file_internet \
            and not args.bandwidth_real_time and not args.file_bandwidth \
            and not args.read_internet_file and not args.read_bandwidth_file:
        print("You have to pick at least one of those options: internet_real_time, file_internet, "
              "bandwidth_real_time, file_bandwidth, read_internet_file, read_bandwidth_file")
        exit(-1)
    else:

        try:
            curses.wrapper(main_loop(ConsoleClient(args.internet_real_time, args.bandwidth_real_time, loop), args, loop))
        except Exception as e:
            #print(e)
            pass