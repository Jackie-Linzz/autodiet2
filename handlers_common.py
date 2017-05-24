import tornado.web
import uuid

from tornado.escape import json_decode, json_encode

import data


class EntryHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('entry.html')

    def post(self):
        #as customer
        self.set_secure_cookie('role', 'customer')
        #set desk
        desk = json_decode(self.get_argument('desk')).upper()
        print desk
        if desk in data.desks:
            self.set_cookie('desk', desk)

            response = {'status': 'ok', 'next': '/customer-cate'}

        else:
            response = {'status': 'ok', 'next': '/'}
        self.write(json_encode(response))


class FacultyLoginHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('faculty-login.html')

    def post(self):
        fid = self.get_argument('fid', None)
        password = self.get_argument('passwd', None)
        if fid is None or password is None:
            response = {'status': 'error', 'next': '/faculty-login'}
            self.finish(json_encode(response))
            return
        fid = json_decode(fid)
        password = json_decode(password)

        faculty = filter(lambda x: x['fid'] == fid, data.faculty)
        row = None
        if faculty:
            row = faculty[0]
        response = {'status': 'error', 'next': '/faculty-login'}
        if row:
            if password == row['password']:
                role = row['role']

                self.set_secure_cookie('role', role)
                self.set_secure_cookie('fid', fid)
                response = {'status': 'ok', 'next': '/faculty-home'}

        self.finish(json_encode(response))


class FacultyHomeHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('faculty-home.html')

    def post(self):
        role = self.get_secure_cookie('role')
        fid = self.get_secure_cookie('fid')
        response = {}
        if role == 'waiter':
            response = {'status': 'ok', 'next': '/waiter-request'}
        elif role == 'cook':
            # init cook
            response = {'status': 'ok', 'next': '/cook-cook'}

        elif role == 'manager':
            response = {'status': 'ok', 'next': '/manager'}
        self.write(json_encode(response))


class FacultyLogoutHandler(tornado.web.RequestHandler):
    def post(self):
        self.clear_cookie('role')
        self.clear_cookie('fid')
        response = {'status': 'ok', 'next': '/'}
        self.finish(json_encode(response))