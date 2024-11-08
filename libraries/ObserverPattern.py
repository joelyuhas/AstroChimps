"""
Author: Joel Yuhas
Date: November 30th, 2023

ObserverPattern

Class for observing the desired stock values and saving them to a database so other programs can use them.

This does twofold:
- Alleviates the issue where only so many yfinance calls can be done in a day, having only one observer pattern do this
  drastically reduces the amount of calls instead of having each individual program do their own calls
- Consolidates and simplifies how the stock values are gathered and read from. By having the observer pattern be solely
  responsible for collecting stock values, it simplifies the methods and creates on one location where the stock values
  are gathered/saved. This makes the code more maintainable and easily scalable. Also makes it easier to have a standard
  interface across other parts of the code.


"""

import yfinance as yf
import sqlite3
import datetime
import os
from pathlib import Path

from libraries.helper_functions import OBSERVER_DATABASE_PATH


class ObserverPattern:
    def __init__(self):
        self.stock_dict = {}

    def add_stock(self, stock_ticker: str):
        """
        Add the desired stock to the stock dictionary and link its database file.

        :param stock_ticker: (string): The ticker of the stock to be added.

        """
        # If the ticket is not already in the stock_dict, add it. If not, should be already added.
        if stock_ticker not in self.stock_dict:
            database_file = self.setup_observe_stock(stock_ticker)
            self.stock_dict[stock_ticker] = database_file

    @staticmethod
    def fetch_stock_price(stock_ticker: str) -> float:
        """
        Fetch the stock price for the desired stock ticker using yfinance

        :param stock_ticker: (str): The ticket of the stock to get the current price from.
        :return: (float): The yfinance value of the stock in float format

        """
        try:
            ticker = yf.Ticker(stock_ticker)
            todays_data = ticker.history(period='1d')
        except RuntimeError:
            print("issue fetching stock price")

        return todays_data['Close'][0]

    @staticmethod
    def create_db(file_name: Path):
        """
        Create a sqlite database with specific file name.

        :param file_name: (Path): The name of the database file to be created

        """
        conn = sqlite3.connect(file_name)
        c = conn.cursor()
        c.execute('''CREATE TABLE stocks (timestamp text, stock_ticker text, price real)''')
        conn.commit()
        conn.close()

    @staticmethod
    def write_to_db(file_name: Path, stock_ticker: str, price: float, timestamp: str):
        """
        Write to the specified database with the stock ticker name, price of the stock, and timestamp values.

        :param file_name: (Path): Filename and path of the file of the database to write to
        :param stock_ticker: (str): The ticker of the stock
        :param price: (float): The price of the stock in float format
        :param timestamp: (str): The timestamp the write_to_db has taken place, typically in Y-m-d H:M:S format

        """
        try:
            conn = sqlite3.connect(file_name)
            c = conn.cursor()
            c.execute("INSERT INTO stocks VALUES (?,?,?)", (timestamp, stock_ticker, price))
            conn.commit()
        except sqlite3.OperationalError as e:
            c.execute('''CREATE TABLE IF NOT EXISTS stocks
                         (timestamp text, stock_ticker text, price real)''')
            conn.commit()
        finally:
            conn.close()

    def setup_observe_stock(self, stock_ticker: str) -> Path:
        """
        Set up an observer for the specific stock ticker provided. Return the path to the database.

        :param stock_ticker: (str): The ticket of the stock
        :return: (Path): The path of the database file for the specific stock.
        """
        current_month_year = datetime.datetime.now().strftime("%Y_%m")
        file_name = f"stocks_{stock_ticker}_{current_month_year}.db"
        full_file_name = OBSERVER_DATABASE_PATH / file_name
        try:
            # try to connect to the db file for the current month, if it doesn't exist then create it
            if os.path.exists(full_file_name):
                sqlite3.connect(full_file_name)
            else:
                self.create_db(full_file_name)
        except:
            self.create_db(full_file_name)

        return full_file_name

    def observe_stock(self, stock_ticker: str, file_name: Path):
        """
        Begin observation of the stock and record the information, including price and timestamp of price, to the
        database file name.

        :param stock_ticker: (str): The ticker of the stock to observe
        :param file_name: (Path): The filename path where the corresponding stock database is located.

        """
        price = self.fetch_stock_price(stock_ticker)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.write_to_db(file_name, stock_ticker, price, timestamp)

    def observer_all_stocks(self):
        """
        Basic helper function to observe all stocks in the stock dictionary.

        """
        for stock in self.stock_dict:
            print(stock)
            self.observe_stock(stock, self.stock_dict[stock])

