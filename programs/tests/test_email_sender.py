""""
NOTE
Quick prototyping project for sending emails, will look into this more later and what not too

"""


from libraries.StockFactory import StockFactory
from libraries.EmailSenderLibrary import EmailSenderLibrary
from libraries.helper_functions import ACCOUNT_LOG_PATH
from datetime import datetime


# Initialize the EmailSenderLibrary
account_paths = [ACCOUNT_LOG_PATH / "account_program_04_TQQQ", ACCOUNT_LOG_PATH / "account_program_04_QQQ"]
#account_paths = [ACCOUNT_LOG_PATH / "account_test"]
stock_factory = StockFactory("direct")
current_date = datetime.now().strftime("%Y,%m,%d")
email_sender = EmailSenderLibrary(account_paths=account_paths,
                                  stock_factory=stock_factory)

# Debugging portion
stock_factory = StockFactory("direct")

output = email_sender.string_aggregate_accounts()
plots = email_sender.generate_plot_attachments()
email_sender.send_email(f"{current_date} stocks",
                                output,
                                plots)
print(output)
