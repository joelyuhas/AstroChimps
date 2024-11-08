"""
Author: Joel Yuhas
Date: February 2023

Algorithm 04

Scalable program that adds the "rise and fall transaction" algorithms. Is used to execute these algorithms given the
specific inputs.

"""
import os
import time
import argparse


from libraries.helper_functions import ACCOUNT_LOG_PATH, is_trade_hours, pause_until_trade_hours_start
from libraries.AccountLibrary import AccountLibrary
from libraries.StockFactory import StockFactory
from algorithms import rise_and_fall_transactions


# Time to wait between updates in seconds
WAIT_TIME_SECONDS = 60

# The starting amount in dollars
STARTING_AMOUNT_DOLLARS = 10000


def arg_parser():
    """
    Get following information so the program can run
    - desired stock ticker
    - transaction file save location
    - account file save location

    """
    parser = argparse.ArgumentParser()
    parser.add_argument("account_number", type=int, help="The desired account identifier number")
    parser.add_argument("ticker", type=str, help="The desired stock ticker as string")
    parser.add_argument("loss_threshold", type=float, help="Threshold (int 0-100) percentage to sell at loss")
    parser.add_argument("gain_threshold", type=float, help="Threshold (int 0-100) percentage to buy at gain")

    # NOTE, may want this argument optional and if not produced,then goto default location
    # parser.add_argument("account_path", type=str, help="The Path location of the account directory")
    return parser.parse_args()


def main(args):
    """
    The main loop function that gets sets up the program and gets it ready
    :param args:
    :return:
    """
    # start color
    os.system('color')

    account_path = ACCOUNT_LOG_PATH / ('account_program_04_' + args.ticker)

    # load or create the account
    stock_factory = StockFactory("observer")
    account_one = AccountLibrary(account_number=args.account_number,
                                 account_path=account_path,
                                 stock_factory=stock_factory)
    was_account_create = account_one.create_new_account()

    # If the account doesnt exist, perform first time setup, deposit STARTING_AMOUNT_DOLLARS, and save
    # If not, load from existing account
    if was_account_create:
        account_one.deposit_money(STARTING_AMOUNT_DOLLARS)
        account_one.write_account_to_file()
    else:
        account_one.load_from_file()
        account_one.print_account()

    # if the account has money, buy DESIRED_STOCK before proceeding at current value
    if account_one.money > 0:
        print("Buying stock at the initialization of algorithm_04")
        account_one.buy(ticker=args.ticker, dollar_amount=float(account_one.money))

    # Check that stock exist. If it does not exist and there is no money then there is an issue with the account
    if not account_one.get_stock(args.ticker):
        print("Stock does not exist! Error in initializing. Either not enough money or no desired stock")
        raise RuntimeError

    account_one.print_account()

    # Main loop!
    while True:
        if is_trade_hours():
            # Update all the stock peaks, prices, recent prices, and trends
            account_one.update_stock_values_all()
            # check if still have quantity of stock:
            #   - if no quantity, check to buy
            #   - if yes quantity, check to sell
            # Currently setup to sell 100% and buy at 100% quantity
            stock = account_one.get_stock(args.ticker)
            print(f"STOCK QUANTITY: {stock.quantity}")
            if stock.quantity > 0:
                print("In no stock quantity")
                rise_and_fall_transactions.sell_if_fall(account_one, stock, args.loss_threshold, stock.new_high)
            else:
                print("In stock quantity")
                rise_and_fall_transactions.buy_if_rise(account_one, stock, args.gain_threshold, stock.new_low)
            # Wait for next update
            print(f"Waiting for {WAIT_TIME_SECONDS} seconds")
            time.sleep(WAIT_TIME_SECONDS)
        else:
            account_one.write_account_to_file(end_of_day_save=True)
            pause_until_trade_hours_start()


args = arg_parser()
main(args)

print("Finsihed!")