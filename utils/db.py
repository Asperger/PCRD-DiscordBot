import json
import os
import datetime

from utils.log import FileLogger
from utils.sqlite_undoredo import SQLiteUndoRedo
import utils.timer

import sqlite3
db_conn_path = os.path.join(os.path.dirname(__file__),'repo.db')
conn = sqlite3.connect(db_conn_path)
try:
    conn.executescript(
        '''CREATE TABLE "TimeTable" (
            "user_id"	INTEGER NOT NULL,
            "rounds"	INTEGER NOT NULL,
            "boss"	INTEGER NOT NULL,
            "damage"	INTEGER NOT NULL,
            "play_date"	TEXT NOT NULL
        );
        CREATE TABLE "UserTable" (
            "user_id"	INTEGER NOT NULL,
            "damage"	INTEGER NOT NULL,
            "normal_play"	INTEGER NOT NULL DEFAULT 0,
            "last_play"	INTEGER NOT NULL DEFAULT 0,
            "compensate_play"	INTEGER NOT NULL DEFAULT 0,
            "missing_play"	INTEGER NOT NULL DEFAULT 0,
            "play_date"	TEXT NOT NULL,
            "played_boss"	TEXT NOT NULL
        );'''
    )
except sqlite3.OperationalError:
    pass

sqlur = SQLiteUndoRedo(conn)
sqlur.activate('TimeTable', 'UserTable')

def query(table, where):
    cursor = conn.cursor()

    sql = f'''SELECT * FROM {table} WHERE {where}'''
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
        FileLogger.exception(f'Exception at {__file__} {__name__}\nSQL: {sql}')
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
    sql = f'''INSERT INTO {table} ({columns}play_date) VALUES ({values}'{play_date}')'''

    cursor = conn.cursor()
    cursor.execute("BEGIN")
    try:
        cursor.execute(sql)
    except sqlite3.OperationalError:
        FileLogger.exception(f'Exception at {__file__} {__name__}\nSQL: {sql}')
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
        if type(column_value[i]) is str:
            sets += f'''{i}={i}||','||{column_value[i]},'''
        else:
            sets += f'''{i}={i}+{column_value[i]},'''
    sql = f'''UPDATE {table} SET {sets[:-1]} WHERE {where}'''

    cursor = conn.cursor()
    cursor.execute("BEGIN")
    try:
        cursor.execute(sql)
    except sqlite3.OperationalError:
        FileLogger.exception(f'Exception at {__file__} {__name__}\nSQL: {sql}')
        conn.rollback()
        return False
    cursor.execute("COMMIT") 
    conn.commit()
    return True

def upsert(table, column_value, where):
    if not column_value:
        return False

    play_date = utils.timer.get_settlement_time()
    where += f''' AND play_date='{play_date}' '''
    result = query(table, where)

    if result:
        return increment(table, column_value, where)
    else:
        return insert(table, column_value)