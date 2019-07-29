import json
import os
import datetime

from utils.log import FileLogger
import utils.timer

import sqlite3
print(sqlite3.sqlite_version)
db_conn_path = os.path.join(os.path.dirname(__file__),'repo.db')
conn = sqlite3.connect(db_conn_path)

def query(table, where):
    cursor = conn.cursor()

    sql = '''SELECT * FROM {0} WHERE {1}'''.format(table, where)
    result = []
    try:
        cursor.execute(sql)
        row = cursor.fetchone()  
        while row:
            column_value = {}
            for i in range(len(cursor.description)):
                column_value[str(cursor.description[i][0])] = row[i]
            result.append(column_value)    
            row = cursor.fetchone()
    except sqlite3.OperationalError:
        FileLogger.exception('Exception at '+__file__+' '+__name__)
    return result

def insert(table, column_value):
    if not column_value:
        return False

    columns = ''
    values = ''
    for i in column_value:
        columns += '{0},'.format(i)
        values += '{0},'.format(column_value[i])
    play_date = utils.timer.get_settlement_time()
    sql = '''INSERT INTO {0} ({1}play_date) VALUES ({2}'{3}')'''.format(table, columns, values, play_date)

    cursor = conn.cursor()
    cursor.execute("BEGIN")
    try:
        cursor.execute(sql)
    except sqlite3.OperationalError:
        FileLogger.exception('Exception at '+__file__+' '+__name__)
        conn.rollback()
        return False
    cursor.execute("COMMIT") 
    conn.commit()
    return True

def increment(table, column_value, where):
    if not column_value:
        return False

    sets = ''
    for i in column_value:
        if where.startswith(i):
            continue
        sets += '''{0}={0}+{1},'''.format(i, column_value[i])
    sql = '''UPDATE {0} SET {1} WHERE {2}'''.format(table, sets, where)

    cursor = conn.cursor()
    cursor.execute("BEGIN")
    try:
        cursor.execute(sql)
    except sqlite3.OperationalError:
        FileLogger.exception('Exception at '+__file__+' '+__name__)
        conn.rollback()
        return False
    cursor.execute("COMMIT") 
    conn.commit()
    return True

def upsert(table, column_value, where):
    if not column_value:
        return False

    play_date = utils.timer.get_settlement_time()
    where += ''' AND play_date='{0}' '''.format(play_date)
    result = query(table, where)

    if result:
        return increment(table, column_value, where)
    else:
        return insert(table, column_value)

def find_last_period():
    sql ='''WITH 
                dates(cast_date) AS (
                    SELECT DISTINCT play_date
                    FROM TimeTable
                ),
                groups AS (
                    SELECT
                        date(cast_date, '-'||(ROW_NUMBER() OVER (ORDER BY cast_date))||' days') AS grp,
                        cast_date
                    FROM dates
                )
            SELECT
                MIN(cast_date) AS date_start,
                MAX(cast_date) AS date_end
            FROM groups GROUP BY grp ORDER BY 2 DESC LIMIT 1'''

    cursor = conn.cursor() 
    result = []
    try:
        cursor.execute(sql)
        result = cursor.fetchone()
    except sqlite3.OperationalError:
        FileLogger.exception('Exception at '+__file__+' '+__name__)

    if not result or len(result) != 2:
        FileLogger.error('Failed to collect play_date')
        return

    parsed = []
    try:
        parsed.append(str(result[0]))
        parsed.append(str(result[1]))
    except ValueError:
        FileLogger.exception('Date format error')
        FileLogger.error('Collected play_date not valid')
        return []
    return parsed