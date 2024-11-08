"""
Author: Joel Yuhas
Date: December 1st, 2021

Testing the sqlite plot printing features.

"""
import os
from libraries.AccountLibrary import AccountLibrary
from libraries.StockFactory import StockFactory
from libraries.StockSubClasses import StockObserver
from libraries import helper_functions

import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

from libraries.helper_functions import OBSERVER_DATABASE_PATH
from libraries.StockBaseClass import StockBaseClass

def main():
    # Connect to SQLite database
    #stock_factory = StockFactory("observer")
    print("OVEOREO")
    print(StockObserver.get_current_file_name("QQQ"))
    conn = sqlite3.connect(StockObserver.get_current_file_name("QQQ"))  # Replace 'your_database.db' with your actual database file

    # Replace 'your_table' with the actual name of your table
    query = "SELECT * FROM stocks WHERE timestamp LIKE '2023-12-05%'"
    df = pd.read_sql_query(query, conn)

    # Close the database connection
    conn.close()

    # Convert the timestamp column to datetime format
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # Plot the data
    plt.figure(figsize=(10, 6))
    plt.plot(df['timestamp'], df['price'], marker='o')
    plt.title('Stock Movement on 2023-01-01')
    plt.xlabel('Timestamp')
    plt.ylabel('Stock Price')
    plt.grid(True)
    plt.show()

main()

print("Finsihed!")