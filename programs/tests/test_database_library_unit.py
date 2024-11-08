"""
Basic database library testing for manual use.


"""



import datetime

from unittest.mock import MagicMock
from libraries.DatabaseLibrary import DatabaseLibrary
from libraries import helper_functions


STOCK_LIST = ("NOTREAL_TEST",
              "AAPL")


def ensure_todays_date_in_file(log_file):
    """
    Check the file, if datetime for today is recorded already, do not shut down. This is added safety feature
    :return: 0 for valid date, but does not match today
             1 for valid date, but matches today
             2 for no file detected
    """
    try:
        with open(log_file, 'r') as f:
            last_date = f.read().split(',')[-2]
            my_date = datetime.datetime.strptime(last_date, '%Y-%m-%d-%H:%M:%S')
    except FileNotFoundError:
        print("ERROR: File does not exist, return True in case of corruption")
        print("Creating file now")
        helper_functions.write_to_log(log_file=log_file, overwrite=True)
        return False

    if my_date.strftime("%Y-%m-%d") == datetime.datetime.now().strftime("%Y-%m-%d"):
        return True
    else:
        return False


def test_write_to_database_iterator():
    data_lib = DatabaseLibrary(stocks=STOCK_LIST)
    for stock in STOCK_LIST:
        print("Performing update: " + stock)
        data_lib.write_to_database_iterator(stock)

        # Get the path's of the files that should be created
        test_database_path = helper_functions.DATABASE_PATH / (stock + "_interval.txt")
        test_log_path = helper_functions.LOGBASE_PATH / (stock + "_interval.txt")

        # Ensure logs are created
        helper_functions.evaluator_helper(test_database_path.is_dir())
        helper_functions.evaluator_helper(test_log_path.is_dir())

        # Ensure correct dates are valid
        ensure_todays_date_in_file(test_database_path)
        ensure_todays_date_in_file(test_log_path)

        #Remove created files


    print("tewt")


def test_write_to_database_daily():
    # Ensure log file is created
    # Ensure it has the correct time and value
    # Remove the files
    print("test2")


def test_exection():
    # Ensure log file is created
    # Ensure it has the correct time and value
    # Remove the files
    print("test")


def main():
    print("Starting Tests!")
    test_write_to_database_iterator()


main()