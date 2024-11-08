"""
Author: Joel Yuhas
Date: December 1st, 2021

Lite testing for basic test cases.

"""
import os
from libraries.AccountLibrary import AccountLibrary
from libraries.StockFactory import StockFactory
from libraries import helper_functions


def main():
    os.system('color')

    account_path = helper_functions.ACCOUNT_LOG_PATH / "account_test"
    # stock_factory = StockFactory("observer")
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
    account_one.buy(ticker="SPXS", dollar_amount=500.0)
    account_one.print_account()

    helper_functions.evaluator_helper(account_one.get_stock("SPXS"))

    # buy two stocks (dollar amount)
    print("account_one.buy(ticker=SPXS, dollar_amount=100.0)")
    print("account_one.buy(ticker=TSLA, dollar_amount=10.0)")
    account_one.buy(ticker="SPXS", dollar_amount=100.0)
    account_one.buy(ticker="TSLA", dollar_amount=10.0)
    account_one.print_account()

    helper_functions.evaluator_helper(len(account_one.stocks) == 2)

    # Deposit money
    print("account_one.deposit_money(10000.0)")
    account_one.deposit_money(10000.0)
    account_one.print_account()
    print("account_one.deposit_money(300.0)")
    account_one.deposit_money(300.0)
    account_one.print_account()

    helper_functions.evaluator_helper(account_one.get_account_value() == 11300.0)

    # Withdraw money
    print("account_one.withdraw_money(3000.0)")
    account_one.withdraw_money(3000.0)
    account_one.print_account()

    helper_functions.evaluator_helper(account_one.get_account_value() == 8300.0)

    # Buy new stock (stock amount)
    print("account_one.buy(ticker=VOO, stock_amount=5.0)")
    account_one.buy(ticker="VOO", stock_amount=5.0)
    account_one.print_account()

    helper_functions.evaluator_helper(len(account_one.stocks) == 3)

    # Sell stock (dollar_amount)
    print("account_one.sell(ticker=VOO, dollar_amount=40.0)")
    account_one.sell(ticker="VOO", dollar_amount=40.0)
    account_one.print_account()

    # sell older stock (stock_amount)
    print("account_one.sell(ticker=SPXS, stock_amount=4.0)")
    account_one.sell(ticker="SPXS", stock_amount=4.0)
    account_one.print_account()

    # Withdraw money again
    print("account_one.withdraw_money(3.2)")
    account_one.withdraw_money(3.2)
    account_one.print_account()

    helper_functions.evaluator_helper(account_one.get_account_value() < 8297 and account_one.get_account_value() > 8296)

    # Withdraw money again
    print("writing account to file")
    account_one.write_account_to_file()
    account_one.print_account()


main()

print("Finsihed!")