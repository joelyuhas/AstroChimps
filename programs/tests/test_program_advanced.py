"""
Author: Joel Yuhas
Date: December 1st, 2021

More in depth test cases that covers some edge cases.

"""

import os
from libraries.AccountLibrary import AccountLibrary
from libraries.StockFactory import StockFactory
from libraries import helper_functions

def main():
    account_path = helper_functions.ACCOUNT_LOG_PATH / "account_test"
    #stock_factory = StockFactory("observer")
    stock_factory = StockFactory("direct")
    account_one = AccountLibrary(account_number=123456,
                                 money=1000,
                                 account_path=account_path,
                                 stock_factory=stock_factory)

    # POSITIVE TEST
    # ------------------
    print("BEGINNING POSITIVE TEST")
    account_one.print_account()

    # First buy two stocks (dollar amount)
    print("account_one.buy(ticker=SPXS, dollar_amount=500.0)")
    account_one.buy(ticker="QQQ", dollar_amount=500.0)
    account_one.print_account()


    # buy two stocks (dollar amount)
    print("account_one.buy(ticker=SPXS, dollar_amount=100.0)")
    print("account_one.buy(ticker=TSLA, dollar_amount=10.0)")
    #account_one.buy(ticker="SPXS", dollar_amount=100.0)
    #account_one.buy(ticker="TSLA", dollar_amount=10.0)
    account_one.print_account()

    # Deposit money
    print("account_one.deposit_money(10000.0)")
    account_one.deposit_money(10000.0)
    account_one.print_account()
    print("account_one.deposit_money(300.0)")
    account_one.deposit_money(300.0)
    account_one.print_account()
#
    # Withdraw money
    print("account_one.withdraw_money(3000.0)")
    account_one.withdraw_money(3000.0)
    account_one.print_account()
#
    # Buy new stock (stock amount)
    print("account_one.buy(ticker=VOO, stock_amount=5.0)")
    account_one.buy(ticker="VOO", stock_amount=5.0)
    account_one.print_account()
#
    # Sell stock (dollar_amount)
    print("account_one.sell(ticker=VOO, dollar_amount=40.0)")
    account_one.sell(ticker="VOO", dollar_amount=40.0)
    account_one.print_account()

    # Write to account file
    print("Write to account file")
    account_one.write_account_to_file()
    account_one.print_account()

    # Load to new account from transaction file
    print("Load from account file")
    #account_two.load_from_file()
    #account_two.print_account()





    input("press enter to continue")

main()

print("Finsihed!")