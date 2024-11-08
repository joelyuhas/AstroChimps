"""
Author: Joel Yuhas
Date: Jan 7th, 2022

Early proof of concept that focuses on creating an end to end/day to day algorithm that can store
the highs and lows of one specific stock and sell/buy at specific times.

"""

from libraries import AccountLibrary, StockFactory


def buy_if_rise(account: AccountLibrary, stock: StockFactory, rise_percent_threshold: int, last_low_valley: float):
    """
    Method to buy the specified stock if it rises past a certain threshold from last_low_valley stock value.

    :param account: (AccountLibrary): Account that is being traded from
    :param stock: (StockFactory): The stock that is being traded
    :param rise_percent_threshold: (int): The percent threshold for when to buy the stock
    :param last_low_valley: (float): The last reported stock low price

    """
    # Check if need to buy by checking accounts cash. If 0 then no need to buy, skip
    if account.money > 0.0:
        # Stock below daily high
        print(f"LAST PRICE: {stock.last_price} MEASURED LOW: {last_low_valley}")
        if stock.last_price > last_low_valley:
            diff = stock.last_price - last_low_valley
            buy_threshold = last_low_valley * (rise_percent_threshold / 100)
            print(f"BIR: diff = {diff}, thresh = {buy_threshold} ")

            # if the difference is greater than the threshold, sell
            if diff > buy_threshold:
                print('\033[95m' + "BUYING")
                account.buy(ticker=stock.name, dollar_amount=account.money)
                account.write_account_to_file()
                account.print_account()


def sell_if_fall(account: AccountLibrary, stock: StockFactory, loss_percent_threshold: int, last_high_peak: float):
    """
    Method to sell the specified stock if it falls past a certain threshold from last_high_peak stock value.

    :param account: (AccountLibrary): The account thats being traded form
    :param stock: (StockFactory): The stock that's being traded
    :param loss_percent_threshold: (int): The percent threshold for when to sell the stock
    :param last_high_peak: (float):

    """
    # If no money in account, all of it should have been bought into stocks NOTE: UPDATE TO STOCKS INSTEAD
    if account.money == 0.0:
        # Stock below daily high
        print(f"LAST PRICE: {stock.last_price} MEASURED HIGH: {last_high_peak} ")
        if stock.last_price < last_high_peak:
            diff = last_high_peak - stock.last_price
            sell_threshold_amount = last_high_peak * (loss_percent_threshold/100)
            print(f"SID: diff = {diff}, thresh = {sell_threshold_amount} ")
            # if the difference is greater than the threshold, sell
            if diff > sell_threshold_amount:
                print('\033[95m' + "SELLING")
                account.sell(ticker=stock.name, stock_amount=stock.quantity)
                account.write_account_to_file()
                account.print_account()
