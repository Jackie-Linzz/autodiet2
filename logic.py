import uuid
import time
from tornado.concurrent import Future
import data


tables = {}
tables_waiter = {}
cooks = {}

class Order:
    def __init__(self, did, demand=''):
        t = filter(lambda x: x['did'] == did, data.diet)
        if len(t) != 1:
            return
        item = t[0]

        self.uid = str(uuid.uuid4())
        self.did = did
        self.name = item['name']
        self.price = item['price']
        self.base = item['base']
        self.num = self.base
        self.cid = item['cid']
        self.ord = item['ord']
        self.picture = item['picture']


        self.demand = demand
        self.stamp = time.time()

        self.taken = False
        #left submit taken doing done
        self.status = 'none'
        self.cancel = False

        self.appraise = None

    def to_dict(self):
        res = {}
        res['uid'] = self.uid
        res['did'] = self.did
        res['name'] = self.name
        res['price'] = self.price
        res['base'] = self.base
        res['num'] = self.num
        res['cid'] = self.cid
        res['ord'] = self.ord
        #res['picture'] = self.picture

        res['demand'] = self.demand
        res['status'] = self.status
        return res


class Table:
    def __init__(self, desk):
        self.desk = desk
        self.orders = []
        self.left = []
        self.packs = []
        self.gdemand = ''
        self.customers = set([])

        self.waiters = set([])
        self.stamp = time.time()

        self.submit_time = 0
        self.last_time = 0

        self.status = 'none'

    def reset(self):
        self.orders = []
        self.left = []
        self.gdemand = ''
        self.customers = set([])

        self.submit_time = time.time()
        self.last_time = time.time()

        self.status = 'none'

    def check_done(self):
        for one in self.orders:
            if one.status != 'done':
                return False
        return True


    def perform(self, who, ins):
        #print who,
        if self.status == 'lock':
            if who == 'customer':
                pass
                return

        # add a base piece,ins ('+', 'id', 'demand')
        if '+' == ins[0]:
            self.status = 'none'
            # add new diet and merge with the previous same one
            did = ins[1]
            demand = ins[2]
            one = Order(did, demand)
            self.left.append(one)

        # ('-', 'uid')
        elif '-' == ins[0]:
            self.status = 'none'
            #delete diet
            uid = ins[1]
            self.left = filter(lambda x: x.uid != uid, self.left)
        #('gd', '')
        elif 'gd' == ins[0]:
            self.status = 'none'
            #modify 'gdemand'
            self.gdemand = ins[1]
        #('d', 'uid', 'demand')
        elif 'd' == ins[0]:
            self.status = 'none'
            uid = ins[1]
            demand = ins[2]
            t = filter(lambda x: x.uid == uid, self.left)
            one = t[0]
            one.demand = demand

        elif 'submit' == ins[0]:
            if self.left:
                if self.status == 'none':
                    self.status = 'ready'
                elif self.status == 'ready':
                    self.status = 'submit'
                if self.status == 'submit':
                    self.status = 'lock'

                    if who == 'customer':
                        #submit request
                        customer_submits.request(self.desk)
                    if who == 'waiter':
                        #direct submit
                        self.confirm()

        elif 'confirm' == ins[0]:
            if self.status == 'lock':
                self.confirm()

        self.stamp = time.time()
        self.set_future()

    def confirm(self):

        #impart self.gdemand
        if self.gdemand:
            for one in self.left:
                one.demand += ','+self.gdemand
            self.gdemand = ''
        #check submit_time
        if self.check_done():
            self.submit_time = time.time()
        #pack
        pack = Pack(self.left, time.time(), self.customers)
        self.packs.append(pack)
        self.orders += self.left
        self.left = []
        self.orders.sort(key=lambda x: x.ord)

    def waiter_update(self, stamp):
        future = Future()
        if stamp < self.stamp:
            future.set_result(self.order_dict())
        else:
            self.waiters.add(future)
        return future

    def set_future(self):
        for future in self.waiters:
            try:
                future.set_result(self.order_dict())
            finally:
                pass
        self.waiters = set([])
    def order_dict(self):
        res = {}
        res['stamp'] = self.stamp
        res['orders'] = [x.to_dict() for x in self.orders]
        res['left'] = [x.to_dict() for x in self.left]
        return res


class Pack:
    def __init__(self, orders, submit_time, customers):
        self.customers = customers
        self.submit_time = submit_time
        self.orders = []
        self.orders += orders
        self.appraised = False


class CustomerRequestBuffer(object):

    def __init__(self):
        self.waiters = set([])
        #for requests
        self.buffer = []
        self.stamp = time.time()

    def request(self, desk):
        if desk is None:
            return
        if desk not in self.buffer:
            self.buffer.append(desk)
            self.buffer.sort()
            self.stamp = time.time()
        self.set_future()
        return self.buffer

    def answer(self, desk):
        if desk in self.buffer:
            self.buffer.remove(desk)
            self.stamp = time.time()
        self.set_future()
        return self.buffer

    def set_future(self):
        for future in self.waiters:
            try:
                future.set_result(self.buffer)
            finally:
                pass
        self.waiters = set([])

    def update(self, stamp):
        future = Future()
        if stamp < self.stamp:
            future.set_result(self.buffer)
        else:
            self.waiters.add(future)
        return future


class CookRequestBuffer(object):
    def __init__(self):
        self.waiters = set([])
        #for requests
        #(fid, name)
        self.buffer = []
        self.stamp = time.time()

    def request(self, fid):
        if fid is None:
            return

        fids = map(lambda x: x[0], self.buffer)
        global cooks
        #cursor.execute('select * from faculty where id=:fid', {'fid': fid})
        #row = cursor.fetchone()
        #name = row['name']

        if fid not in fids:
            t = filter(lambda x: x['fid'] == fid, data.faculty)
            name = t[0]['name']
            self.buffer.append((fid, name))

            self.stamp = time.time()
        self.set_future()
        return self.buffer

    def answer(self, fid):

        self.buffer = filter(lambda x: x[0] != fid, self.buffer)
        self.stamp = time.time()
        self.set_future()
        return self.buffer

    def set_future(self):
        for future in self.waiters:
            try:
                future.set_result(self.buffer)
            finally:
                pass
        self.waiters = set([])

    def update(self, stamp):
        future = Future()
        if stamp < self.stamp:
            future.set_result(self.buffer)
        else:
            self.waiters.add(future)
        return future


class CookFinishBuffer(object):

    def __init__(self):
        self.waiters = set()
        #for requests
        self.buffer = []
        self.stamp = time.time()

    def request(self, finish):
        if finish is None:
            return
        #(uid, name, num, desk, fid, cookname)
        if finish not in self.buffer:
            self.buffer.append(finish)

            self.stamp = time.time()
        self.set_future()
        return self.buffer

    def answer(self, uid):
        self.buffer = filter(lambda x: x[0] != uid, self.buffer)
        self.stamp = time.time()
        self.set_future()
        return self.buffer

    def set_future(self):
        for future in self.waiters:
            try:
                future.set_result(self.buffer)
            finally:
                pass
        self.waiters = set()

    def update(self, stamp):
        future = Future()
        if stamp < self.stamp:
            future.set_result(self.buffer)
        else:
            self.waiters.add(future)
        return future
customer_requests = CustomerRequestBuffer()
customer_submits = CustomerRequestBuffer()
cook_requests = CookRequestBuffer()
cook_finish = CookFinishBuffer()
