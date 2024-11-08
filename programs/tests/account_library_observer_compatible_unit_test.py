"""
Author: Joel Yuhas
Date: December 1st, 2021


Test to ensure basic StockFactory, AccountLibrary, and other functions. Basic test with observer and direct stock
compatible. Used to ensure nothing major is broken when performing updates.

----- NOTE ------
Even if the output is totally green, the error messages may be incorrect in the negative tests and/or some
of the positive tests may also be wrong.

The colors is supposed to supply a quick glance check of pass fail, but for more detail, manual evaluation is
recommended.

"""
import os
from libraries.AccountLibrary import AccountLibrary
from libraries.StockFactory import StockFactory
from libraries import helper_functions


def main():
    os.system('color')

    account_path = helper_functions.ACCOUNT_LOG_PATH / "account_test"
    # Can toggle between observer and direct
    # stock_factory = StockFactory("observer")
    stock_factory = StockFactory("direct")
    account_one = AccountLibrary(account_number=123456,
                                 money=1000,
                                 account_path=account_path,
                                 stock_factory=stock_factory)

    # POSITIVE TEST
    # ------------------
    print("BEGINNING POSITIVE TEST")
    print("create new account")
    account_one.create_new_account()
    account_one.print_account()

    # First buy two stocks (dollar amount)
    print("account_one.buy(ticker=VOO, dollar_amount=500.0)")
    account_one.buy(ticker="VOO", dollar_amount=500.0)
    account_one.print_account()

    # Buy another stock
    print("account_one.buy(ticker=QQQ, dollar_amount=500.0)")
    account_one.buy(ticker="QQQ", dollar_amount=500.0)
    account_one.print_account()

    # Write to account file
    print("Write to account file")
    account_one.write_account_to_file()
    account_one.print_account()

    # Sell stock
    # Sell stock (dollar_amount)
    print("account_one.sell(ticker=VOO, dollar_amount=40.0)")
    account_one.sell(ticker="VOO", dollar_amount=40.0)
    account_one.print_account()

    # Deposit money
    print("account_one.deposit_money(10000.0)")
    account_one.deposit_money(12300.0)
    account_one.print_account()

    # Load previous account to new account from transaction file
    print("Load from account file")
    account_one.load_from_file()
    account_one.print_account()

    # Deposit money
    print("account_one.deposit_money(10000.0)")
    account_one.deposit_money(123000.0)
    account_one.print_account()

    # Buy another stock
    print("account_one.buy(ticker=QQQ, dollar_amount=500.0)")
    account_one.buy(ticker="QQQ", dollar_amount=500.0)
    account_one.print_account()

    # Withdraw money
    print("account_one.withdraw_money(3000.0)")
    account_one.withdraw_money(3000.0)
    account_one.print_account()

    # Write to account file
    print("Write to account file")
    account_one.write_account_to_file()
    account_one.print_account()

    # Load previous account to new account from transaction file
    print("Load from account file")
    account_one.load_from_file()
    account_one.print_account()

    print("FINAL ACCOUNT")
    account_path = helper_functions.ACCOUNT_LOG_PATH / "account_test2"
    stock_factory = StockFactory("observer")
    #stock_factory = StockFactory("direct")
    account_two = AccountLibrary(account_number=123456, money=1010, account_path=account_path, stock_factory=stock_factory)

    # Load previous account to new account from transaction file
    print("Load from account file")
    account_two.create_new_account()
    account_two.load_from_file()
    account_two.deposit_money(99.0)
    account_two.print_account()


    # Misc commented out sections for manaul debugging if needed
    # ---------------------------------------------------------


    #helper_functions.evaluator_helper(account_one.get_stock("SPXS"))
#
    ## buy two stocks (dollar amount)
    #print("account_one.buy(ticker=SPXS, dollar_amount=100.0)")
    #print("account_one.buy(ticker=TSLA, dollar_amount=10.0)")
    #account_one.buy(ticker="SPXS", dollar_amount=100.0)
    #account_one.buy(ticker="TSLA", dollar_amount=10.0)
    #account_one.print_account()
#
    #helper_functions.evaluator_helper(len(account_one.stocks) == 2)
#
    ## Deposit money
    #print("account_one.deposit_money(10000.0)")
    #account_one.deposit_money(10000.0)
    #account_one.print_account()
    #print("account_one.deposit_money(300.0)")
    #account_one.deposit_money(300.0)
    #account_one.print_account()
#
    #helper_functions.evaluator_helper(account_one.get_account_value() == 11300.0)
#
    ## Withdraw money
    #print("account_one.withdraw_money(3000.0)")
    #account_one.withdraw_money(3000.0)
    #account_one.print_account()
#
    #helper_functions.evaluator_helper(account_one.get_account_value() == 8300.0)
#
    ## Buy new stock (stock amount)
    #print("account_one.buy(ticker=VOO, stock_amount=5.0)")
    #account_one.buy(ticker="VOO", stock_amount=5.0)
    #account_one.print_account()
#
    #helper_functions.evaluator_helper(len(account_one.stocks) == 3)
#
    ## Sell stock (dollar_amount)
    #print("account_one.sell(ticker=VOO, dollar_amount=40.0)")
    #account_one.sell(ticker="VOO", dollar_amount=40.0)
    #account_one.print_account()
#
    ## sell older stock (stock_amount)
    #print("account_one.sell(ticker=SPXS, stock_amount=4.0)")
    #account_one.sell(ticker="SPXS", stock_amount=4.0)
    #account_one.print_account()
#
    ## Withdraw money again
    #print("account_one.withdraw_money(3.2)")
    #account_one.withdraw_money(3.2)
    #account_one.print_account()
#
    #helper_functions.evaluator_helper(account_one.get_account_value() < 8297 and account_one.get_account_value() > 8296)
#
    ## Withdraw money again
    #print("writing account to file")
    #account_one.write_account_to_file()
    #account_one.print_account()
#
    ## NEGATIVE TEST
    ## ------------------
    ## Sell unowned stock
    #print("BEGINNING NEGATIVE TEST")
    #try:
    #    account_one.sell(ticker="AMD", stock_amount=4.0)
    #except AssertionError:
    #    print(" Selling unwoned stock failed correctly")
    #else:
    #    print(helper_functions.evaluator_helper(False))
    #    print("did NOT FAIL correctly")
    #account_one.print_account()
#
    ## Sell Too much stock (stock amount)
    #try:
    #    account_one.sell(ticker="VOO", stock_amount=500.0)
    #except AssertionError:
    #    print(" Selling too much SPXS (stock amount) failed correctly")
    #else:
    #    print(helper_functions.evaluator_helper(False))
    #    print("did NOT FAIL correctly")
    #account_one.print_account()
#
    ## Sell Too much stock (dollar amount)
    #try:
    #    account_one.sell(ticker="SPXS", stock_amount=1000.0)
    #except AssertionError:
    #    print(" Selling too much SPXS (dollar amount) failed correctly")
    #else:
    #    print(helper_functions.evaluator_helper(False))
    #    print("did NOT FAIL correctly")
    #account_one.print_account()
#
    ## Withdraw too much
    #try:
    #    account_one.withdraw_money(10000000.0)
    #except AssertionError:
    #    print(" Withdrawing excess failed correctly")
    #else:
    #    print(helper_functions.evaluator_helper(False))
    #    print("did NOT FAIL correctly")
    #account_one.print_account()
#
    ## Get Buy price of stock that is not bought
    #try:
    #    account_one.get_buy_price("SNAP")
    #except AssertionError:
    #    print(" Getting buy price of stock that hasnt been bought failed correctly")
    #else:
    #    print(helper_functions.evaluator_helper(False))
    #    print("did NOT FAIL correctly")
    #account_one.print_account()
#
    ## Get Buy stock with both stock and dollar amounts filled
    #try:
    #    account_one.buy(ticker="VOO", stock_amount=5.0, dollar_amount=10.0)
    #except AssertionError:
    #    print(" Buying stock with stock and dollar amount filled failed correctly")
    #else:
    #    print(helper_functions.evaluator_helper(False))
    #    print("did NOT FAIL correctly")
    #account_one.print_account()
#
    ## Get Buy stock with both stock and dollar amounts filled
    #try:
    #    account_one.sell(ticker="VOO", stock_amount=5.0, dollar_amount=10.0)
    #except AssertionError:
    #    print(" Buying stock with stock and dollar amount filled failed correctly")
    #else:
    #    print(helper_functions.evaluator_helper(False))
    #    print("did NOT FAIL correctly")
    #account_one.print_account()

    input("press enter to continue")

main()

print("Finsihed!")