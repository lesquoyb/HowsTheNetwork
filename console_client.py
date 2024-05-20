import asyncio
from asyncio import AbstractEventLoop
from datetime import datetime
import curses
from typing import Optional

from bandwidth_statistics import BandwidthStatistics
from client import Client
from connection_statistics import ConnectionStatistics
from utils import duration_to_str, kbits_to_str


class ConsoleClient(Client):

    CONNECTION_SCREEN_HEIGHT = 8
    BANDWIDTH_SCREEN_HEIGHT = 5

    def __init__(self, connection: bool, bandwidth: bool, loop: AbstractEventLoop):

        self.current_connection_statistics: Optional[ConnectionStatistics] = None
        self.current_bandwidth_statistics: Optional[BandwidthStatistics] = None
        self.loop = loop

        if connection or bandwidth:
            self.whole_screen = curses.initscr()
            curses.noecho()
            curses.cbreak()
            self.bandwidth_start_line = 0
            if connection:
                self.bandwidth_start_line += self.CONNECTION_SCREEN_HEIGHT + 1

            self.start_user_input_thread()

    def start_user_input_thread(self):

        self.loop.create_task(self.user_input_thread())

    async def user_input_thread(self):
        # sets negative timeout so getch becomes blocking
        self.whole_screen.timeout(-1)
        self.whole_screen.nodelay(True)
        while True:
            h = self.whole_screen.getch()
            if h == ord('q'):
                self.closing()
            await asyncio.sleep(0.5)

    def write_line(self, line: int, string: str):
        self.whole_screen.addstr(line, 0, string)
        self.whole_screen.clrtoeol() # overwrite the old stuff

    def update_screen(self):
        self.whole_screen.clear()
        if self.current_connection_statistics:
            self.write_line(0, f"Current state: "
                               f"{'connected' if self.current_connection_statistics.currently_connected else 'not connected'} "
                               f"for {duration_to_str(self.current_connection_statistics.current_duration)} "
                               f"Ping: {self.current_connection_statistics.current_ping}ms")
            self.write_line(1, f"Longest disconnection: {duration_to_str(self.current_connection_statistics.longest_duration)} "
                               f"starting: {datetime.fromtimestamp(self.current_connection_statistics.start_longest) if self.current_connection_statistics.start_longest > 0 else 0}")
            self.write_line(2, f"Average disconnection duration: {duration_to_str(self.current_connection_statistics.average_duration)}")
            self.write_line(3, f"Total number of disconnection: {self.current_connection_statistics.nb_disconnection}")
            self.write_line(4, f"Average number of disconnection per hour: {self.current_connection_statistics.average_nb_disc_hour:.2f}")
            self.write_line(5, f"Lowest ping: {self.current_connection_statistics.min_ping:.0f}ms")
            self.write_line(6, f"Highest ping: {self.current_connection_statistics.max_ping:.0f}ms")
            self.write_line(7, f"Average ping: {self.current_connection_statistics.average_ping:.0f}ms")

        if self.current_bandwidth_statistics:
            self.write_line(self.bandwidth_start_line, f"Real network use since last update: {kbits_to_str(self.current_bandwidth_statistics.current_network_use)}")
            self.write_line(self.bandwidth_start_line + 1, f"Real network speed since last update: {kbits_to_str(self.current_bandwidth_statistics.current_network_speed)}/second")
            self.write_line(self.bandwidth_start_line + 2, f"Average network use: {kbits_to_str(self.current_bandwidth_statistics.average_network_use)}/second")
            self.write_line(self.bandwidth_start_line + 3, f"Total network use: {kbits_to_str(self.current_bandwidth_statistics.total_use)}")
            self.write_line(self.bandwidth_start_line + 4, f"Total monitoring duration: {duration_to_str(self.current_bandwidth_statistics.total_duration)}")

        self.whole_screen.refresh()

    def update_internet_statistics(self, stats: ConnectionStatistics):
        self.current_connection_statistics = stats
        self.update_screen()

    def update_bandwidth_statistics(self, stats: BandwidthStatistics):
        self.current_bandwidth_statistics = stats
        self.update_screen()

    def closing(self):
        curses.nocbreak()
        curses.echo()
        curses.endwin()
        # we need to stop asyncio event loop to stop the program
        self.loop.stop()
