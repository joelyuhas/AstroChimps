"""
Author: Joel Yuhas
Date: July 8th, 2023

Class StockSubClasses

This class is used to store information and logic an owned stock depending on if its an Observer stock or a Direct
stock.

- Observer stocks, get their stock values from the observer patter class
- Direct stocks, get their stock values directly from yfinance
- Retro stocks (planned), get their stock values from already saved data so it can be ran against existing data sets


Specific information includes but not limited to:
        self.name               : (int)     Name/ticker of the stock
        self.quantity           : (float)   The amount of the stock in # of stocks
        self.buy_price          : (float)   price the stock was originally bought at (discrepancy is more bought later)
        self.last_price         : (float)   Last known price of the stock
        self.peak               : (float)   Peak price of the stock
        self.transaction_file   : (str)     Directory to transaction file
        self.account_file       : (str)     Director to account file

More information is being added as time goes on as well.

NOTE: Transaction and account file are used ot save transaction and account data for later on.

"""

import yfinance as yf
import sqlite3
import time
from pathlib import Path

from libraries.helper_functions import OBSERVER_DATABASE_PATH
from libraries.StockBaseClass import StockBaseClass

# The index where the price is listed in the database.
PRICE_INDEX = 2

class StockObserver(StockBaseClass):
    """
    Stock observer
    This variation of the stock class is compatible with the observer class and gets its values from there

    """


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @staticmethod
    def get_current_file_name(ticker: str) -> Path:
        """
        Get the current file name where the stock info is stored.

        :param ticker: (str): The name of the stock ticker
        :return: (Path): The Path of the current filename for the stock.

        """
        # Get the current year and month
        current_time = time.localtime()
        year = str(current_time.tm_year)
        month = str(current_time.tm_mon).zfill(2)

        return OBSERVER_DATABASE_PATH / f'stocks_{ticker}_{year}_{month}.db'

    @staticmethod
    def get_current_price(ticker: str) -> float:
        """
        Get the current price from the database of the corresponding stock ticker.

        :param ticker: (str): The name of the stock ticker
        :return: (float): The latest price as a float

        """
        # Connect to the database file
        try:
            conn = sqlite3.connect(StockObserver.get_current_file_name(ticker))
            c = conn.cursor()

            # Get the latest stock information
            c.execute("SELECT * FROM stocks ORDER BY timestamp DESC LIMIT 1")
            latest_stock_info = c.fetchone()
            conn.close()
        except:
            print("ISSUE GETTING STOCK INFO, file most likely does not exist, ensure observer is running")
            print("Stock name: %s", ticker)
            print("fetching value directly")
            raise AssertionError

        return float(latest_stock_info[PRICE_INDEX])

    @staticmethod
    def dict_to_stock(stock_dict: dict) -> 'StockObserver':
        """
        Turn the dictionary item that contains the stock information into a Stock object

        :param stock_dict: (dict) The already made dictionary with the saved stock info
        :return: (StockObserver): The created StockObserver class
        """
        name = stock_dict['name']
        quantity = stock_dict['quantity']
        buy_price = stock_dict['buy_price']
        sell_price = stock_dict['sell_price']
        all_time_peak = stock_dict['all_time_peak']
        last_high = stock_dict['last_high']
        last_low = stock_dict['last_low']
        trend = stock_dict['trend']
        last_price = stock_dict['last_price']
        transaction_file = stock_dict['transaction_file']
        account_file = stock_dict['account_file']
        new_high = stock_dict['new_high']
        new_low = stock_dict['new_low']

        return StockObserver(name=name,
                             quantity=quantity,
                             buy_price=buy_price,
                             sell_price=sell_price,
                             all_time_peak=all_time_peak,
                             last_high=last_high,
                             last_low=last_low,
                             trend=trend,
                             last_price=last_price,
                             transaction_file=transaction_file,
                             account_file=account_file,
                             new_high=new_high,
                             new_low=new_low)


class StockDirect(StockBaseClass):
    """
    StockDirect

    This class is for direct stock connection, where it will get the values directly from yahoo finance with no
    observer.

    Pros:
        - No need for observer pattern
        - Good for lite use

    Cons:
        - Doesn't scale well as there is limit to how many yfinance calls there can be a day
            - Can only check a few of these stocks at a time
        - Slower since has to do many more calls
        - If multiple accounts are running, then alot of duplicate calls

    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @staticmethod
    def get_current_file_name(ticker: str) -> Path:
        """
        Return nothing here since this method is not needed for direct stock.

        """
        return None

    @staticmethod
    def get_current_price(ticker: str) -> float:
        """
        Return the current price from the stock directly given its ticker.

        :param ticker: (str): The name of the stock ticker
        :return: (float): The latest price as a float

        """
        try:
            ticker = yf.Ticker(ticker)
            todays_data = ticker.history(period='1d')
            return float(todays_data['Close'][0])
        except RuntimeError:
            print("RunTime Error encountered while getting current price for " + ticker)

    @staticmethod
    def dict_to_stock(stock_dict: dict) -> 'StockDirect':
        """
        Turn the dictionary item that contains the stock information into a StockDirect Object.

        :param stock_dict: (dict): The dictionary to be turned into a stock
        :return: (StockDirect): A stock direct object with stock_dict info

        """
        name = stock_dict['name']
        quantity = stock_dict['quantity']
        buy_price = stock_dict['buy_price']
        sell_price = stock_dict['sell_price']
        all_time_peak = stock_dict['all_time_peak']
        last_high = stock_dict['last_high']
        last_low = stock_dict['last_low']
        trend = stock_dict['trend']
        last_price = stock_dict['last_price']
        transaction_file = stock_dict['transaction_file']
        account_file = stock_dict['account_file']
        new_high = stock_dict['new_high']
        new_low = stock_dict['new_low']

        return StockDirect(name=name,
                           quantity=quantity,
                           buy_price=buy_price,
                           sell_price=sell_price,
                           all_time_peak=all_time_peak,
                           last_high=last_high,
                           last_low=last_low,
                           trend=trend,
                           last_price=last_price,
                           transaction_file=transaction_file,
                           account_file=account_file,
                           new_high=new_high,
                           new_low=new_low)




