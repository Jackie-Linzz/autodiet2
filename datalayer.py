# only care about data
import datetime
import time
import re
import mysql
import data
import util


def insert(table, row):
    if mysql.insert(table, row):
        return True
    return False


def insert_many(table, rows):
    if mysql.insert_many(table, rows):
        return True
    return False


def delete(table, con):
    if mysql.delete(table, con):
        return True
    return False


def delete_all(table):
    if mysql.delete_all(table):
        return True
    return False


def get(table, con):
    res = mysql.get(table, con)
    return res


def get_all(table):
    res = mysql.get_all(table)
    return res


def get_order(time_from, time_to):
    if not isinstance(time_from, float) or not isinstance(time_to, float):
        return None
    sql = 'select did, sum(num) as n from order_history where stamp >= %s and stamp < %s group by did order by did' % (time_from, time_to)
    cursor = mysql.query(sql)
    res = []
    total = 0
    for row in cursor.fetchall():
        did = row[0]
        num = row[1]
        t = filter(lambda x: x['did'] == did, data.diet)
        if len(t) != 1:
            continue
        item = t[0]
        total += item['price'] * num
        res.append({'did': did, 'name': item['name'], 'sum': num, 'price': item['price'], 'total': item['price'] * num})
    for item in res:
        item['percentage'] = '%.2f' % (item['total'] * 100/total)
    res.sort(key=lambda x: x['did'])
    return res


def get_feedback(time_from, time_to):
    if not isinstance(time_from, float) or not isinstance(time_to, float):
        return None
    sql = 'select did, fb, sum(num) from feedback where stamp >= %s and stamp < %s group by did, fb' % (time_from, time_to)
    cursor = mysql.query(sql)

    res = map(lambda x: {'did': x['did'], 'name': x['name'], 'num': 0, 'good': 0, 'normal': 0, 'bad': 0}, data.diet)
    for row in cursor.fetchall():
        did = row[0]
        fb = row[1]
        num = row[2]
        t = filter(lambda x: x['did'] == did, res)
        if len(t) != 1:
            continue
        item = t[0]
        item['num'] += num

        if fb == -1:
            item['bad'] = num
        elif fb == 0:
            item['normal'] = num
        elif fb == 1:
            item['good'] = num
    res.sort(key=lambda x: x['did'])
    return res


def get_trend(num, base):
    if not isinstance(num, int):
        return None
    if num > 12 or num < 0:
        num = 12
    label = []
    end = range(num)
    end.reverse()
    start = map(lambda x: x + 1, end)
    if base == 'day':
        day = datetime.timedelta(days=1)
        today = datetime.date.today()
        time_from = map(lambda x: time.mktime((today - x * day).timetuple()), start)
        time_to = map(lambda x: time.mktime((today - x * day).timetuple()), end)
        label = map(lambda x: util.stamptostr(x), time_from)
    elif base == 'week':
        week = datetime.timedelta(weeks=1)
        today = datetime.date.today()
        time_from = map(lambda x: time.mktime((today - x * week).timetuple()), start)
        time_to = map(lambda x: time.mktime((today - x * week).timetuple()), end)
        label = map(lambda x: util.stamptostr(x), time_from)
    elif base == 'month':
        today = datetime.date.today()
        year = today.year
        month = today.month
        def get_date(x):
            if month-x > 0:
                return year, month-x
            else:
                return year-1, month - x + 12
        time_from = map(lambda x: datetime.date(get_date(x)[0], get_date(x)[1], 1), start)
        time_to = map(lambda x: datetime.date(get_date(x)[0], get_date(x)[1], 1), end)
        #print time_from
        #print time_to
        time_from = map(lambda x: time.mktime(x.timetuple()), time_from)
        time_to = map(lambda x: time.mktime(x.timetuple()), time_to)
        label = map(lambda x: util.stamptostr(x), time_from)
    sql = 'select did, sum(num) from order_history where stamp >= %s and stamp < %s group by did'
    interval = zip(time_from, time_to)
    res = []
    for i in interval:
        cursor = mysql.query(sql % i)
        total = 0
        for row in cursor.fetchall():
            did = row[0]
            num = row[1]
            t = filter(lambda x: x['did'] == did, data.diet)
            if len(t) != 1:
                continue
            item = t[0]
            total += item['price'] * num
        res.append(total)

    return label, res


def get_cookinfo(time_from, time_to):
    r = re.compile(r'^([0-9]{4})\.([0-9]{2}|[0-9])\.([0-9]{2}|[0-9])$')
    if not r.match(time_from) or not r.match(time_to):
        return None
    time_from = util.strtostamp(time_from)
    time_to = util.strtostamp(time_to)
    sql = 'select fid, did, sum(num) from cook_history where stamp >= %s and stamp < %s group by fid, did' % (time_from, time_to)
    cursor = mysql.query(sql)
    res = filter(lambda x: x['role'] == 'cook', data.faculty)
    res = map(lambda x: {'fid': x['fid'], 'name': x['name'], 'num': 0, 'num_per': 0, 'total': 0, 'total_per': 0}, res)
    num_total = 0
    total_total = 0
    for row in cursor.fetchall():
        fid = row[0]
        did = row[1]
        num = row[2]
        d = filter(lambda x: x['did'] == did, data.diet)
        item = filter(lambda x: x['fid'] == fid, res)
        if len(d) != 1 or len(item) != 1:
            continue
        d = d[0]
        item = item[0]
        item['num'] += num

        item['total'] += num * d['price']
        num_total += num
        total_total += num * d['price']
    for row in res:
        row['num_per'] = '%.2d' % (row['num'] * 100 / num_total)
        row['total_per'] = '%.2d' % (row['total'] * 100 / total_total)
    res.sort(key=lambda x: x['fid'])
    return res, num_total, total_total


def get_onecookinfo(fid, time_from, time_to):
    r = re.compile(r'^([0-9]{4})\.([0-9]{2}|[0-9])\.([0-9]{2}|[0-9])$')
    if not r.match(time_from) or not r.match(time_to):
        return None
    time_from = util.strtostamp(time_from)
    time_to = util.strtostamp(time_to)
    sql = 'select * from cook_history where fid = %s and stamp >= %s and stamp < %s' % (fid, time_from, time_to)
    sql = 'select feedback.did, fb, sum(feedback.num) from (' + sql + ') as p, feedback where p.did = feedback.did group by feedback.did, fb '
    cursor = mysql.query(sql)

    res = map(lambda x: {'did': x['did'], 'name': x['name'], 'num': 0, 'good': 0, 'normal': 0, 'bad': 0}, data.diet)
    for row in cursor.fetchall():
        did = row[0]
        fb = row[1]
        num = row[2]
        t = filter(lambda x: x['did'] == did, res)
        if len(t) != 1:
            continue
        item = t[0]
        item['num'] += num

        if fb == -1:
            item['bad'] = num
        elif fb == 0:
            item['normal'] = num
        elif fb == 1:
            item['good'] = num
    res.sort(key=lambda x: x['did'])
    return res

