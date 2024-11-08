"""
Author: Joel Yuhas
Date: July 8th, 2023

Main program file that starts all needed programs and threads to start the stock process.

Currently set to run:
- Stock programs with different parameters and different stocks
- Observer pattern to collect stock info and store in Sqlite database
- Send email at end of day

"""

import subprocess
from libraries.helper_functions import PROGRAM_PATH, BIN_PATH, OBSERVER_PATH, EMAIL_REPORTING_PATH


def run_program_04(account_number: int, ticker: str, loss_threshold: float, gain_threshold: float):
    """
    Method used to run program_04 along with its parameters.

    :param account_number: (int): The identification number of the account to run against
    :param ticker: (str): The ticker for the stock that is desired to trade
    :param loss_threshold: (int): The threshold to sell a stock if surpassed
    :param gain_threshold: (int): The threshold to buy the stock if surpassed

    """
    cmd = f"python {PROGRAM_PATH}/program_04.py {account_number} {ticker} {loss_threshold} {gain_threshold}"
    subprocess.Popen(cmd, shell=True)


def run_email_generator():
    """
    Basic helper method to run the email generation.

    """
    cmd = f"python {EMAIL_REPORTING_PATH}/email_sender.py "
    subprocess.Popen(cmd, shell=True)


if __name__ == "__main__":
    # Kick off the observer pattern that intakes list of stocks
    observer_path = OBSERVER_PATH / "observer_pattern.py"
    stocks_to_intake_path = BIN_PATH / "list_of_stocks.txt"
    subprocess.Popen(f"python {observer_path} {stocks_to_intake_path}", shell=True)

    # Get list of stocks to trade and put them into stock list
    stock_list=[]
    with open(stocks_to_intake_path, 'r') as file:
        for line in file:
            print(line.rstrip())
            stock_list.append(line.rstrip())

    # Start the trading program for each stock and each interval
    for stock in stock_list:
        for i in range(1, 3):
            run_program_04(i, stock, float(i), float(i))

        # Custom Initializations
        run_program_04(505, stock, 0.5, 0.5)
        run_program_04(5, stock, float(5), float(5))

    # Run the email sender program
    run_email_generator()


