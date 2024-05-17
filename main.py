import asyncio
import socket
import time
from typing import Dict, List, Tuple

import psutil
import argparse
import sched

# my network is so bad that I have to take some of my time to write software to demonstrate it to my internet provider
# based on: https://stackoverflow.com/questions/3764291/how-can-i-see-if-theres-an-available-and-active-network-connection-in-python
# and: https://stackoverflow.com/questions/15616378/python-network-bandwidth-monitor


# global variables for real time display
internet: List[Tuple[int, bool]] = []
bandwidth: List[Tuple[int, float]] = []


def is_internet_working(host: str = "8.8.8.8", port: int = 53, timeout: int = 3) -> bool:
    """
    Tries to connect to the host with the given port and timeout, and if successful returns True

    :param host: the host to connect to
    :param port: the port at which we try to connect
    :param timeout: the timeout duration in seconds
    :return: True if the connection is successful, False otherwise
    """
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error as ex:
        return False


async def check_internet(host: str, port: int, timeout: int, save_real_time: bool, internet_check_delay: int = 10,
                         saving_file_path: str = None):
    global internet
    if saving_file_path:
        internet_file = open(saving_file_path, "w")

    while True:
        connected = is_internet_working()
        now = int(time.time())
        if save_real_time:
            internet += [(now, connected)]
            longest, start_time, avg_dur, nb_disc, avg_disc_hour = get_disconnection_stats(internet)
            print("")
            print(f"longest disconnection: {longest/60} at time {start_time}")
            print(f"average disconnection duration: {avg_dur}")
            print(f"total number of disconnection: {nb_disc}")
            print(f"average number of disconnection per hour: {avg_disc_hour}")

        if saving_file_path:
            internet_file.write(f"{now},{connected}\n")
            internet_file.flush()

        await asyncio.sleep(internet_check_delay)


def convert_to_kbit(value: int) -> float:
    """
    Converts a number of bytes into its value in Kbit

    :param value: a number of bytes
    :return: the conversion in Kilo bit
    """
    return value / 1024. / 1024. * 8


async def check_bandwidth_usage(bandwidth_refresh_rate: int = 30, save_real_time: bool = True,
                                save_in_file: bool = True, saving_bandwidth_file: str = "bandwidth.csv"):
    global bandwidth
    old_value = 0
    old_time = 0

    if save_in_file:
        bandwidth_file = open(saving_bandwidth_file, "w")

    while True:

        new_value = psutil.net_io_counters().bytes_sent + psutil.net_io_counters().bytes_recv
        new_time = time.time()
        if old_value:
            use_per_second = (new_value - old_value) / (new_time - old_time)
            if save_in_file:
                bandwidth_file.write(f"{new_time},{round(convert_to_kbit(use_per_second))}\n")
                bandwidth_file.flush()
            if save_real_time:
                bandwidth += (new_time, new_value)

        old_value = new_value
        old_time = new_time

        await asyncio.sleep(bandwidth_refresh_rate)


def get_next_disconnected_period(internet_connection_history: List[Tuple[int, bool]], start_index: int) \
        -> Tuple[int, int]:
    """
    Starts reading the connection history at the given index and returns a pair of indices representing the
    start and end of the next disconnection period.
    In case no disconnection was found, the function returns (-1,-1)

    :param internet_connection_history: the connection history, each pair represents a timestamp and a boolean
        representing the state of the connection (True = connected, False = disconnected). The list must be ordered.
    :param start_index: The index at which the search for the next disconnection period must start
    :return: a tuple where the first element is the index of the start of the next disconnection period in the history
        and the second element of the tuple is the index of the end of the next disconnection period in the history.
        In case no disconnection was found, the function returns (-1,-1)
    """
    start = -1
    end = -1
    for i, (_, state)  in enumerate(internet_connection_history[start_index:]):
        if not state:
            start = start_index + i
            end = start + 1
            while end < len(internet_connection_history) and not internet_connection_history[end][1]:
                end += 1
            break
    return start, end


def get_disconnection_stats(internet_connection_history: List[Tuple[int, bool]]) -> Tuple[int, int, float, int, float]:
    """
    Iterates over a history of connection/disconnection and returns basic statistics about the disconnections

    :param internet_connexion_history: ordered list of pairs, the first item is a timestamp in second, the second a
        boolean that is True when the connection is established and False when disconnected
    :return: A tuple composed in that order of: the duration in seconds of the longest disconnection, the starting time
        in seconds of that disconnection, the average disconnection duration, the total number of disconnection, and the
        average number of disconnection per hour
    """
    longest_time: int = 0
    start_time_longest_disconnection: int = 0
    average_time: float = 0
    nb_disconnection: int = 0
    average_disconnection_per_hour: float = 0

    start, end = get_next_disconnected_period(internet_connection_history, 0)
    while start != -1:
        nb_disconnection += 1
        
        if end < len(internet_connection_history):
            duration = internet_connection_history[end][0] - internet_connection_history[start][0]
        else:
            duration = internet_connection_history[end-1][0] - internet_connection_history[start][0] 
            #TODO: this is wrong but ok for now
        average_time += duration
        if duration > longest_time:
            longest_time = duration
            start_time_longest_disconnection = internet_connection_history[start][0]

        start, end = get_next_disconnected_period(internet_connection_history, end)

    # now we can finish to calculate the average disconnection time by dividing it by the number of disconnections
    if nb_disconnection > 0:
        average_time /= nb_disconnection

    # we calculate the average number of disconnection per hour ( nb of disconnections / nb of hours)
    total_history_duration: float = internet_connection_history[-1][0] - internet_connection_history[0][0]
    # we transform the total duration from seconds to hours
    total_history_duration /= 3600
    if total_history_duration > 0:
        average_disconnection_per_hour = nb_disconnection / total_history_duration

    return longest_time, start_time_longest_disconnection, average_time, nb_disconnection, average_disconnection_per_hour


async def main(args: argparse.Namespace):
    loop = asyncio.get_event_loop()
    if args.internet:
        loop.create_task(check_internet(args.host, args.port, args.timeout, args.internet_real_time, args.delay_internet, args.file_internet))
    if args.bandwidth:
        loop.create_task(check_bandwidth_usage())
    while True:
        await asyncio.sleep(args.main_loop_rate)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--main-loop-rate", default=10, help="The speed at which the main loop runs in seconds,"
                                                             "increase it to let your cpu breath")
    parser.add_argument("-b", "--bandwidth", action="store_true", help="Use this to monitor actual bandwidth usage of "
                                                                       "this computer. Beware, this is just the real "
                                                                       "bandwidth use, not the bandwidth 'potential'")
    # parameters for internet checking
    parser.add_argument("-i", "--internet", action="store_true", help="Use it to monitor if this computer has access"
                                                                      "to internet or not.")
    parser.add_argument("--host", default="8.8.8.8", help="The host to connect to when checking the internet "
                                                                "connection")
    parser.add_argument("-p", "--port", default=53, help="The port of the host to connect to when checking the internet"
                                                         " connection")
    parser.add_argument("-t", "--timeout", default=3, help="The time in seconds to timeout when checking the internet "
                                                           "connection")
    parser.add_argument("-di", "--delay-internet", default=10, help="The preferred time in between two checks of "
                                                                    "the internet connection. This time won't "
                                                                    "necessarily be met, it depends on your computer "
                                                                    "load level")
    parser.add_argument("-irt", "--internet-real-time", action="store_true", help="Use this option to get real time "
                                                                                  "overview of your network "
                                                                                  "connections and disconnections "
                                                                                  "to the internet")
    parser.add_argument("-fi", "--file-internet", type=str, required=False, help="Use this option to save the internet "
                                                                                 "connection data into a file")

    # bandwidth
    # TODO
    # bandwidth_refresh_rate: int = 30, save_real_time: bool = True,
    # save_in_file: bool = True, saving_bandwidth_file: str = "bandwidth.csv"

    args = parser.parse_args()
    if not args.internet and not args.bandwidth:
        print("You have to pick at least one of those two options: internet and bandwidth")
    else:
        asyncio.run(main(args))
