# AstroChimps
Hobby stock trading project using python, sqlite, and automation. This project creates its own account classes and transaction infrastructure, pulls in real time stock data using yfinance, and executes several trading algorithms. It runs on its own "testrunner" computer running Linux that automatically turns on Mon-Fri before trading hours, and turns itself off afterwards.

At the end of the trading day, an email with the algorithms daily and weekly results is sent to my personal email, along with graphs of the weekly performance compared to SPY.

Separate programs save specific stock data to custom databases as well so they can be used to back test new algorithms in the future.

Several software development principals were experimented with this project and it also has provided a great opportunity to work with databases, automation, and real time trading.

This project has been under work on and off for several years and has been a fun hobby project to come back to update and try out new coding techniques.

More detailed documentation and reports coming soon.

## Objective
There were a few objectives to this project that focused on learning experiences, the main objectives being:
- Create a project that follows a topic that has a significant amount of resources and similar support for (stock trading in this case) so that personal implementations could be compared to other implementations for learning opportunities.
- Have a problem that could be experimented with in different ways (trade algorithms) to continue to practice software development strategies and continue to learn new techniques. 
- Have a continuous project that could run automatically for set intervals during the week to practice continuous automation.
- Have a project that could be used to practice designing maintainable code, and come back to it periodically to ensure its easy to pick back up and is easy to understand.
- Have a project that could be continually built off of so it doesn't need to "end".


## High Level Breakdown
The following is a high level breakdown of the code and how it has been organized.

### Libraries Directory (Portfolio Infrastructure)
The main section of the program is the infrastructure around managing the "portfolios", or tracking different accounts and their stocks. The following classes comprise of the main portfolio logic:

#### AccountLibrary
- Takes care of all account information, including identifying information, links to all stocks and their quantities, liquid capital, and more.

#### Stock Classes
There are several stock classes depending on the program that is being ran. Some stocks are designed to use live information directly, others pull from a live, local database, and future ones can pull from data already collected for historical analysis.

The main stocks classes are
- StockBaseClass: The parent abstract class used for inheritance.
- StockSubClasses: The child classes, like the observer (pulls from local database), direct (pulls directly from yfinance) and soon to be more.
- StockFactory: Used by other programs to create the desired stock object, since the type may be dynamic.

#### Transaction
The Transaction class is responsible for storing all information for a specific transaction when it takes place. Each time there is a transaction, another transaction object is created, and can be stored and saved so that transaction data can be analyzed. It also contains the transaction logic to keep it compartmentalized.

#### ObserverPattern
There are currently two main ways live stock info can be gathered, through yfinance API calls directly, or though the created "Observer Pattern" which this class performs. yfinance can only be called so many times a day, so this limits how many algorithms can run depending on how many calls they do a second.

The solution was to create an observer pattern class, a class that is the sole source that calls yfinance and dispenses the information to the other classes. The ObserverPattern checks the desired stock value every X seconds and saves it to a local database that the other programs can pull from.

These databases can also be used in the future for testing and analysis.

#### EmailSenderLibrary
This class takes care of all the logic around formulating the daily email report and sending the email at the end of the day.

### Algorithms Directory
This entire directory is dedicated to algorithm modules. In here, new Python modules can be created that can specify algorithms that should be used when trading specific stocks. 

The current default algorithm will buy a stock after it rises X percent, and sell it if it falls X percent. The percentage can be modified to the users discretion.

### Bin Directory
The bin directory has the startup scripts and main program that runs on startup on the testrunner. This directory is designed to keep all the main startup programs and materials for ease of use and organizational purposes.  

### Databases Directory
This directory contains all the active databases, there are the observer, sqlite databases, as well as some legacy databases that store the values of the specific stocks in a .txt file for easy accesses.

### Logs Directory
Contains the saved information for the accounts and the transactions. These logs can be used to load accounts and save their information so they can be used overtime.

Also contains some maintenance logs with debug outputs from different programs.

### Programs Directory
Contains the list of programs that can be executed. The programs tie together the portfolio logic and the algorithms to execute certain stock trading methods.

### Email Reporting Directory
Contains the executable program that executes the email sending logic defined in the EmailSenderLibrary class.

## Execution
To execute the stock programs, the testrunner will turn on for the day and kick off the startup.sh script.

The startup.sh script will start the following:
- database_creator_generic_01.py. which saves several stock info logic to the plain text data bases.
- program_main.py, which starts the main programs and is the primary script. This will kick off:
     - observer_pattern.py, which starts the observer pattern and saves stock data to the sqlite database every X seconds.
     - Several `program` scripts, each of which run their own stock trading algorithm with different parameters
       - Right now it runs 6 different versions of the buy-when-rise-sell-when-fall algorithm, varying in the perecent change paramater for each
       - Each program is kicked off as a subprocess
     -  At the end of the day, the `program_main.py` will kill all subprocess and send the email using the email logic.

This runs automatically every trading day from 8:45am-4:15pm EST

## Planned Updates
Several updates are planned as one of the primary objectives of this project is to be something that can be continually updated/improved. Current future updates include:
- Making the algorithms their own class, with an abstract parent class so they can be used with a similar interface.
- Finishing the historical stock class, so it algorithms can run on historical data and be tested faster.
- Adding many more stock trading algorithms and more parameters.
- Adding a watchdog program that ensures all other programs are running correctly.
- Write a brief report to show the code and thought process of the project in a bit more detail.

