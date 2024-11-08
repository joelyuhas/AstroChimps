"""
Author: Joel Yuhas
Date: February 8th, 2023

Class StockBaseClass:

The Base Stock Class that other stock classes will inherit from. This includes all the core functionality for the stock
and what methods are needed.


"""
from abc import ABC, abstractmethod
from pathlib import Path
from libraries.helper_functions import Colors


class StockBaseClass(ABC):
    def __init__(self, name: str = None, quantity: float = 0.0, buy_price: float = None, sell_price: float = None,
                 last_high: float = 0.0, last_low: float = 0.0, all_time_peak: float = 0, trend: str = None,
                 last_price: str = None, transaction_file: Path = None, account_file: Path = None,
                 new_high: float = None, new_low: float = None):
        self.name = name
        self.quantity = quantity
        self.buy_price = buy_price
        self.sell_price = sell_price
        self.all_time_peak = all_time_peak  # all time stock peak
        self.last_high = last_high  # most recent high
        self.last_low = last_low  # most recent low
        self.trend = trend
        self.last_price = last_price or self.get_current_price(self.name)
        self.transaction_file = transaction_file
        self.account_file = account_file
        self.new_high = new_high or self.last_price  # new nigh after a buy, if no buy then last price
        self.new_low = new_low or self.last_price

        # All below get initialized by update_price
        self.stock_file_name = self.get_current_file_name(self.name)

        # new low after a sell, if no sell then last price
        self.daily_high = self.last_price  # highest point of that day
        self.daily_low = self.last_price  # lowest point of that day

        self.last_last_price = self.last_price  # last know price before the last price
        # TODO: Potentially update the prices to just be a list so that multiple variables dont need to keep beign added and have
        #  alot more informaiton

    @staticmethod
    @abstractmethod
    def get_current_file_name(ticker: str):
        pass

    @staticmethod
    @abstractmethod
    def get_current_price(ticker: str) -> float:
        pass

    @staticmethod
    @abstractmethod
    def dict_to_stock(stock_dict: dict) -> 'StockBaseClass':
        pass

    @staticmethod
    def stock_to_dict(stock) -> dict:
        """
        Turn a stock into a dictionary format so that it can be saved. Separated out so that it can be compartmentalized
        into just this file

        :param stock: (StockBaseClass): The stock that is being turned into a dict.
        :return: (dict): The stock information in a dict
        """
        stock_dict = {
            'name': stock.name,
            'quantity': stock.quantity,
            'buy_price': stock.buy_price,
            'sell_price': stock.sell_price,
            'all_time_peak': stock.all_time_peak,
            'last_high': stock.last_high,
            'last_low': stock.last_low,
            'trend': stock.trend,
            'last_price': stock.last_price,
            'transaction_file': stock.transaction_file,
            'account_file': stock.account_file,
            'new_high': stock.new_high,
            'new_low': stock.new_low
        }
        return stock_dict

    def print_stock(self) -> str:
        """
        Print detailed information on the stock, intended for debugging.

        :return: (str): The stock and its parameters as a string for printing purposes

        """
        value = f"      name: {self.name} quant: {self.quantity} last_price: {self.last_price} total_val: " \
                f"{self.total_value()} sell_price : {self.sell_price}"

        print(value)

        return value

    def print_stock_compact(self):
        """
        Color coded print important stock values. Intended for real time use and debugging.

        """
        # Set the color for the print statement based on the trend
        if self.trend == "UP":
            color = Colors.GREEN
        else:
            color = Colors.ORANGE

        print(color + f"{self.name} at {self.last_price} last {self.last_last_price} trend {self.trend} "
                      f"last high {self.last_high} " f"last low {self.last_low} daily high {self.daily_high} "
                      f"daily low {self.daily_low} new high {self.new_high} new low {self.new_low}")

    def total_value(self) -> float:
        """
        Gets the total monetary value of the stock. update is required to run before. Will use last_price value

        :return: (float): Total monetary value of the current stock based on its price and quantity
        """
        return self.quantity * self.last_price

    def update_stock_values(self):
        """
        Update all peaks, trends, valleys, and last price with only one API call.

        NOTE: May want to break up into separate functions like before if we find we need the other functions separate.
              Kept it this way so that only 1 latest price call needs to be made**

        Method will most likely update as more information is added

        """

        # Note, may update this so that it is a list of all previous prices so we dont need creeping values like this
        self.last_last_price = self.last_price
        self.last_price = self.get_current_price(self.name)

        # Set trend
        # ------------------
        if self.last_price >= self.last_last_price:
            self.trend = "UP"
        else:
            self.trend = "DOWN"

        # Set last_high/low}
        # ----------------------
        # Stock still going up, raising new last high
        if self.last_price > self.last_high:
            self.last_high = self.last_price

        # Price is continuing to go down, keep updating last low
        elif self.last_price < self.last_low:
            self.last_low = self.last_price

        # stock just passed last high, start new last low
        elif self.trend == "UP":
            self.last_high = self.last_price

        # Price is going up since last low, update new highs
        elif self.trend == "DOWN":
            self.last_low = self.last_price

        # Daily peaks
        # ---------------------------
        if self.last_price > self.daily_high:
            self.daily_high = self.last_price
        elif self.daily_low > self.last_price:
            self.daily_low = self.last_price

        # New peaks
        # Note, these flags are used for stop losses. Currently, they only will work if you sell ALL stocks when wanting
        # to sell sinceit uses quanity to trigger the resets. Otherwise, flags wont be reset. This will need to be
        # updated in the future.
        # ---------------------------

        # If there ARE stocks, then reset the low, track the high
        if self.quantity > 0.0:
            if self.last_price > self.new_high:
                self.new_high = self.last_price
            self.new_low = self.last_price

        # If there are now stocks, track the low, reset the high
        else:
            if self.new_low > self.last_price:
                self.new_low = self.last_price
            self.new_high = self.last_price