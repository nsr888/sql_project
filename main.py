import sqlite3
import os
import sys
from py_scripts import utils, terminals, fraud


if __name__ == "__main__":
    con = sqlite3.connect('sber.db')
    utils.loadSql(con, './sql_scripts/init.sql')  # create all tables
    utils.loadBank(con)
    date = ''
    try:
        date = utils.getFileDate()  # get current date from given files names
    except Exception as e:
        print('Error: ' + str(e))
        sys.exit()
    if date != '':  # if date is set and files found
        utils.loadTransactions(con, date)
        utils.loadPassportBlk(con, date)
        terminals.loadIncremental(con, date)
        # utils.printAllTables(con)
        fraud.passport(con, date)
        fraud.account(con, date)
        fraud.city(con)
    utils.showData(con, 'REP_FRAUD')
