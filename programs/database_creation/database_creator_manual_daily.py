"""
Author: Joel Yuhas
Date: May 13th, 2022

If a daily value was missed, this tool can be run manually to gather those values after hours or for other debugging
purposes.

"""
from libraries.DatabaseLibrary import DatabaseLibrary

STOCK_LIST = ["QQQ",
              "TQQQ",
              "VOO"]


def main():
    # Add values to stock list if needed!
    databases = DatabaseLibrary(stocks=STOCK_LIST)
    databases.manual_dailies()


main()
