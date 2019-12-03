# How to Install, Run, and Test

## Installing


Install python and pip however you usually install software on your computer

After that you can run `install.bat` on a Windows machine or complete the following steps manually


First, run `pip install pyOpenSSL==17.5.0`


Then, to install all the libraries needed for this, run `pip install -r requirements.txt` from this `backend` folder.

This should install all the libraries needed.  If you get an error saying some module wasn't installed... you can just run `pip install <that module>` to install whatever is missing.

## Setup

The database needs to be setup before you can run the app.  To start with a fresh and clean database, just run the command `flask initdb` from your command line.  

To fill the database with sample data (of your design in tests.py), run `flask bootstrapdb` instead.

Remember, you'll often be deleting/clearing the database, so don't trust any data there to stick around (in development, at least).

## Running

To run the app, from the command line in this folder, just run `flask run`, which will startup a server on `http://localhost:5000/`.  Go to that URL in your browser to start using the app!

## Running tests

To run tests with code coverage, it is important to note a few key steps:

1. run the command `coverage run -m flask test` to run your tests and collect coverage data.  Your test results will print in your console.  To output them to a file (which you will want to do for final reporting), run `coverage run -m flask test > test_results.txt` to write your results to a file called test_results.txt.

2. run the command `coverage html` to generate a beautiful html report to view the coverage data after you ran your tests.

## Other admin commands

To dump the contents of the db (for manual reading), run `flask dumpdb > output_file.txt` 