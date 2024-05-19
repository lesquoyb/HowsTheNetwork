
class ConnectionStatistics:

    def __init__(self, currently_connected: bool, current_ping: int, current_time: int, longest: float, start_time: float, avg_dur: float,
                 nb_disc: int, avg_disc_hour: float, min_ping: int, max_ping: int, average_ping: int):

        self.currently_connected = currently_connected
        self.current_ping = current_ping
        self.current_time = current_time
        self.longest_duration = longest
        self.start_longest = start_time
        self.average_duration = avg_dur
        self.nb_disconnection = nb_disc
        self.average_nb_disc_hour = avg_disc_hour
        self.min_ping = min_ping
        self.max_ping = max_ping
        self.average_ping = average_ping
