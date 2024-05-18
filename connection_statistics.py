
class ConnectionStatistics:

    def __init__(self, currently_connected: bool, longest: float, start_time: float, avg_dur: float,
                 nb_disc: int, avg_disc_hour: float):
        self.currently_connected = currently_connected
        self.longest_duration = longest
        self.start_longest = start_time
        self.average_duration = avg_dur
        self.nb_disconnection = nb_disc
        self.average_nb_disc_hour = avg_disc_hour
