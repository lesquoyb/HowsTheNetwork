

class BandwidthStatistics:

    def __init__(self, current_use: float, current_time: int, current_speed: float, avg_use: float, total_duration: int, total_use: float):
        self.current_network_use = current_use
        self.current_time = current_time
        self.current_network_speed = current_speed
        self.average_network_use = avg_use
        self.total_use = total_use
        self.total_duration = total_duration

