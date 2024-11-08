"""
Author: Joel Yuhas
Date: November 15th, 2023

Program that handles sending the email using the existing infrastructure

"""
import time

from libraries.StockFactory import StockFactory
from libraries.EmailSenderLibrary import EmailSenderLibrary
from libraries.helper_functions import ACCOUNT_LOG_PATH, is_trade_hours, pause_until_trade_hours_start, \
    pause_until_trade_hours_end
from datetime import datetime


# Initialize the EmailSenderLibrary
account_paths = [ACCOUNT_LOG_PATH / "account_program_04_TQQQ", ACCOUNT_LOG_PATH / "account_program_04_QQQ"]
stock_factory = StockFactory("observer")
current_date = datetime.now().strftime("%Y,%m,%d")
email_sender = EmailSenderLibrary(account_paths=account_paths,
                                  stock_factory=stock_factory)

# Debugging portion
# stock_factory = StockFactory("observer")
# email_sender.send_email(f"{current_date} stocks",email_sender.string_aggregate_accounts(),email_sender.generate_plot_attachmetns())
# print("Sending Email!")

while True:
    # Pause until trade time is done, then send email. This way it only sends email on trading day
    if is_trade_hours():
        pause_until_trade_hours_end()

        email_sender.send_email(f"{current_date} stocks",
                                email_sender.string_aggregate_accounts(),
                                email_sender.generate_plot_attachments())
        print("Sending Email!")

    else:
        pause_until_trade_hours_start()
        print("Waiting until trade hours start")
