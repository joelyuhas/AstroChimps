"""
Light and manual test script for testing the reading functionality.

"""

import sqlite3
import time
import argparse


def get_current_file_name():
    print("get_current_file_name")
    # Get the current year and month
    current_time = time.localtime()
    year = str(current_time.tm_year)
    month = str(current_time.tm_mon).zfill(2)
    print(f'stocks_{year}_{month}.db')
    return f'stocks_{year}_{month}.db'


def read_latest_stock_info(file_name):
    print("read_latest_stock_info")
    # Connect to the database file
    conn = sqlite3.connect(file_name)
    c = conn.cursor()

    # Get the latest stock information
    c.execute("SELECT * FROM stocks ORDER BY timestamp DESC LIMIT 1")
    latest_stock_info = c.fetchone()
    print(latest_stock_info)
    conn.close()

    return latest_stock_info


if __name__ == '__main__':
    #parser = argparse.ArgumentParser(
    #    description='Read the latest stock information every 10 seconds from the SQLite database')
    #parser.add_argument('--file_path', type=str, help='Path to the SQLite database file', required=True)
    #args = parser.parse_args()

    file_name = get_current_file_name()

    while True:
        latest_stock_info = read_latest_stock_info(file_name)
        print(latest_stock_info)
        print(latest_stock_info[2])
        time.sleep(10)
