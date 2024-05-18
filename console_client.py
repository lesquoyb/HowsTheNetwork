from datetime import datetime

from HowsTheNetwork.client import Client
from HowsTheNetwork.connection_statistics import ConnectionStatistics


class ConsoleClient(Client):


    def update_internet_statistics(self, stats: ConnectionStatistics):
        print("")
        print(f"current state: {'connected' if stats.currently_connected else 'not connected'}")
        print(f"longest disconnection: {stats.longest_duration // 60}m{stats.longest_duration % 60:.0f}s "
              f"at time {datetime.fromtimestamp(stats.start_longest) if stats.start_longest > 0 else 0}")
        print(f"average disconnection duration: {stats.average_duration:.0f}s")
        print(f"total number of disconnection: {stats.nb_disconnection}")
        print(f"average number of disconnection per hour: {stats.average_nb_disc_hour:.2f}")