"""
Author: Joel Yuhas
Date: July 8th, 2023

StockFactory

Used to create specific subclasses of the Stock class, specifically when a class needs it to be done for them since the
stock class can be dynamically made to one of the subclasses.


"""
from typing import Union

from libraries.StockSubClasses import StockObserver, StockDirect


class StockFactory:
    def __init__(self, stock_type):
        self.stock_type = stock_type

    def create_stock(self, ticker: str) -> Union[StockObserver, StockDirect]:
        """
        Create the stock class based on its ticker. Currently, it can either be the StockObserver or StockDirect type.

        Stock type is set as variable of the StockFactory class

        :param ticker: (str): Ticker of the stock class
        :return:(StockObserver or StockDirect): Returns the desired stock class, currently just between Observer and
                                                direct

        """
        if self.stock_type == "direct":
            return StockDirect(name=ticker)
        if self.stock_type == "observer":
            return StockObserver(name=ticker)
        else:
            raise ValueError("Invalid Stock Type")

    def dict_to_stock(self, stock_dict: dict) -> Union[StockObserver, StockDirect]:
        """
        Turn the dictionary item that contains the stock information into a Stock object.

        :param stock_dict: (dict): The dictionary to be turned to stock object
        :return:(StockObserver or StockDirect): Return the specified stock based on the provided values in the class

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

        if self.stock_type == "direct":
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

        if self.stock_type == "observer":
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

        else:
            raise ValueError("Invalid Stock Type")

