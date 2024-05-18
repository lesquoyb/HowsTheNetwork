import asyncio
import socket
import time
from typing import List, Tuple

import psutil
import argparse
from datetime import datetime

# my network is so bad that I have to take some of my time to write software to demonstrate it to my internet provider
# based on: https://stackoverflow.com/questions/3764291/how-can-i-see-if-theres-an-available-and-active-network-connection-in-python
# and: https://stackoverflow.com/questions/15616378/python-network-bandwidth-monitor


# global variables for real time display
from HowsTheNetwork.bandwidth_statistics import BandwidthStatistics
from HowsTheNetwork.client import Client
from HowsTheNetwork.connection_statistics import ConnectionStatistics
from HowsTheNetwork.console_client import ConsoleClient

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
    for i, (_, state) in enumerate(internet_connection_history[start_index:]):
        if not state:
            start = start_index + i
            end = start + 1
            while end < len(internet_connection_history) and not internet_connection_history[end][1]:
                end += 1
            break
    return start, end


def get_disconnection_stats(internet_connection_history: List[Tuple[int, bool]],
                            expected_duration_between_checks: int) -> Tuple[int, int, float, int, float]:
    """
    Iterates over a history of connection/disconnection and returns basic statistics about the disconnections

    :param internet_connection_history: ordered list of pairs, the first item is a timestamp in second, the second a
        boolean that is True when the connection is established and False when disconnected
    :param expected_duration_between_checks: the time expected between two checks, used to estimate the end of
        a disconnection period in some cases
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
            # TODO: it can lead to wrong values, but it should stay a reasonable mistake in most cases
            duration = internet_connection_history[end - 1][0] - internet_connection_history[start][
                0] + expected_duration_between_checks
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


async def check_internet_loop(client: Client, host: str, port: int, timeout: int, save_real_time: bool,
                              internet_check_delay: int = 10, saving_file_path: str = None,
                              saving_as_datetime: bool = False):
    global internet
    if saving_file_path:
        internet_file = open(saving_file_path, "w")

    while True:
        connected = is_internet_working(host, port, timeout)
        now = int(time.time())
        if save_real_time:
            internet += [(now, connected)]
            stats = ConnectionStatistics(connected, *get_disconnection_stats(internet, internet_check_delay))
            client.update_internet_statistics(stats)

        if saving_file_path:
            internet_file.write(f"{datetime.fromtimestamp(now) if saving_as_datetime else now},{connected}\n")
            internet_file.flush()

        await asyncio.sleep(internet_check_delay)


def bytes_to_kbits(value: int) -> float:
    """
    Converts a number of bytes into its value in Kbit

    :param value: a number of bytes
    :return: the conversion in Kilo bit
    """
    return value / 1024. / 1024. * 8


def get_bandwidth_stats(bandwidth_history: List[Tuple[int, float]],
                        expected_duration_between_checks: int) -> BandwidthStatistics:
    # bandwidth always has a size of 2 or more so no index checking necessary
    first = bandwidth_history[0]
    last = bandwidth_history[-1]
    total = bytes_to_kbits(last[1])
    current_use = bytes_to_kbits(last[1] - bandwidth_history[-2][1])
    current_speed = current_use / (last[0] - bandwidth_history[-2][0])
    avg = total / (last[0] - first[0])
    duration = bandwidth_history[-1][0] - bandwidth_history[0][0]
    return BandwidthStatistics(current_use, current_speed, avg, duration, total)


async def check_bandwidth_usage(client: Client, bandwidth_refresh_rate: int = 30, save_real_time: bool = True,
                                saving_bandwidth_file: str = "bandwidth.csv", saving_as_datetime: bool = True):
    global bandwidth
    old_value = 0
    old_time = 0

    if saving_bandwidth_file:
        bandwidth_file = open(saving_bandwidth_file, "w")

    while True:

        new_value = psutil.net_io_counters().bytes_sent + psutil.net_io_counters().bytes_recv
        new_time = int(time.time())
        if save_real_time:
            bandwidth += [(new_time, new_value)]

        if old_value:
            use_per_second = (new_value - old_value) / (new_time - old_time)
            if saving_bandwidth_file:
                bandwidth_file.write(f"{datetime.fromtimestamp(new_time) if saving_as_datetime else new_time},"
                                     f"{round(bytes_to_kbits(use_per_second))}\n")
                bandwidth_file.flush()
            if save_real_time:
                stats = get_bandwidth_stats(bandwidth, bandwidth_refresh_rate)
                client.update_bandwidth_statistics(stats)

        old_value = new_value
        old_time = new_time

        await asyncio.sleep(bandwidth_refresh_rate)



def main_loop(client: Client, args: argparse.Namespace):
    """
    Uses the command parameters passed to the function to initialise the two main loops: checking for
    connection and checking bandwidth usage. Once everything is initialised this loop will run forever.

    :param client:
        the object that will be responsible for showing to the user the current state of the network
    :param args:
        the arguments passed to the program
    """
    loop = asyncio.get_event_loop()
    if args.internet_real_time or args.file_internet:
        loop.create_task(check_internet_loop(client, args.host, args.port, args.timeout, args.internet_real_time,
                                             args.delay_internet, args.file_internet, args.datetime))
    if args.bandwidth_real_time or args.file_bandwidth:
        loop.create_task(check_bandwidth_usage(client, args.delay_bandwidth, args.bandwidth_real_time,
                                               args.file_bandwidth, args.datetime))
    loop.run_forever()


def init_arguments() -> argparse.Namespace:
    """
    Initialise the argument parser to treat the parameters passed to the program.
    Checks that there's no incoherence.
    :return: the arguments in the form of an argparse Namespace
    """
    parser = argparse.ArgumentParser()

    # parameters for internet checking
    parser.add_argument("--host", default="8.8.8.8", help="The host to connect to when checking the internet "
                                                          "connection.")
    parser.add_argument("-p", "--port", default=53, type=float,
                        help="The port of the host to connect to when checking the internet connection")
    parser.add_argument("-t", "--timeout", default=3, type=float, help="The time in seconds to timeout when checking "
                                                                       "the internet connection")
    parser.add_argument("-di", "--delay-internet", default=10, type=float,
                        help="The preferred time in between two checks of the internet connection. This time won't "
                             "necessarily be met, it depends on your computer load level")
    parser.add_argument("-irt", "--internet-real-time", action="store_true", help="Use this option to get real time "
                                                                                  "overview of your network "
                                                                                  "connections and disconnections "
                                                                                  "to the internet")
    parser.add_argument("-fi", "--file-internet", type=str, required=False, help="Use this option to save the internet "
                                                                                 "connection data into a file")

    # Parameters for bandwidth checks
    parser.add_argument("-db", "--delay-bandwidth", default=30, type=float,
                        help="The preferred time in between two checks of the real bandwidth consumption. This time "
                             "won't necessarily be met, it depends on your computer load level")
    parser.add_argument("-brt", "--bandwidth-real-time", action="store_true", help="Use this option to get real time "
                                                                                   "overview of your network bandwidth "
                                                                                   "usage.")
    parser.add_argument("-fb", "--file-bandwidth", type=str, required=False, help="Use this option to save the "
                                                                                  "bandwidth use data into a file.")

    # general options
    parser.add_argument("--datetime", action="store_true", help="Use to save the time in files in the format "
                                                                "of a datetime instead of the default timestamp.")

    return parser.parse_args()


