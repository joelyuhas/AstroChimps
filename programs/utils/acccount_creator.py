"""

Basic utility to auto generate an account using the existing infrastructure.

"""

import argparse
from libraries.AccountLibrary import AccountLibrary

WAIT_INTERVAL_SECONDS = 10


# need to make this dynamic
def arg_parser():
    """
    Get following information so the program can run
    - desired stock ticker
    - transaction file save location
    - account file save location

    """
    # NOTE will need to update this to have more than 2 eventually
    parser = argparse.ArgumentParser()
    parser.add_argument("accocunt_number", type=str, help="The account number for this accountt")
    parser.add_argument("inital_money", type=str, help="The inital money to start with in int format")
    parser.add_argument("account_path", type=str, help="Directory for account ot live at")

    return parser.parse_args()



def main(args):
    account = AccountLibrary(account_number=args.accocunt_number, money=args.inital_money,
                             account_path=args.account_parent_path)
    account.create_new_account()


args = arg_parser()
main(args)