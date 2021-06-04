import sqlite3
import os
from py_scripts import utils


if __name__ == "__main__":
    con = sqlite3.connect('sber.db')
    utils.loadSql(con, './sql_scripts/init.sql')
    utils.loadSql(con, 'ddl_dml.sql')
    for fname in os.listdir('.'):
        if (fname.startswith('transactions')):
            utils.loadCsv(con, fname, 'STG_TRANSACTIONS')
        if (fname.startswith('passport')):
            utils.loadExcel(con, fname, 'STG_PASSPORT_BLACKLIST')
        if (fname.startswith('terminals')):
            utils.loadExcel(con, fname, 'STG_TERMINALS')
    utils.loadSql(con, './sql_scripts/transfer.sql')
    utils.dropTemp(con)
    utils.printAllTables(con)
