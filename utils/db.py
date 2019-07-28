import json
import os
import pymssql

from utils.log import FileLogger

db_conn_path = os.path.join(os.path.dirname(__file__),'db_conn.json')
with open(db_conn_path) as json_file:
    data = json.load(json_file)
conn = pymssql.connect(server=data['server'], user=data['user'], password=data['password'], database=data['database'])

def query(table, where):
    sql = 'SELECT * FROM {0} WHERE {1}'.format(table, where)
    cursor = conn.cursor()
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
    except pymssql.OperationalError:
        FileLogger.exception('SQL error')
        conn.rollback()
    except Exception:
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
    sql = 'INSERT {0} ({1}) VALUES ({2})'.format(table, columns[:-1], values[:-1])

    cursor = conn.cursor()        
    cursor.execute("BEGIN TRANSACTION")
    try:
        cursor.execute(sql)
    except pymssql.OperationalError:
        FileLogger.exception('SQL error')
        conn.rollback()
        return False
    except Exception:
        FileLogger.exception('Exception at '+__file__+' '+__name__)
        return False
    cursor.execute("COMMIT TRANSACTION") 
    conn.commit()
    return True

def upsert(table, column_value, where, incre=False):
    if not column_value:
        return False

    sets = ''
    columns = ''
    values = ''
    for i in column_value:
        columns += '{0},'.format(i)
        values += '{0},'.format(column_value[i])
        if where.startswith(i):
            continue
        if incre:
            sets += '{0}={0}+{1},'.format(i, column_value[i])
        else:
            sets += '{0}={1},'.format(i, column_value[i])
    sql =  'IF EXISTS ( SELECT * FROM {0} WITH (UPDLOCK) WHERE {1})\
                UPDATE {0} SET {2} WHERE {1}\
            ELSE \
                INSERT {0} ({3}) VALUES ({4})'.format(table, where, sets[:-1], columns[:-1], values[:-1])

    cursor = conn.cursor()
    cursor.execute("SET TRANSACTION ISOLATION LEVEL SERIALIZABLE")
    cursor.execute("BEGIN TRANSACTION")
    try:
        cursor.execute(sql)
    except pymssql.OperationalError:
        FileLogger.exception('SQL error')
        conn.rollback()
        return False
    except Exception:
        FileLogger.exception('Exception at '+__file__+' '+__name__)
        return False
    cursor.execute("COMMIT TRANSACTION") 
    conn.commit()
    return True