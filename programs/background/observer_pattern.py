"""
Author: Joel Yuhas
Date: July 9th, 2023

Background observer pattern program for exection.

"""
import time
import argparse
from libraries.helper_functions import is_trade_hours, pause_until_trade_hours_start
from libraries.ObserverPattern import ObserverPattern

WAIT_INTERVAL_SECONDS = 10


# need to make this dynamic
def arg_parser():
    """
    Get following information so the program can run
    - desired stock ticker
    - transaction file save location
    - account file save location

    """
    # NOTE will need to update this to have more than 2 eventually
    parser = argparse.ArgumentParser()
    parser.add_argument("stockfile", type=str, help="Text file with stocks in it")

    return parser.parse_args()


def main(args):
    stock_list = []
    # Open the stock file and read the stocks
    with open(args.stockfile, 'r') as file:
        for line in file:
            print(line.rstrip())
            stock_list.append(line.rstrip())

    observer_pattern = ObserverPattern()

    # Create the observer pattern for the stocks in the list_of_stocks.txt file
    for stock in stock_list:
        observer_pattern.add_stock(stock)

    # Main loop
    while True:
        if is_trade_hours():
            observer_pattern.observer_all_stocks()
            time.sleep(WAIT_INTERVAL_SECONDS)
        else:
            pause_until_trade_hours_start()

        time.sleep(WAIT_INTERVAL_SECONDS)


args = arg_parser()
main(args)