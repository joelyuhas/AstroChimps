# AstroChimps
Hobby stock trading project using python, sqlite, and automation. This project creates its own account classes and transaction infrastrucutre, pulls in real time stock data using yfinance, and executes several trading algorthims. It runs on its own "testrunner" computer running Linux that automatically turns on Mon-Fri before trading hours, and turns itself off afterwards.

At the end of the trading day, an email with the algorithms daily and weekly results is sent to my personal email, along with graphs of the weekly performance compared to SPY.

Seperate programs save specific stock data to custom databases as well so they can be used to back test new algorthms in the future.

Several software development principals are experimented with here, as well as an oppertunity to work with databases, automation, and real time trading.

This project has been under works on and off for several years and has been a fun hobby project to come back to and to utilize new coding techniques.

More detailed documentation and reports coming soon.

## Objective
There were a few objectives to this project that focused on learning experiences, the main ones are:
- Create a project that follows a topic that has a significant amount of resources and similar support for (stock trading in this case) so that personal implementations could be compared to other implemenations for learning oppertunities
- Have a problem that could be utilzied (trade algorthims) to continue to practice software development strategies and continue to learn new techniques. 
- Have a continouse project that could run automatically for set intervals during the week to practice continouse automaiton.
- Have a project that could be used to practice desigining maintainable code, and come back to it periodically to ensure its easy to pick back up and is easy to understand.
- Have a project that could be continoully built off of so it doesnt need to "end".


## High Level Breakdown
The following is a high level breakdown of the code and how its orginized

### Account Infrastructure (Libraries Directory)
The main section of the program is the infrastrucuture around tracking different accounts, their portfolios, and their stocks. The following classes comprise of the main portfolio logic:

#### AccountLibrary
- Takes care of all account informatoin, including identifying information, all stocks and their quantities, liquid capital, and more.

#### Stock Classes
There are several stock classes depending on the program that is being ran. Some stocks are designed to use live information directly, others pull from a live, local database, and future ones will pull from data alreaedy collected for historical analysis.

The main stocks classes are
- StockBaseClass: The parent abstract class used for inheritance.
- StockSubClasses: The child classes, like the observer (pulls from local database), direct (pulls directly from yfinance) and soon to be more
- StockFactory: Used by other programs to create the desired stock object, since the type may be dynamic.

#### Transaction
The Transaction class is responsible for storing all information for a specific transaction when it takes place. Each time there is a transaction, another transaction object is created, and can be stored and saved so that transactions can be analyzed. It also contains the transaction logic to keep it compartmentalized.

#### ObserverPattern
There are currently two main ways the stock info can be gathered, through yfinance, or though the created "Observer Pattern" which this class performs. yfinance can only be called so many times a day, so this limits how many algorithms can run depnding on how many calls they do if they all call direct.

The solution was to create an observer pattern class, that is the only class that calls yfinance. It checks the desired stock value every X seconds, and saves it to a local database that the other programs can use.

These databases can also beused in the future for testing.

#### EmailSenderLibrary
This class takes care of all the logic around formulating the final report and sending an email at the end of the day.

### Algorithms Directory
An entire directory is dedicated to algorthim modules. In here, new Python modules can be created that can specify algorithms that should be used when trading specific stocks. 

The current default algorthim will buy a stock after it rises X percent, and sell it if it falls X percent. The percentage can be modified to the users discretion.

### Bin Directory
The bin directory has the startup scripts and main program that runs on startup on the testrunner. This directory is designed to keep all the main startup programs and materials for ease of use and orginiaztional purposes.  

### Databases Directory
This directory contains all the active databases, there are the observer, sqlite databases, as well as some legacy databases that store the values of the specific stock in a .txt file for easy accesses.

### Logs Directory
Contains the saved information for the accounts and the transactions. These logs can be used to load accounts and save their informaiton so they can be used overtime.

Also contains some maintence logs with debug outputs from different programs.

### Programs Directory
Contains the list of programs that can be executed. The programs use the algorithms to execute certain stock trading methods.

### Email Reporting Directory
Contains the executable program that executes the email sending logic at the end of the day.

## Execution
To execute, the testrunner will turn on for the day and start the following:
- observer_pattern.py will save the stock info in the database and run continuously
- A legacy database creation process is also started to save the .txt files.
- program_main.py python script will kick off a certain program from the `programs` directory as subprocesses. It normally kicks off several with different paramaters.
- At the end of the day, the `program_main.py` will kill all subprocess and send the email using the email logic.


