import redis


r = redis.StrictRedis()

print r.keys('*')
r.hmset('hash', {'num': 1, 'name': 'haha'})
print r.hgetall('hash')
