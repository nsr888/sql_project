import pandas as pd


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

def dropTemp(con):
    cursor = con.cursor()
    cursor.execute('drop table if exists cards')
    cursor.execute('drop table if exists accounts')
    cursor.execute('drop table if exists clients')
    con.commit()

def printAllTables(con):
    showData(con, 'DWH_DIM_CARDS')
    showData(con, 'DWH_DIM_ACCOUNTS')
    showData(con, 'DWH_DIM_CLIENTS')
    showData(con, 'DWH_FACT_PASSPORT_BLACKLIST')
    showData(con, 'DWH_DIM_TERMINALS_HIST')
    showData(con, 'DWH_FACT_TRANSACTIONS')

