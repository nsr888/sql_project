import pandas as pd
import os
import sys


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def countData(con, objName):
    cursor = con.cursor()
    cursor.execute(f'select count(*) from {objName}')
    result = cursor.fetchone()
    print(f'{result[0]} rows\n')


def showData(con, objName):
    cursor = con.cursor()
    print(bcolors.OKBLUE + '-_'*20 + '\n' + objName + '\n' + '-_'*20 + '\n'
            + bcolors.ENDC)
    cursor.execute(f'select * from {objName}')
    title = [i[0] for i in cursor.description]
    print(title)
    # for row in cursor.fetchall():
    for row in cursor.fetchall()[0:10]:
        print(row)
    countData(con, objName)


def printLoading(filePath):
    print(bcolors.OKGREEN + 'Loading ' + filePath + '...' + bcolors.ENDC)

def loadSql(con, filePath):
    printLoading(filePath)
    cursor = con.cursor()
    sql_file = open(filePath)
    sql_as_string = sql_file.read()
    cursor.executescript(sql_as_string)
    con.commit()


def loadCsv(con, filePath, tableName):
    printLoading(filePath)
    df = pd.read_csv(filePath, sep=';')
    df.to_sql(tableName, con=con, if_exists='replace', index=False)


def loadExcel(con, filePath, tableName):
    printLoading(filePath)
    df = pd.read_excel(filePath)
    df.to_sql(tableName, con=con, if_exists='replace', index=False)


def printAllTables(con):
    showData(con, 'DWH_DIM_CARDS')
    showData(con, 'DWH_DIM_ACCOUNTS')
    showData(con, 'DWH_DIM_CLIENTS')
    showData(con, 'DWH_FACT_PASSPORT_BLACKLIST')
    showData(con, 'DWH_DIM_TERMINALS_HIST')
    showData(con, 'DWH_FACT_TRANSACTIONS')


def loadBank(con):
    loadSql(con, 'ddl_dml.sql')  # create accounts, cards, clients tables
    cursor = con.cursor()
    cursor.execute('''
        insert into DWH_DIM_CARDS (
            card_num, account_num, create_dt, update_dt
        ) select
            card_num, account, create_dt, update_dt from cards;
    ''')
    cursor.execute('''
        insert into DWH_DIM_ACCOUNTS (
            account_num, valid_to, client, create_dt, update_dt
        ) select
            account, valid_to, client, create_dt, update_dt from accounts;
    ''')
    cursor.execute('''
        insert into DWH_DIM_CLIENTS (
            client_id, last_name, first_name, patronymic, date_of_birth,
            passport_num, passport_valid_to, phone, create_dt, update_dt
        ) select
            client_id, last_name, first_name, patronymic, date_of_birth,
            passport_num, passport_valid_to, phone, create_dt,
            update_dt from clients;
    ''')
    cursor.execute('drop table if exists cards')
    cursor.execute('drop table if exists accounts')
    cursor.execute('drop table if exists clients')
    con.commit()


def getFileDate():
    date = ''
    lst = os.listdir('.')
    lst.sort()
    for fname in lst:
        if fname.startswith('transactions'):
            date = fname.split("_", 1)[1].split(".", 1)[0]
            break
    if date == '':
        raise Exception('Files not found')
    if not os.path.isfile('transactions_' + date + '.txt'):
        raise Exception('transactions file not found')
    if not os.path.isfile('passport_blacklist_' + date + '.xlsx'):
        raise Exception('passport_blacklist file not found')
    if not os.path.isfile('terminals_' + date + '.xlsx'):
        raise Exception('terminals file not found')
    return date


def loadTransactions(con, date):
    source_file = "transactions_" + date + ".txt"
    loadCsv(con, source_file, 'STG_TRANSACTIONS')
    cursor = con.cursor()
    cursor.execute('''
        insert into DWH_FACT_TRANSACTIONS (
            trans_id, trans_date, amt, card_num, oper_type, oper_result,
            terminal
        ) select
            transaction_id, transaction_date, amount, card_num, oper_type,
            oper_result, terminal from STG_TRANSACTIONS;
    ''')
    cursor.execute('drop table if exists STG_TRANSACTIONS')
    con.commit()
    backup_file = os.path.join("archive", "transactions_" + date + ".txt.backup")
    os.rename(source_file, backup_file)
    return date


def loadPassportBlk(con, date):
    source_file = "passport_blacklist_" + date + ".xlsx"
    loadExcel(con, source_file, 'STG_PASSPORT_BLACKLIST')
    cursor = con.cursor()
    cursor.execute('''
        insert into DWH_FACT_PASSPORT_BLACKLIST (
            passport_num, entry_dt
        ) select
            passport, date from STG_PASSPORT_BLACKLIST;
    ''')
    cursor.execute('drop table if exists STG_PASSPORT_BLACKLIST')
    backup_file = os.path.join("archive", "passport_blacklist_" + date + ".xlsx.backup")
    os.rename(source_file, backup_file)
    con.commit()
