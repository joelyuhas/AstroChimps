"""
Author: Joel Yuhas
Date: November 30th, 2021

Helper functions

Miscellaneous helper functions that can be used by multiple algorithms

NOTE: May but into a helper/buildingblocks class later on, but for now the methods are simple enough this works.


"""

import datetime
import time
import pause
import socket
from pathlib import Path

# The hard coded computer name and directories. Can update later to use env variables but works for now
COMPUTER_DIRECTORY_DICT = {
    'DESKTOP-XXXXXXX': "D:\Joel\Git\AstroChimps",
    'DESKTOP-XXXXXXX': "D:\Git\AstroChimps"
}

# Get the current hostname of the machine
hostname = socket.gethostname()

# Check if the hostname exists as a key in the dictionary
if hostname in COMPUTER_DIRECTORY_DICT:
    # Get the value associated with the hostname key
    ASTRO_HOME_PATH = Path(COMPUTER_DIRECTORY_DICT[hostname])
    print("Found hostname: " + hostname + "and directory: " + str(ASTRO_HOME_PATH))

else:
    ASTRO_HOME_PATH = Path.home() / 'AstroChimps'


# Basic dataclass for helping distinguish colors for printing to console
class Colors:
    PURPLE = '\033[95m'
    GREEN = '\033[92m'
    ORANGE = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    RED = '\033[91m'


# Trade hour constants
TRADE_END_HOUR = 16
TRADE_END_MIN = 1
TRADE_HHMM_END = (TRADE_END_HOUR * 100) + TRADE_END_MIN

TRADE_START_HOUR = 9
TRADE_START_MIN = 30
TRADE_HHMM_START = (TRADE_START_HOUR * 100) + TRADE_START_MIN

TRADE_END_BUFFER_MIN = 30
TRADE_OPENING_BUFFER_HIBERNATION_MIN = 30


# Interval wait time constant
DEFAULT_ALGORITHM_CYCLE_TIME_SECONDS = 60

DATABASE_PATH = ASTRO_HOME_PATH / 'databases' / 'developing_databases'
OBSERVER_DATABASE_PATH = ASTRO_HOME_PATH / 'databases' / 'observer_databases'
LOGBASE_PATH = ASTRO_HOME_PATH / 'logs' / 'maintenance_logs'
ACCOUNT_LOG_PATH = ASTRO_HOME_PATH / 'logs' / 'account_logs'
PROGRAM_PATH = ASTRO_HOME_PATH / 'programs'
OBSERVER_PATH = PROGRAM_PATH / 'background'
BIN_PATH = ASTRO_HOME_PATH / 'bin'
REPORTING_PATH = ASTRO_HOME_PATH / 'reporting'
EMAIL_REPORTING_PATH = REPORTING_PATH / 'email_reporting'


def evaluator_helper(evaluator: bool):
    """
    Helper function to assist with formatting. If passed true, will print green PASS, if false, reports red FAIL.

    :param evaluator: (bool): True reports green PASS, False reports red FAIL

    """
    if evaluator:
        print(Colors.GREEN + f" -- PASS -- ")
    else:
        print(Colors.RED + f" -- FAIL -- ")


def is_trade_hours() -> bool:
    """
    Function used to check if the time is currently in trade hours.

    :return: (bool): True if in trade hours, False if not

    """
    t = datetime.datetime.now().strftime("%H%M")
    # Set true and then fail if condition found to be outside trading hours
    trade_status = True

    # Check for trading days (saturday or sunday then false)
    if datetime.datetime.today().weekday() > 4:
        trade_status = False

    # Check for trading hours (before 930 or after 4 then false)
    if int(t) < TRADE_HHMM_START or int(t) >= TRADE_HHMM_END:
        trade_status = False

    return trade_status


def time_until_trade_hours_start() -> datetime:
    """
    Returns the datetime of when the next open trade hour will be.

    :return: (datetime): Datetime of when next trade opening starts (not including holidays atm)

    """
    t = datetime.datetime.now().strftime("%H%M")
    t = int(t)
    current_time = datetime.datetime.today()

    # Check if trade day (Mon - Fri) and before 9:30, then just wait until trade open later that day
    if datetime.datetime.today().weekday() < 5:
        if t < TRADE_HHMM_START:
            return datetime.datetime(current_time.year, current_time.month, current_time.day, TRADE_START_HOUR,
                                     TRADE_START_MIN)

    # If after 9:30, check which day
    # if Friday, add a 3 days until Monday
    if datetime.datetime.today().weekday() == 4:
        current_time += datetime.timedelta(days=3)
        return datetime.datetime(current_time.year, current_time.month, current_time.day, TRADE_START_HOUR,
                                 TRADE_START_MIN)

    # if Saturday, add a 2 days until Monday
    elif datetime.datetime.today().weekday() == 5:
        current_time += datetime.timedelta(days=2)
        return datetime.datetime(current_time.year, current_time.month, current_time.day, TRADE_START_HOUR,
                                 TRADE_START_MIN)

    # All other days just need to add 1 day to reach next trade day
    else:
        current_time += datetime.timedelta(days=1)
        return datetime.datetime(current_time.year, current_time.month, current_time.day, TRADE_START_HOUR,
                                 TRADE_START_MIN)


def time_until_trade_hours_end() -> datetime:
    """
    Returns the datetime of the next time the trade hours end.

    :return: (datetime): Datatime of when next trade hours close.

    """
    t = datetime.datetime.now().strftime("%H%M")
    t = int(t)
    current_time = datetime.datetime.today()

    # Check if trade day (Mon - Fri) and before 4:00, then just wait until trade end later that day
    if datetime.datetime.today().weekday() < 5:
        if t < TRADE_HHMM_END:
            return datetime.datetime(current_time.year, current_time.month, current_time.day, TRADE_END_HOUR,
                                     TRADE_END_MIN)

    # If after 4:00, check which day
    # if Friday, add 3 days until Monday
    if datetime.datetime.today().weekday() == 4:
        current_time += datetime.timedelta(days=3)
        return datetime.datetime(current_time.year, current_time.month, current_time.day, TRADE_END_HOUR,
                                 TRADE_END_MIN)

    # if Saturday, add a 2 days until Monday
    elif datetime.datetime.today().weekday() == 5:
        current_time += datetime.timedelta(days=2)
        return datetime.datetime(current_time.year, current_time.month, current_time.day, TRADE_END_HOUR,
                                 TRADE_END_MIN)

    # All other days just need to add 1 day to reach nex trade day
    else:
        current_time += datetime.timedelta(days=1)
        return datetime.datetime(current_time.year, current_time.month, current_time.day, TRADE_END_HOUR,
                                 TRADE_END_MIN)


def pause_until_trade_hours_start():
    """
    Pause process until 9:30am of the next day, dynamic based on when the script is started.

    """
    # Not in trade hours so proceed
    if not is_trade_hours():
        time_to_wait = time_until_trade_hours_start()
        print("Pause until: " + str(time_to_wait))
        # Pause until then
        pause.until(time_to_wait)

    # Function should only be called outside trade hours, print error
    else:
        print("pause_until_trade_hours called inside trade hours")


def pause_until_trade_hours_end():
    """
    Pause process until 4:00pm the current day if in trade hours.

    """
    # Not in trade hours so proceed
    if is_trade_hours():
        time_to_wait = time_until_trade_hours_end()
        print("Pause until: " + str(time_to_wait))
        # Pause until then
        pause.until(time_to_wait)

    # Function should only be called outside trade hours, print error
    else:
        print("pause_until_trade_hours_end called inside outside trade hours")


def time_until_hibernation_wake() -> datetime:
    """
    Simple mechanism used to return a value 30 minutes before trade hours to wake up PC from hibernation.

    This is used specifically for the linux_hibernation_script, which HIBERNATES the computer vs pause a script

    :return: (datetime): Datatime of next time to wake from hibernation

    """
    if not is_trade_hours():
        # Get time until next wake
        time_to_wait = time_until_trade_hours_start()

        # Subtract wake time buffer
        time_to_wait -= datetime.timedelta(minutes=TRADE_OPENING_BUFFER_HIBERNATION_MIN)

        print("Hibernation until: " + str(time_to_wait))

        # Return the time to hibernate until
        return time_to_wait

    # Function should only be called outside trade hours, print error
    else:
        print("time_until_hibernation_wake called inside trade hours")


def trade_hours_and_wait_helper(interval_seconds: int = DEFAULT_ALGORITHM_CYCLE_TIME_SECONDS):
    """
    The following does 3 things:
        - Consolidates both wait_until_trade_hours and wait_for_update_intervals into one call for ease to read
        - Will wait for trade hours and only return during trade hours
        - During trade hours, will hold the "interval seconds" time so that the algorithm can be updated
            on that frequency (i.e. if interval_Seconds is 10, the algorithm will update every 10 seconds)

    :param interval_seconds: (int) Time to wait in seconds, during trading hours, for the frequency the algorithms
                                will run
    :return: Returns when in trade hours, if not, will wait until then

    """
    # In trade hours
    if is_trade_hours():
        # Wait for next update based on desired interval time
        print(f"Waiting for {interval_seconds} seconds before next update")
        time.sleep(interval_seconds)
        return
    else:
        # Wait until trade hours
        print("AFTER HOURS")
        pause_until_trade_hours_start()


def trade_hours_and_wait_helper_advanced(interval_seconds: int = DEFAULT_ALGORITHM_CYCLE_TIME_SECONDS) -> int:
    """
    Does the same as trade_hours_and_wait_helper, but instead os basic wait/return, this function
    returns a 1 when waiting during trade hours, and a 2 when out of trade hours.

    This allows functionality to continue after office hours if needed

    :param interval_seconds: (int) Time to wait in seconds, during trading hours, for the frequency the algorithms
                                will run
    :return: (int): Returns 1 when in trade hours (will wait on the interval)
                    Returns 2 when out of trade horus

    """
    # In trade hours
    if is_trade_hours():
        # Wait for next update based on desired interval time
        print(f"Waiting for {interval_seconds} seconds before next update")
        time.sleep(interval_seconds)
        return 1
    else:
        return 2


def write_to_log(log_file: Path, message: str = "", overwrite: bool = True):
    """
    Use to write specific contents to a custom log file

    :param log_file: (Path): The directory of the log file as a Path variable
    :param message: (str): The log message to write in string format
    :param overwrite: (bool): If true, overwrite contents of file, else, append to end of existing file

    """
    if not DATABASE_PATH.is_dir():
        DATABASE_PATH.mkdir()

    if not LOGBASE_PATH.is_dir():
        LOGBASE_PATH.mkdir()

    # Set the overwrite_flag
    if overwrite:
        overwrite_flag = 'w'
    else:
        overwrite_flag = 'a'

    file = open(log_file, overwrite_flag)
    file.write(str(datetime.datetime.today().strftime('%Y-%m-%d-%H:%M:%S'))
               + ", " + str(message)
               + '\n')
    file.close()
