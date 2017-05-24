import MySQLdb


conn = MySQLdb.connect(host='localhost', port=3306, user='autodiet', passwd='autodiet2', db='autodiet2', charset='utf8')
conn.autocommit(False)

cursor = conn.cursor()

#row is dict
def insert(table, row):

    if not isinstance(row, dict):
        return False
    columns = []
    values = []
    for k, v in row.items():
        columns.append(str(k))
        if isinstance(v, (str, unicode)):
            v = '"%s"' % v
        values.append(str(v))
    columns = ','.join(columns)
    values = ','.join(values)

    sql = 'insert into %s (%s) values (%s)' % (table, columns, values)
    try:
        global cursor
        cursor.execute(sql)
        conn.commit()
        return cursor
    except Exception as e:
        print e
        conn.rollback()
        return None


def insert_many(table, rows):
    #check row key consistence
    if not isinstance(rows, (list, tuple)):
        return False
    if len(rows) < 1:
        return False
    if not isinstance(rows[0], dict):
        return False
    keys = rows[0].keys()
    columns = ','.join(keys)
    template = ','.join(['%s'] * len(keys))

    values = []
    for row in rows:
        if set(keys) != set(row.keys()):
            return False
        temp = []
        for key in keys:
            v = row[key]
            #if isinstance(v, (str, unicode)):
             #   v = '"%s"' % v
            temp.append(v)
        values.append(temp)

    sql = 'insert into %s (%s) values (%s)' % (table, columns, template)

    try:
        global cursor
        cursor.executemany(sql, values)
        conn.commit()
        return cursor
    except Exception as e:
        print e
        conn.rollback()
        return None


def delete(table, con):

    if not isinstance(con, dict):
        return False
    condition = []
    for k, v in con.items():
        if isinstance(v, (str, unicode)):
            v = '"%s"' % v
        condition.append('%s = %s' % (k, v))
    condition = 'and'.join(condition)
    sql = 'delete from %s where %s' % (table, condition)
    try:
        global cursor
        cursor.execute(sql)
        conn.commit()
        return cursor
    except Exception as e:
        print e
        conn.rollback()
        return None


def delete_all(table):
    sql = 'delete from %s' % table
    try:
        global cursor, conn
        cursor.execute(sql)
        conn.commit()
        return cursor
    except Exception as e:
        print e
        conn.rollback()
        return None


def update(table, row):

    pass


def query(sql):
    try:
        global cursor, conn
        cursor.execute(sql)
        conn.commit()
        return cursor
    except Exception as e:
        print e
        conn.rollback()
        return None



def get(table, con):
    global cursor
    if not isinstance(con, dict):
        return False
    condition = []
    for k, v in con.items():
        if isinstance(v, (str, unicode)):
            v = '"%s"' % v
        condition.append('%s = %s' % (k, v))
    condition = 'and'.join(condition)
    sql = 'select * from %s where %s' % (table, condition)
    try:

        cursor.execute(sql)
        conn.commit()

    except Exception as e:
        print e
        conn.rollback()
        return None

    columns = [d[0] for d in cursor.description]

    result = [dict(zip(columns, row)) for row in cursor.fetchall()]
    return result


def get_all(table):
    sql = 'select * from %s' % table
    try:
        global cursor, conn
        cursor.execute(sql)
        conn.commit()

    except Exception as e:
        print e
        conn.rollback()
        return None

    columns = [d[0] for d in cursor.description]

    result = [dict(zip(columns, row)) for row in cursor.fetchall()]
    return result



