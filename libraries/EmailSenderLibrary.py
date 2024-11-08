"""
Author: Joel Yuhas
Date: October 8th, 2023

EmailSenderLibrary

Library to handle sending emails to target email addresses. This is used to help report results at the end of each
trading day to make it easier to debug and monitor. Can also be used for other means in the future.

Originally used outlook.com mail, but changes to the authentication methods have made it so the program cannot log in
correctly. Have since switched to gmail.


"""
import matplotlib.pyplot as plt
import smtplib
from pathlib import Path

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from libraries.AccountLibrary import AccountLibrary
from libraries.StockFactory import StockFactory


class EmailSenderLibrary:
    def __init__(self, account_paths: list[Path], stock_factory: StockFactory):
        # Receives an array of stock tickers.
        # The code will take care of the rest in terms of the file names!
        # Currently coded to save in the databases/developing databases directories
        self.account_paths = account_paths
        self.stock_factory = stock_factory
        self.sender_email = "XXXXXXXXXXXXXXXXXX"
        self.password = "XXXXXXXXXXXXXXXXXX"
        self.receiver_emails = ['XXXXXXXXXXXXXXXXXX', 'XXXXXXXXXXXXXXXXXX']
        self.smtp_server = 'smtp.gmail.com'
        self.smtp_port = 465
        self.aggregate_list: list = []
        # Call the aggregate_accounts so aggregate list can be utilized
        self._aggregate_accounts()

    def _aggregate_accounts(self):
        """
        Take the list of account paths, use them to create a list of loaded accounts from it that can be used to
        use the information with.

        TODO: May make sense in the future to have a completely separate class for "data analysis" that aggregates
        accounts and does more.

        """
        # Get the account path from individual lists
        for account_path in self.account_paths:
            # The next sections scan the path for files named "account" and then will automatically get the account
            # number from the file so it can be loaded into the account Class and then printed
            for file in account_path.iterdir():
                if file.is_file() and file.name.startswith('account'):
                    filename = file.stem
                    number = filename.split('_')[1]
                    tmp_account = AccountLibrary(stock_factory=self.stock_factory,
                                                 account_number=int(number),
                                                 account_path=account_path)
                    # Load the account
                    tmp_account.load_from_file()
                    # be sure to get the updated values or else it will pull the old values!!
                    tmp_account.update_stock_values_all()
                    self.aggregate_list.append(tmp_account)

    def string_aggregate_accounts(self) -> str:
        """
        Return a string of all the aggregate account information for email sending

        :return: (str) : String of all aggregate account info

        """
        # Update all the values before putting in the string
        for item in self.aggregate_list:
            item.update_stock_values_all()
        # Add detailed list
        my_list = [str(item.print_account()) for item in self.aggregate_list]
        list_string = '\n'.join(my_list)
        # Add condensed, changes list
        list_string = "\n" + list_string
        my_list = [str(self.run_statistics(item)) for item in self.aggregate_list]
        list_string = '\n'.join(my_list) + list_string
        list_string = "\n" + list_string
        list_string = "Have a great afternoon! \n" + list_string

        return str(list_string)

    def send_email(self, subject: str, body: str, image_attachments: list):
        """
        Method to consolidate and send the email. Receives the subject, body, and images to attach.

        :param subject: (str): the Subject line of ht email
        :param body: (str): The body of the email to
        :param image_attachments: (list): Any attached images. Current case is to send plotted data as well.

        """
        msg = MIMEMultipart()
        msg['From'] = self.sender_email
        msg['To'] = ', '.join(self.receiver_emails)
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        # Add any image attachments
        counter = 0
        for attachment in image_attachments:
            with open(attachment, 'rb') as file:
                attachment = MIMEImage(file.read(), name=f'trend_plot{counter}.png')  # Change the name as needed
            msg.attach(attachment)
            counter = counter + 1

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(self.sender_email, self.password)
            smtp.sendmail(self.sender_email, self.receiver_emails, msg.as_string())
        print("Message sent!")

    @staticmethod
    def print_difference_helper(list_string: str, today_value: float, compare_value: float, category: str = "") -> str:
        """
        Helper function that prints the price different from end of day value of stock yesterday to today. Useful for
        reporting information in the email.

        :param list_string: (str): The main string to send that has values concatenated to it.
        :param today_value: (float): The current value of the stock
        :param compare_value: (float): The value to compare the current value with. Typically, the previous EOD value
        :param category: (str): Any descriptive category to add to the string
        :return: (str): The final string with all different values in both monetary and percent difference.

        """
        difference = today_value - compare_value
        # Check for 0 edge case
        if compare_value != 0:
            percentage = (difference / compare_value) * 100
        else:
            percentage = 999

        # Depending on if its positive or negative, change the output formatting
        if difference >= 0:
            list_string = list_string + f"{category}| +${round(difference,2)}, +{round(percentage,2)}%  |"
        else:
            list_string = list_string + f"{category}| -${round(abs(difference),2)}, -{round(abs(percentage),2)}%  |"

        return list_string

    def run_statistics(self, input_account: AccountLibrary) -> str:
        """
        Run and collect the desired values to put into the email. Specifically the previous values, differences with
        current values, today's values, and more.

        :param input_account: (AccountLibrary): The account for which to get the statistics from
        :return: (str): The string with all the added statistics of the account in string format.

        """
        # Get the current value
        today_value = float(input_account.get_account_value())

        # Get the value from yesterday

        yesterday_value = float(input_account.get_previous_end_of_day_total_value(1)[0])

        # Get the value from last week (5 days)
        last_week_value = float(input_account.get_previous_end_of_day_total_value(5)[0])

        # return string with account value differences
        list_string = f"Account {input_account.account_number}: ${round(today_value,2)} "
        list_string = self.print_difference_helper(list_string, today_value, yesterday_value, )
        list_string = list_string + str(input_account.get_previous_end_of_day_total_value(1)[1])
        list_string = self.print_difference_helper(list_string, today_value, last_week_value, )
        list_string = list_string + str(input_account.get_previous_end_of_day_total_value(5)[1])
        list_string = list_string + "\n"

        return list_string

    @staticmethod
    def plot_trend(account: AccountLibrary, window_size: int = 5):
        """
        Method to plot the values on a graph. Saves the figure to specific path and generates image.

        TODO: May include this in a new "DataAnalysis" class or something similar going forward so we can use this on

        :param account: (AccountLibrary): The account for which to get the statistics from
        :param window_size: (int): Size of the window for the plot

        """
        # fetch all the correct values from the previous days and compile into list
        total_values = []
        for i in range(0, window_size):
            total_values.insert(0, account.get_previous_end_of_day_total_value(int(i))[0])

        # Create a line graph
        plt.plot(total_values, marker='o', linestyle='-', color='b', label='Total Value Trend')

        # Add labels and title
        plt.xlabel('Past Entries')
        plt.ylabel('Total Value')
        plt.title(f'ACCOUNT: {account.account_number} Total Value Trend Over the Last 5 Entries')

        # Show legend
        plt.legend()

        # Display the graph
        plt.savefig(account.account_parent_path / (str(account.account_number) + "_image.jpg"))
        plt.clf()

    def generate_plot_attachments(self) -> list:
        """
        Generate the plot attachments for all the accounts being reported on.

        :return: (list): The list of the attachment paths for the plots that have been generated

        """
        attachment_paths = []
        for account in self.aggregate_list:
            self.plot_trend(account)
            attachment_paths.append(account.account_parent_path / (str(account.account_number) + "_image.jpg"))

        return attachment_paths

    def test_info_sender(self):
        """
        Test method for generating plots

        """
        # Get the account path from individual lists
        for account in self.aggregate_list:
            self.plot_trend(account)
