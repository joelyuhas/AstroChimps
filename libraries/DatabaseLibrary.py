"""
Author: Joel Yuhas
Date: May 10th, 2022

DatabaseLibrary

The databases in this program are used to store a variety of stock information. Some of the info is used for eventual
regression testing on previous stock values, while others are used by active trading programs. This library is used to
help generalize the database collection code and methods.


"""
import yfinance as yf
import time
from datetime import datetime

from libraries import helper_functions


# The default update time interval in seconds
WAIT_TIME_INTERVAL_SECONDS = 300


class DatabaseLibrary:
    def __init__(self, stocks: list[str] = None):
        # Receives an array of string stock tickers.
        # The code will take care of the rest in terms of the file names!
        # Currently coded to save in the databases/developing databases directories
        self.stocks = stocks if stocks is not None else []

    @staticmethod
    def get_raw_value(ticker: str):
        """
        Get the raw value of the specified ticker.

        :param ticker: (str): Ticker of desired stock.
        :return: returns all yahoo finance data history

        """
        ticker = yf.Ticker(ticker)
        return ticker.history(period='1d')

    def write_to_database_iterator(self, ticker: str):
        """
        Write stock information to database file. This method is designed to be called multiple times a day and
        iterate based on the desired time interval.

        This function writes full date and time along with the stock price to 3 decimal places

        :param ticker:(str) Ticker of desired stock.

        """
        current_month_year = datetime.now().strftime("%Y_%m")
        database_file = helper_functions.DATABASE_PATH / (ticker + "_" + current_month_year + "_interval.txt")
        file = open(database_file, "a")

        # Get most recent value, check first the ticker can be found in case of issues (sometimes will fail)
        try:
            yf_close = self.get_raw_value(ticker)['Close'][0]
        except IndexError:
            print("ISSUE WITH CALLING STOCK VALUES ITERATOR")
            helper_functions.write_to_log(helper_functions.LOGBASE_PATH / ('execution_' + str(ticker) + '_debug_log.txt'),
                                          "ISSUE WITH CALLING STOCK VALUES, database_iterator, cant find ticker",
                                          False)
            close_format = "ERROR-1"
        else:
            close_format = "{:.3f}".format(yf_close)

        file.write(str(datetime.today().strftime('%Y-%m-%d-%H:%M:%S'))
                   + "," + str(close_format)
                   + '\n')
        file.close()

    def write_to_database_daily(self, ticker: str):
        """
        Write stock information to database file.

        This function designed to be executed once per day, and includes the open, high, low, close and volume of
        specified stock.

        :param ticker: (str): Ticker of desired stock.

        """
        database_file = helper_functions.DATABASE_PATH / (ticker + "_daily.txt")
        file = open(database_file, "a")

        attempts = 0
        while attempts < 5:
            try:
                print("After daily, getting stock values")
                yahoo_stock = self.get_raw_value(ticker)
                # Run to check the stock info retrieval, if no 'Close' value, index error will occur
                yahoo_stock['Close'][0]
            except IndexError:
                print("ISSUE WITH CALLING STOCK VALUES DAILY")
                helper_functions.write_to_log(helper_functions.LOGBASE_PATH / ('execution_' + str(ticker) + '_debug_log.txt'),
                                              "ISSUE WITH CALLING STOCK VALUES, write_to_database_daily, cant find ticker",
                                              False)
                file.write(str(datetime.today().strftime('%Y-%m-%d'))
                           + "," + "ERROR-1"
                           + '\n')
                attempts += 1

            else:
                print("Writing the values needed")
                # get all desired daily values
                yf_open = yahoo_stock['Open'][0]
                yf_high = yahoo_stock['High'][0]
                yf_low = yahoo_stock['Low'][0]
                yf_close = yahoo_stock['Close'][0]
                yf_volume = yahoo_stock['Volume'][0]

                # Format: Date,Open,High,Low,Close,Volume
                open_format = "{:.3f}".format(yf_open)
                high_format = "{:.3f}".format(yf_high)
                low_format = "{:.3f}".format(yf_low)
                close_format = "{:.3f}".format(yf_close)
                file.write(str(datetime.today().strftime('%Y-%m-%d'))
                           + "," + str(open_format)
                           + "," + str(high_format)
                           + "," + str(low_format)
                           + "," + str(close_format)
                           + "," + str(yf_volume)
                           + '\n')
            break
        file.close()

    def execution(self):
        """
        This method continuously runs and gathers the information at the specified update interval time.

        """
        # Flag used to see if script is activated during trading
        trading_flag = False

        # Main loop!
        while True:
            # Check if in trading hours
            if helper_functions.is_trade_hours():
                # In trading hours, set flag high, iterate on each stock, then sleep for wait_time_interval_seconds
                print("In trade hours, performing iterations")

                trading_flag = True
                for stock in self.stocks:
                    # pass in iterator file path and stock name
                    helper_functions.write_to_log(helper_functions.LOGBASE_PATH / ('execution_' + str(stock) + '_debug_log.txt'), "In trade hours, performing iterations", False)
                    self.write_to_database_iterator(stock)
                time.sleep(WAIT_TIME_INTERVAL_SECONDS)

            # Out of trade hours
            else:
                print("AFTER HOURS")
                # Only write daily values if program was running during trade hours, otherwise this could be
                # unnecessary addition (also may cause bug if attempting this part outside of trade horus or right as
                # computer turns on when not fully connected to internet
                helper_functions.write_to_log(helper_functions.LOGBASE_PATH / 'general_execution_debug_log.txt', False)
                helper_functions.write_to_log(helper_functions.LOGBASE_PATH / 'general_execution_debug_log.txt', str(trading_flag), False)
                if trading_flag:
                    for stock in self.stocks:
                        helper_functions.write_to_log(helper_functions.LOGBASE_PATH / ('execution_' + str(stock) + '_debug_log.txt'), helper_functions.time_until_trade_hours_start(), False)
                        # pass in daily file path and stock name
                        self.write_to_database_daily(stock)
                        helper_functions.write_to_log(helper_functions.LOGBASE_PATH / ('execution_' + str(stock) + '_debug_log.txt'), "Writing to the database daily file!", False)
                    trading_flag = False

                # Regardless of trading, pause until start of trading hours
                helper_functions.pause_until_trade_hours_start()

    def manual_dailies(self):
        """
        In case daily values were missed due to outage, this can be ran manually to gather them again

        """
        print("Gathering daily values")
        for stock in self.stocks:
            print("Writing daily for: " + str(stock))
            self.write_to_database_daily(stock)