"""
Author: Joel Yuhas
Date: December 3rd, 2023

Test used to ensure the Stock inheritance is working correctly.

"""
import os
from libraries.StockSubClasses import StockObserver, StockDirect
from libraries import helper_functions



def main():
    os.system('color')

    stock1 = StockObserver(name="QQQ")
    stock1.print_stock()

    stock2 = StockObserver(name="VOO")
    stock2.print_stock()

    stock1 = StockDirect(name="QQQ")
    stock1.print_stock()

    stock2 = StockDirect(name="SPXS")
    stock2.print_stock()

    input("press enter to continue")

main()

print("Finsihed!")