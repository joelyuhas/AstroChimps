"""
Author: Joel Yuhas
Date: July 8th, 2023

Class AccountLibrary:

This class stores all of a user's information and account data. This will store how many stocks the user has, amount of
money, transactions, and more. This is intended to be the "head" of a users experience and link together all the
pertinent account information.

NOTE: Transaction and account file are used to save transaction and account data for later on


"""
import os.path
import json
import csv
import time
import pandas as pd

from datetime import datetime
from typing import Optional, Dict
from pathlib import Path
from libraries.StockBaseClass import StockBaseClass
from libraries.StockFactory import StockFactory
from libraries.Transaction import Transaction

# Constant to show account fields and their names
ACCOUNT_FIELDNAMES = ["date", "account_dict", "total_value", "end_of_day_save"]


class AccountLibrary:
    def __init__(self, account_number: int, stock_factory: StockFactory, account_path: Path, money: float = None,
                 stocks: Optional[Dict[str, StockBaseClass]] = None, transactions: list = None):
        self.account_number = account_number
        self.money = money if money is not None else 0.0
        self.stocks = stocks if stocks is not None else {}
        self.transactions = transactions if transactions is not None else []
        self.account_parent_path = account_path
        self.stock_factory = stock_factory
        self.transaction_file = self.account_parent_path / f"transaction_{account_number}.txt"
        self.account_file = self.account_parent_path / f"account_{account_number}.csv"

        # Generate the account on instantiation of the class
        self.create_new_account()

    def create_new_account(self) -> bool:
        """
        Create a new account with new directory, account file, and transaction file

        :return: (bool): Return True if new account was created, false if it already existed.

        """
        # Initialization sections, if directory does not exist, make it
        if not self.account_parent_path.is_dir():
            print("Account path does not exist, initializing")
            self.account_parent_path.mkdir(parents=True)
        else:
            print("Provided with already existing account path")

        # if the files do not exist, in the directory, or on their own then create them
        if not self.transaction_file.is_file():
            print("Creating transaction file")
            self.transaction_file.touch()
        if not self.account_file.is_file():
            print("Writing new account data")
            self.write_account_to_file()

            # if at this point, account file did not exist, return true for creating account
            return True

        else:
            print("Account already exists and has values in it")
            return False

    def get_account_value(self) -> float:
        """
        Get the total monetary value of the account by doing the following
        - Get the current money balance of the account
        - Add the total values of all stocks in account
        - Report final float value

        :return: (float): Total account value including balance and all stocks at time it is run.

        """
        total_value = self.money
        for stock in self.stocks.values():
            total_value += float(stock.total_value())
        return total_value

    def get_account_file_info(self) -> list:
        """
        Return the account_file information in full.

        :return: (list): List of DictReader of the account file info
        """
        with open(self.account_file, 'r') as file:
            reader = csv.DictReader(file)
            data = list(reader)
        return data

    def get_previous_end_of_day_total_value(self, days_back: int = 1, try_multiple_attempts: bool = False) -> (
            tuple)[float, datetime]:
        """
        Get the previous account total value from however many days back from before. Ensures it is actually grabbing
        previouse day values as well, as there can be multiple csv rows per day. Added in logic to ensure it will
        gather latest info from a previous day and not just the last save

        NOTE: currently working in progress on this, debate between if we want it to always get the last value in the
        account csv as the "current value" or if the time this is being ran really is the total value.

        Been having issues with going off of the last save since sometimes a save hasn't been done yet, so it reports
        yesterday's values.

        :param days_back: (int): How many days back should the last end of day value be gathered
        :param try_multiple_attempts: (bool): If the method runs into an error trying to get last value, skip that value
                                                and try again
        :return: tuple(float,datetime) The float of the total value from the day before as well as the datetime from
                                        where it got it

        """
        # Read the CVS file with account info
        data = self.get_account_file_info()

        # Attempt to get the previous days back values.
        try:
            # Get the current datetime
            current_datetime = datetime.now()
            current_date = current_datetime.strftime("%Y-%m-%d %H:%M:%S.%f")
            parsed_datetime = datetime.strptime(current_date, "%Y-%m-%d %H:%M:%S.%f")

            # Loop through entries until one is found that has a time difference greater than specified amount
            row_delta = 1
            while True:
                potential_date = datetime.strptime(data[-(days_back + row_delta)][ACCOUNT_FIELDNAMES[0]],
                                                   "%Y-%m-%d %H:%M:%S.%f")
                days_difference = abs(parsed_datetime - potential_date).total_seconds() / (24 * 3600)

                # Ensure days back is satisfied and it is an end of day save
                # Subtract just a bit since it might not be exactly 24 horus since the last save at 4pm
                if days_difference > (days_back - 0.1) and potential_date.hour == 16:
                    return round(float(data[-(days_back + row_delta)][ACCOUNT_FIELDNAMES[2]]), 2), potential_date
                else:
                    row_delta = row_delta + 1

                # Safety break check to exit loop if needed
                if row_delta > 1000:
                    print("Looping way too long")
                    raise AssertionError

        except KeyError:
            print("Total Value most likely not in this account file, adding")
            self.check_and_fix_account_file_formatting()
            # Sleep 1 seconds for the file to update and then run again
            time.sleep(1)
            if not try_multiple_attempts:
                self.get_previous_end_of_day_total_value(days_back=days_back, try_multiple_attempts=True)
            else:
                raise KeyError

    def print_account(self) -> list[str]:
        """
        Prints out basic account information to console and also returns same information as a list of strings.

        Values in the account:
            - account number
            - stocks
            - quantity
            - transactions
            - liquid money
            - transaction file
            - account file

        :return: (list): List of strings with all the correct stock information

        """
        account_number = f"   account_number :{self.account_number}"
        cash = f": Cash ${round(self.money, 2)}"
        total_value = f": Total Value ${round(self.get_account_value(), 2)}"
        number_of_transactions = f" #transactions : {len(self.transactions)}"

        aggregate_list = [account_number,
                          cash,
                          total_value,
                          number_of_transactions]

        accumulated_stock_quantity = 0
        for stock in self.stocks.values():
            aggregate_list.append(stock.print_stock())
            accumulated_stock_quantity += stock.quantity
        print("\n")

        print("--ACCOUNT PRINT--")
        for item in aggregate_list:
            print(item)
            pass

        return aggregate_list

    def print_account_verbose(self):
        """
        Prints out more detailed account information. Used primarily for debugging.

        """
        print("--ACCOUNT PRINT--")
        print(f"   account_number   : {self.account_number}")
        print(f"   money            : {self.money}")
        print(f"   transaction_file : {self.transaction_file}")
        print(f"   account_file     : {self.account_file}")
        print(f"   # of stocks      : {len(self.stocks)}")
        print(f"   # of trans       : {len(self.transactions)}")

        for stock in self.stocks.values():
            stock.print_stock()

        for transaction in self.transactions:
            transaction.print_transaction()

        print("\n")

    def account_to_dict(self) -> dict:
        """
        Turn an account object's information into a dictionary so it can be saved to files and organized more
        easily.

        :return: (dict): Dictionary of all account information saved with their respective data types.

        """
        account_dict = {'account_number': self.account_number,
                        'money': self.money,
                        'account_path': str(self.account_parent_path),
                        'transaction_file': str(self.transaction_file),
                        'account_file': str(self.account_file),
                        'stocks': [],
                        }
        # Turn all stocks into dicts
        for stock in self.stocks.values():
            account_dict['stocks'].append(StockBaseClass.stock_to_dict(stock))
        return account_dict

    def account_from_dict(self, account_dict: dict):
        """
        Turn a saved account dictionary into an account object. This way it can be loaded from database and text
        files easily.

        :param account_dict: (dict) Dictionary with all the account information to save to account object

        """
        print("LOADING FROM THE FILES!!")
        self.account_number = account_dict['account_number']
        self.money = account_dict['money']
        self.transaction_file = Path(account_dict['transaction_file'])
        self.account_file = self.account_parent_path / f"account_{self.account_number}.csv"
        self.account_parent_path = self.account_parent_path
        for stock_dict in account_dict['stocks']:
            stock_to_add = self.stock_factory.dict_to_stock(stock_dict)
            self.stocks[stock_to_add.name] = stock_to_add
        self.print_account()

    def check_and_fix_account_file_formatting(self):
        """
        Check to ensure the file formatting of the account file is up-to-date. If not, update it.
        - If the file is missing any headers, add them
        - If the file is missing any columns of data, back-fill them with 0's

        """
        # Check if the file exists, if not make it
        file_exists = os.path.isfile(self.account_file)

        if file_exists:
            # Open the file and read out the field names to check formatting. If formatting incorrect, rewrite it
            with open(self.account_file, "r", newline="") as csvfile:
                # check the formatting of the file
                reader = csv.DictReader(csvfile)
                header = reader.fieldnames
                # Check the formatting
                missing_columns = []
                for fields in ACCOUNT_FIELDNAMES:
                    if fields not in header:
                        missing_columns.append(fields)

            # If any of the headers are incorrect, then reformat them in their entirety
            if len(missing_columns) > 0:
                # Read the existing CSV file into a DataFrame
                df = pd.read_csv(self.account_file, header=None, skiprows=1)

                # If there are 3 columns of data, just update the header, keep data same
                if df.shape[1] == len(ACCOUNT_FIELDNAMES):
                    df.columns = ACCOUNT_FIELDNAMES
                # If there are less columns than expected, (missing data column) add them with 0's
                elif df.shape[1] < len(ACCOUNT_FIELDNAMES):
                    df[missing_columns] = 0
                    df.columns = ACCOUNT_FIELDNAMES

                # Save the entire DataFrame with correct columns, back to the CSV file
                df.to_csv(self.account_file, index=False)

        # If the file doesn't exist, write the header
        else:
            with open(self.account_file, "a", newline="") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=ACCOUNT_FIELDNAMES)
                writer.writeheader()

    def write_account_to_file(self, end_of_day_save: bool = False):
        """
        Write the desired Account to the given account file (different file for every account).

        Specifically, save into a csv file, first column being the date, second column being the "account_dict" which
        has all the pertinent account information.

        :end_of_day_save: (bool): If this save is the final save of the day. Useful for retrieving retroactive data

        """
        # Check the formatting of the account file is correct
        self.check_and_fix_account_file_formatting()

        # Create data variable in correct format to save for later
        #   0 is date
        #   1 is info
        #   2 is total value
        data = {
            ACCOUNT_FIELDNAMES[0]: str(datetime.today()),
            ACCOUNT_FIELDNAMES[1]: json.dumps(self.account_to_dict()),
            ACCOUNT_FIELDNAMES[2]: str(self.get_account_value()),
            ACCOUNT_FIELDNAMES[3]: str(end_of_day_save)
        }

        # Open account and write to it
        with open(self.account_file, "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=ACCOUNT_FIELDNAMES)
            writer.writerow(data)

    def load_from_file(self):
        """
        Reads from the specified account file and populates all required fields. Gets the account file by searching for
        the account file name using the account number.

        """
        with open(self.account_file, "r") as csvfile:
            reader = csv.DictReader(csvfile)

            # Convert the rows into a list and extract the last row
            rows = list(reader)
            last_row = rows[-1]
            self.account_from_dict(json.loads(last_row["account_dict"]))

    def deposit_money(self, deposit_amount: float):
        """
        Deposit the desired amount of money into the account balance.

        :param deposit_amount: (float): The desired amount of money to be deposited

        """
        desired_transaction = Transaction(account=self,
                                          dollar_amount=deposit_amount,
                                          transaction_file=self.transaction_file,
                                          account_file=self.account_file)
        # Perform the deposit
        desired_transaction.deposit()

    def withdraw_money(self, withdrawal_amount: float):
        """
        Withdraw money from account.

        :param withdrawal_amount: (float): the amount to be withdrawn

        """
        desired_transaction = Transaction(account=self,
                                          dollar_amount=withdrawal_amount,
                                          transaction_file=self.transaction_file,
                                          account_file=self.account_file)
        # Perform the deposit
        desired_transaction.withdraw()

    def buy(self, ticker: str, dollar_amount: float = 0.0, stock_amount: float = 0.0):
        """
        Buy the desired stock.

        NOTE: Only one of dollar_amount or stock_amount needs to be populated. The function will calculate whichever
        value is not provided. Both of these params are included so the option to buy using either method is available.

        :param ticker: (str): Ticker of the stock.
        :param dollar_amount: (float): The to purchase in dollars.
        :param stock_amount: (float): The amount to purchase in number of respective stocks.

        """
        # Create transaction data structure
        desired_transaction = Transaction(account=self,
                                          ticker=ticker,
                                          stock=self.get_stock(ticker),
                                          stock_amount=stock_amount,
                                          dollar_amount=dollar_amount,
                                          transaction_file=self.transaction_file,
                                          account_file=self.account_file)
        # perform the transaction
        desired_transaction.buy()

    def sell(self, ticker: str, dollar_amount: float = 0.0, stock_amount: float = 0.0):
        """
        Sell stocks

        NOTE: Only one of dollar_amount or stock_amount needs to be populated. The function will calculate whichever
        value is not provided. Both of these params are included so the option to buy using either method is available.

        :param ticker: (str): The ticker of the stock
        :param dollar_amount: (float): The to purchase in dollars.
        :param stock_amount: (float): The amount to purchase in number of respective stocks.

        """
        # Create transaction data structure
        desired_transaction = Transaction(account=self,
                                          ticker=ticker,
                                          stock=self.get_stock(ticker),
                                          stock_amount=stock_amount,
                                          dollar_amount=dollar_amount,
                                          transaction_file=self.transaction_file,
                                          account_file=self.account_file)
        # perform the transaction
        desired_transaction.sell()

    def get_buy_price(self, ticker: str) -> float:
        """
        Get the current price of the stock.

        :ticker: (str): The ticker of the stock to get the buy price from in the account
        :return: (float): The current price of the stock

        """
        return self.stocks[ticker].buy_price

    def get_stock(self, ticker: str) -> StockBaseClass:
        """
        Returns the stock object from desired stock name, if no stock currently exists, create a blank StockBaseClass.

        :param ticker: (str): Ticker of the desired stock
        :return: (StockBaseClass): Returns stock object with ticker, if not found, creates new one

        """
        if ticker not in self.stocks:
            return self.stock_factory.create_stock(ticker)

        return self.stocks[ticker]

    def update_stock_values_all(self):
        """
        Update all peaks, trends, and prices, and values using the specified stock's methods.

        """
        for stock in self.stocks:
            self.stocks[stock].update_stock_values()
