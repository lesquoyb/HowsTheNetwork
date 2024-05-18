from HowsTheNetwork.bandwidth_statistics import BandwidthStatistics
from HowsTheNetwork.connection_statistics import ConnectionStatistics


# This is an interface to describe how a client of the command can be called for updates
class Client:

    def update_internet_statistics(self, stats: ConnectionStatistics):
        pass

    def update_bandwidth_statistics(self, stats: BandwidthStatistics):
        pass