#coding=utf-8
import MySQLdb

conn = MySQLdb.connect(host='localhost', port=3306, user='autodiet', passwd='autodiet2', db='test', charset='utf8')



cursor = conn.cursor()

t = 'haha'
t = '"%s"' % t
print t

sql = 'insert into type (n, c) values (%s, "%s")' % (5, '哦哦')
print sql
sql2 = 'select * from type'
cursor.execute(sql2)
print cursor.description

print cursor.fetchall()
conn.commit()

conn.close()