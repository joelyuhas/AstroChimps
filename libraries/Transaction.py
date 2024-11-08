"""
Author: Joel Yuhas
Date: November 11th, 2021

Class Transaction:

This class is used to execute and store transaction data. A class was decided to store and manipulate this information
instead of directly writing the information to a file so that transaction data could be readily available and easier
to store, access, reproduce, and update as time goes on.

Having this information in a class makes storing and keeping the transaction data much easier which will be important
for data analysis.

        self.transaction_number     : (int)     The number of the account int
        self.account                : (int)     The account class along with all account information
        self.ticker                 : (st)      Ticker that is used to identify and retrieve the stock
        self.type                   : (str)     Type of transaction: DEPOSIT, WITHDRAW, BUY, SELL
        self.stock_amount           : (float)   The number of stocks that wish to be bought or sold
        self.dollar_amount          : (float)   The dollar value of stock that wishes to be bought or sold
        self.stock_price            : (float)   The updated price of the stock
        self.transaction_file       : (str)     Directory to transaction file
        self.account_file           : (str)     Director to account file

NOTE: Only one of the stock_amount or dollar_amount is needed as the class will calculate the whichever isnt given using
      the current stock price. This is done because to know both at the same time, the current stock price is needed
NOTE: Transaction and account file are used ot save transaction and account data for later on

"""

from datetime import datetime


class Transaction:
    def __init__(self, account=None, ticker=None, stock=None, stock_amount=0.0, dollar_amount=0.0, transaction_file=None,
                 account_file=None, error=""):
        self.transaction_number = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
        self.account = account
        self.ticker = ticker
        self.type = None
        self.stock_amount = stock_amount # only populate one of either stock amount or dollar amount
        self.dollar_amount = dollar_amount
        self.stock = stock
        if self.ticker is not None:
            self.stock_price = float(stock.get_current_price(ticker))
        self.transaction_file = transaction_file
        self.account_file = account_file
        self.error = error

    def write_transaction_to_file(self):
        """
        write the desired transaction to the given transaction file.

        """
        file = open(self.transaction_file, "a")

        # check if error message:
        if self.error:
            file.write(str(datetime.today().strftime('%Y-%m-%d-%H:%M:%S')) + " account: " +
                       str(self.account.account_number) + " : " +
                       str(self.error) + '\n')
        else:
            if self.type == "DEPOSIT":
                file.write(str(datetime.today().strftime('%Y-%m-%d-%H:%M:%S')) + " account: " +
                           str(self.account.account_number) + " : " +
                           self.type + "  -> " +
                           str(self.dollar_amount) + " total: " +
                           str(self.account.money) + '\n')

            elif self.type == "WITHDRAW":
                file.write(str(datetime.today().strftime('%Y-%m-%d-%H:%M:%S'))  + " account: " +
                           str(self.account.account_number) + " : " +
                           self.type + " -> " +
                           str(self.dollar_amount) + " total: " +
                           str(self.account.money) + '\n')
            else:
                file.write(str(datetime.today().strftime('%Y-%m-%d-%H:%M:%S'))  + " account: " +
                           str(self.account.account_number) + " : " +
                           self.type + "      -> " +
                           str(self.stock_amount) + " " +
                           str(self.ticker) + " at $" +
                           str(self.stock_price) + " total: $" +
                           str(self.stock_amount * self.stock_price ) + ' balance: ' +
                           str(self.account.money) + '\n')
        file.close()

    def deposit(self):
        """
        Deposit money into the account. Record it in the transaction file and add it to the account class.

        """
        self.type = "DEPOSIT"
        self.account.money += self.dollar_amount
        self.write_transaction_to_file()
        self.account.transactions.append(self)

    def withdraw(self):
        """
        Withdraw money from the account. Record it in the transaction file and add it to the account class.

        """
        self.type = "WITHDRAW"
        if self.account.money > self.dollar_amount:
            self.account.money -= self.dollar_amount
            self.write_transaction_to_file()
            self.account.transactions.append(self)
        else:
            print("ERROR: Not enough money to withdraw! Attempted to withdraw [%s], only [%s] available",
                  self.dollar_amount, self.account.money)
            self.error = (f"ERROR#1: Not-enough-funds-to-withdraw: Funds {self.account.money} Request "
                          f"{self.dollar_amount}")
            self.write_transaction_to_file()
            raise AssertionError

    def buy(self):
        """
        Buy the desired stock.
            - Populate the stock_amount if the dollar_amount isnt given and vice versa
            - Ensure there is enough money in the account to purchase the desired amount of stock
            - Check if the stock ticker already exist inside the account, if not add it
            - Record and save transaction to file and into account object

        """
        self.type = "BUY"
        # Calibrate stock and dollar amount

        if self.stock_amount != 0.0 and self.dollar_amount != 0.0:
            # stock amount and dollar amount were filled with potentially conflicting info
            print("ERROR: stock amount and dollar amount were both given values, only one value should be populated")
            print(f"stock amount = {self.stock_amount}")
            print(f"dollar amount = {self.dollar_amount}")
            raise AssertionError
        elif self.stock_amount != 0.0:
            self.dollar_amount = self.stock_amount * self.stock_price
        else:
            self.stock_amount = self.dollar_amount / self.stock_price

        # Check if transaction can be made/have enough money to buy required amount
        if self.dollar_amount > self.account.money:
            print("Error: Not enough money, attempted to buy [%s] amount of stock, only have [%s] funds available",
                  self.dollar_amount, self.account.money)
            self.error = f"ERROR#2: Not-enough-funds-to-buy {self.ticker}: Funds {self.account.money} " \
                         f"Request: {self.dollar_amount}"
            self.write_transaction_to_file()
            raise AssertionError

        else:
            # Transaction good to go!
            self.account.money -= self.dollar_amount
            # check if stock is already owned
            if self.ticker in self.account.stocks:
                self.account.stocks[self.ticker].quantity += self.stock_amount
                self.account.stocks[self.ticker].last_price = self.stock_price
            else:
                self.stock.quantity = self.stock_amount
                self.stock.buy_price = self.stock_price
                self.stock.new_high = self.stock_price
                self.stock.last_price = self.stock_price
                self.account.stocks[self.ticker] = self.stock

            self.write_transaction_to_file()
            self.account.transactions.append(self)

    def sell(self):
        """
        Sell the desired stock.
            - Populate the stock_amount if the dollar_amount isnt given and vice versa
            - Ensure there is enough stock in the account to sell desired amount
                NOTE: stock wil currently NOT be removed from list if quantity goes to 0
            - Check if the stock ticker already exist inside the account, if not raise an error
            - Record and save transaction to file and into account object

        """
        self.type = "SELL"
        # Calibrate stock and dollar amount
        if self.stock_amount != 0.0 and self.dollar_amount != 0.0:
            # stock amount and dollar amount were filled with potentially conflicting info
            print("ERROR: stock amount and dollar amount were both given values, only one value should be populated")
            raise AssertionError  # Potentially remove errors later so program can keep running
        elif self.stock_amount != 0.0:
            self.dollar_amount = self.stock_amount * self.stock_price
        else:
            self.stock_amount = self.dollar_amount / self.stock_price

        # check if have stock
        if self.ticker not in self.account.stocks:
            print("ERROR: Stock", self.ticker, " is not owned")
            self.error = f"ERROR#3: Stock {self.ticker} not-owned"
            self.write_transaction_to_file()
            raise AssertionError # Potentially remove errors later so program can keep running
        else:
            # Check if transaction can be made
            if self.account.stocks[self.ticker].quantity < self.stock_amount:
                print("ERROR: Not enough stock, [%s] stocks available, [%s] attempted to be removed",
                      self.account.stocks[self.ticker].quantity, self.stock_amount)
                self.error = f"ERROR#4: Not-enough-stock {self.ticker} to-sell, Have: {self.account.stocks[self.ticker].quantity}, " \
                             f"Requested {self.stock_amount}"
                self.write_transaction_to_file()
                raise AssertionError # Potentially remove errors later so program can keep running

            else:
                # Transaction good to go!
                self.account.money += self.dollar_amount
                self.account.stocks[self.ticker].quantity -= self.stock_amount
                self.account.stocks[self.ticker].last_price = self.stock_price
                self.account.stocks[self.ticker].sell_price = self.stock_price
                self.account.stocks[self.ticker].new_low = self.stock_price
                self.write_transaction_to_file()
                self.account.transactions.append(self)

    def print_transaction(self):
        """
        Print the transaction object, usefull for debugging, two different methods depending on if deposit/ withdraw vs
        buy/sell

        """
        if self.type == "DEPOSIT" or "WITHDRAW":
            print("TRANSACTION  PRINT**")
            print(f"   transaction_number   :  {self.transaction_number}")
            print(f"   account_number       :  {self.account.account_number}")
            print(f"   type                 :  {self.type}")
            print(f"   dollar_amount        :  {self.dollar_amount}")
            print(f"   transaction_file     :  {self.transaction_file}")
            print(f"   account_file         :  {self.account_file}")

        else:
            print("TRANSACTION  PRINT**")
            print(f"   transaction_number   :  {self.transaction_number}")
            print(f"   account_number       :  {self.account.account_number}")
            print(f"   ticker               :  {self.ticker}")
            print(f"   type                 :  {self.type}")
            print(f"   stock_amount         :  {self.stock_amount}")
            print(f"   dollar_amount        :  {self.dollar_amount}")
            print(f"   stock_price          :  {self.stock_price}")
            print(f"   transaction_file     :  {self.transaction_file}")
            print(f"   account_file         :  {self.account_file}")