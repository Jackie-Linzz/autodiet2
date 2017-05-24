import mysql

print mysql.delete('category', {'cid': 1}).rowcount
print mysql.delete_all('category').rowcount

print mysql.delete('diet', {'did': 1}).rowcount
print mysql.delete_all('diet').rowcount

print mysql.delete_all('faculty').rowcount

print mysql.delete_all('order_history').rowcount

print mysql.delete_all('cook_history').rowcount

print mysql.delete_all('feedback').rowcount

print mysql.delete_all('stat_week').rowcount

print mysql.delete_all('stat_month').rowcount
