import sqlite3
import sys
from py_scripts import utils, load2db, load2db_terminals, fraud


if __name__ == "__main__":
    con = sqlite3.connect('sber.db')
    load2db.sql_load(con, './sql_scripts/init.sql')  # create all tables
    load2db.bank(con)
    date = ''
    try:
        date = utils.getFileDate()  # extract current date from given files names
    except Exception as e:
        print('Error: ' + str(e))
        sys.exit()
    if date != '':  # if date extracted and files found
        load2db.transactions(con, date)
        load2db.passport_blacklist(con, date)
        load2db_terminals.incremental_load(con, date)
        # utils.printAllTables(con)
        fraud.passport(con, date)
        fraud.account(con, date)
        fraud.city(con)
        fraud.sum_guessing(con)
    utils.showData(con, 'REP_FRAUD')
