import asyncio
import socket
import time
from asyncio import AbstractEventLoop
from typing import List, Tuple

import psutil
import argparse
from datetime import datetime

# my network is so bad that I have to take some of my time to write software to demonstrate it to my internet provider
# based on: https://stackoverflow.com/questions/3764291/how-can-i-see-if-theres-an-available-and-active-network-connection-in-python
# and: https://stackoverflow.com/questions/15616378/python-network-bandwidth-monitor


# global variables for real time display
from bandwidth_statistics import BandwidthStatistics
from client import Client
from connection_statistics import ConnectionStatistics

internet: List[Tuple[int, bool]] = []
bandwidth: List[Tuple[int, float]] = []


def is_internet_working(host: str = "8.8.8.8", port: int = 53, timeout: int = 3) -> float:
    """
    Tries to connect to the host with the given port and timeout, and if successful returns the
    time it took to connect in seconds, otherwise returns -1.0

    :param host: the host to connect to
    :param port: the port at which we try to connect
    :param timeout: the timeout duration in seconds
    :return: The time it took to connect if the connection is successful, -1.0 otherwise
    """
    try:
        socket.setdefaulttimeout(timeout)
        start = time.perf_counter()
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return time.perf_counter() - start
    except socket.error as ex:
        return -1.0


def get_next_disconnected_period(internet_connection_history: List[Tuple[int, int]], start_index: int) \
        -> Tuple[int, int]:
    """
    Starts reading the connection history at the given index and returns a pair of indices representing the
    start and end of the next disconnection period.
    In case no disconnection was found, the function returns (-1,-1)

    :param internet_connection_history: the connection history, each pair represents a timestamp and an integer
        representing the time it took to establish the connection (positive value = connected,
        negative = disconnected). The list must be ordered.
    :param start_index: The index at which the search for the next disconnection period must start
    :return: a tuple where the first element is the index of the start of the next disconnection period in the history
        and the second element of the tuple is the index of the end of the next disconnection period in the history.
        In case no disconnection was found, the function returns (-1,-1)
    """
    start = -1
    end = -1
    for i, (_, ping) in enumerate(internet_connection_history[start_index:]):
        if ping < 0:
            start = start_index + i
            end = start + 1
            while end < len(internet_connection_history) and internet_connection_history[end][1] < 0:
                end += 1
            break
    return start, end


def get_disconnection_stats(internet_connection_history: List[Tuple[int, int]],
                            expected_duration_between_checks: int) -> Tuple[int, int, int, float, int, float, int, int, int]:
    """
    Iterates over a history of pings and returns basic statistics about the disconnections

    :param internet_connection_history: ordered list of pairs, the first item is a timestamp in second, the second an
            integer that represents the time it took to establish a connection, in case it was not possible to connect
            its value is negative
    :param expected_duration_between_checks: the time expected between two checks, used to estimate the end of
        a disconnection period in some cases
    :return: A tuple composed in that order of: the duration in seconds of the current state the
        program is in, the duration in seconds of the longest disconnection, the starting time
        in seconds of that disconnection, the average disconnection duration, the total number of disconnection, the
        average number of disconnection per hour, the minimum ping value, the maximum ping value and the average ping
        value
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
            duration = internet_connection_history[end-1][0] - internet_connection_history[start][0]
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

    # we need a separate iteration for ping processing

    max_ping = -1
    min_ping = -1
    average_ping = 0
    nb_pings = 0
    latest_duration: float = 0
    # we set the initial value at the opposite of the first, so it starts by "resetting"
    connected: bool = internet_connection_history[0][1] < 0
    previous = 0
    for time, ping in internet_connection_history:

        # this first part is for calculating the duration of the latest state (could be in a separate smaller loop)
        # if the state changed we reset
        if connected and ping < 0 or not connected and ping > 0:
            latest_duration = 0
            connected = ping > 0
        else:
            latest_duration += time - previous

        if ping > 0:
            max_ping = max(max_ping, ping)
            min_ping = min(min_ping, ping) if nb_pings > 0 else ping
            average_ping += ping
            nb_pings += 1

        previous = time

    if nb_pings:
        average_ping /= nb_pings

    return int(latest_duration), longest_time, start_time_longest_disconnection, average_time, nb_disconnection, \
           average_disconnection_per_hour, min_ping, max_ping, average_ping


async def check_internet_loop(client: Client, host: str, port: int, timeout: int, save_real_time: bool,
                              internet_check_delay: int, saving_file_path: str,
                              saving_as_datetime: bool):
    global internet
    if saving_file_path:
        internet_file = open(saving_file_path, "a")

    while True:
        ping = int(is_internet_working(host, port, timeout) * 1000) # we express ping in ms
        now = int(time.time())
        if save_real_time:
            internet += [(now, ping)]
            stats = ConnectionStatistics(ping >= 0, ping, now, *get_disconnection_stats(internet, internet_check_delay))
            client.update_internet_statistics(stats)

        if saving_file_path:
            internet_file.write(f"{datetime.fromtimestamp(now) if saving_as_datetime else now},{ping}\n")
            internet_file.flush()

        await asyncio.sleep(internet_check_delay)


def bytes_to_kbits(value: int) -> float:
    """
    Converts a number of bytes into its value in Kbit

    :param value: a number of bytes
    :return: the conversion in Kilo bit
    """
    return value / 1024. * 8


def get_bandwidth_stats(bandwidth_history: List[Tuple[int, float]],
                        expected_duration_between_checks: int) -> BandwidthStatistics:
    # bandwidth always has a size of 2 or more so no index checking necessary
    first = bandwidth_history[0]
    last = bandwidth_history[-1]
    total = last[1]
    if len(bandwidth_history) > 1:
        current_use = last[1] - bandwidth_history[-2][1]
        current_speed = current_use / (last[0] - bandwidth_history[-2][0])
        avg = total / (last[0] - first[0])
    else:
        current_use = last[1]
        current_speed = current_use / expected_duration_between_checks
        avg = current_speed
    duration = last[0] - first[0]
    return BandwidthStatistics(current_use, last[0], current_speed, avg, duration, total)


def get_total_kbits_use_since_boot():
    return bytes_to_kbits(psutil.net_io_counters().bytes_sent + psutil.net_io_counters().bytes_recv)


async def check_bandwidth_usage(client: Client, bandwidth_refresh_rate: int, save_real_time: bool,
                                saving_bandwidth_file: str, saving_as_datetime: bool, initial_bandwidth_use: int):
    global bandwidth

    if saving_bandwidth_file:
        bandwidth_file = open(saving_bandwidth_file, "a")

    while True:

        new_value = get_total_kbits_use_since_boot() - initial_bandwidth_use
        new_time = int(time.time())
        if save_real_time:
            bandwidth += [(new_time, new_value)]

        if saving_bandwidth_file:
            bandwidth_file.write(f"{datetime.fromtimestamp(new_time) if saving_as_datetime else new_time},"
                                 f"{round(new_value)}\n")
            bandwidth_file.flush()
        if save_real_time:
            stats = get_bandwidth_stats(bandwidth, bandwidth_refresh_rate)
            client.update_bandwidth_statistics(stats)

        await asyncio.sleep(bandwidth_refresh_rate)


def kbits_to_str(kbits: float) -> str:
    if kbits < 1024:
        return f"{kbits:.2f}Kbits"
    mbits = kbits / 1024
    if mbits < 1024:
        return f"{mbits:.2f}Mbits"
    gbits = mbits/1024
    if gbits < 1024:
        return f"{gbits:.2f}Gbits"
    return f"{gbits/1024:.2f}Tbits"


def ping_to_str(ping: float) -> str:
    if ping > 0:
        return f"{ping:.0f}ms"
    else:
        return "timeout"

def duration_to_str(duration: float) -> str:
    if duration < 60:
        return f"{duration:.0f}s"
    elif duration < 3600:
        return f"{duration//60:02.0f}m{duration % 60:02.0f}"
    else:
        return f"{duration//3600}h{(duration % 3600) //60:02.0f}m{duration % 60:02.0f}s"


def read_internet_file(client: Client, read_internet_file: str, save_real_time: bool, delay_internet: int):
    global internet

    pings = internet if save_real_time else []

    f = open(read_internet_file, "r")
    for timestamp, ping in [[int(i) for i in line.split(",")] for line in f.readlines()]:
        pings += [(timestamp, ping)]
        stats = ConnectionStatistics(ping >= 0, ping, timestamp, *get_disconnection_stats(pings, delay_internet))
        # TODO: it shouldn't be the default delay, we could update an average through the reading to get an approximate
        client.update_internet_statistics(stats)

    if save_real_time:
        pings.sort()# just to make sure we don't mess with incoming data
    f.close()


def read_bandwidth_file(client: Client, read_bandwidth_file: str, save_real_time: bool, delay_bandwidth: int):
    global bandwidth

    usage = bandwidth if save_real_time else []

    f = open(read_bandwidth_file, "r")
    for timestamp, use in [[int(i) for i in line.split(",")] for line in f.readlines()]:
        usage += [(timestamp, use)]
        stats = get_bandwidth_stats(usage, delay_bandwidth)
        # TODO: it shouldn't be the default delay, we could update an average by reading the file to get an approximate
        client.update_bandwidth_statistics(stats)

    if save_real_time:
        usage.sort() # just to make sure we don't mess with incoming data
    f.close()

def main_loop(client: Client, args: argparse.Namespace, loop: AbstractEventLoop):
    """
    Uses the command parameters passed to the function to initialise the two main loops: checking for
    connection and checking bandwidth usage. Once everything is initialised this loop will run forever.

    :param client:
        the object that will be responsible for showing to the user the current state of the network
    :param args:
        the arguments passed to the program
    """
    asyncio.set_event_loop(loop)
    if args.read_internet_file:
        read_internet_file(client, args.read_internet_file, args.internet_real_time, args.delay_internet)
    if args.read_bandwidth_file:
        read_bandwidth_file(client, args.read_bandwidth_file, args.bandwidth_real_time, args.delay_bandwidth)
    if args.internet_real_time or args.file_internet:
        loop.create_task(check_internet_loop(client, args.host, args.port, args.timeout, args.internet_real_time,
                                             args.delay_internet, args.file_internet, args.datetime))
    if args.bandwidth_real_time or args.file_bandwidth:
        initial_bandwidth_use = get_total_kbits_use_since_boot()
        loop.create_task(check_bandwidth_usage(client, args.delay_bandwidth, args.bandwidth_real_time,
                                               args.file_bandwidth, args.datetime, initial_bandwidth_use))
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

    # file reading
    parser.add_argument("-rif", "--read-internet-file", type=str, required=False, help="Use this option to read a "
                                                                                       "previously saved internet file.")
    parser.add_argument("-rbf", "--read-bandwidth-file", type=str, required=False, help="Use this option to read a "
                                                                                        "previously saved bandwidth file.")

    return parser.parse_args()

