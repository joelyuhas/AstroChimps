"""
Author: Joel Yuhas
Date: December 1st, 2021

Test creating and loading accounts

"""
import os
from libraries.AccountLibrary import AccountLibrary
from libraries.StockFactory import StockFactory
from libraries import helper_functions


def main():
    os.system('color')

    account_path = helper_functions.ACCOUNT_LOG_PATH / "account_program_04_QQQ"
    # stock_factory = StockFactory("observer")
    stock_factory = StockFactory("direct")
    account_one = AccountLibrary(account_number="1",
                                 account_path=account_path,
                                 stock_factory=stock_factory)


    # POSITIVE TEST
    # ------------------
    print("BEGINNING TEST")
    account_one.load_from_file()
    account_one.print_account()
    account_one.update_stock_values_all()
    account_one.print_account()


main()

print("Finsihed!")