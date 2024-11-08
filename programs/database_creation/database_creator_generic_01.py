"""
Author: Joel Yuhas
Date: May 10th, 2022

Used to get the price of a stock at specific times and use that to create databases for such.

"""
from libraries.DatabaseLibrary import DatabaseLibrary

STOCK_LIST = ["QQQ",
              "TQQQ",
              "VOO"]


def main():
    # Add values to stock list if needed!
    databases = DatabaseLibrary(stocks=STOCK_LIST)
    databases.execution()


main()
