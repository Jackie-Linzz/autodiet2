import tornado.web
import uuid
import pickle
import os
import qrcode
import tarfile

from tornado.escape import json_decode, json_encode
import util
import data
import datalayer


class ManagerHandler(tornado.web.RequestHandler):
    #@manager_auth
    def get(self):
        self.render('manager.html')


class CompanyInfoHandler(tornado.web.RequestHandler):
    def get(self):
        pass

    def post(self):
        name = json_decode(self.get_argument('name'))
        short_name = json_decode(self.get_argument('sname'))
        address = json_decode(self.get_argument('address'))
        desc = json_decode(self.get_argument('desc'))
        welcome = json_decode(self.get_argument('welcome'))
        info = {'name': name, 'sname': short_name, 'address': address, 'desc': desc, 'welcome': welcome}

        with open(data.company_file, 'wb') as f:

            pickle.dump(info, f)
        response = info
        response['status'] = 'ok'
        self.write(json_encode(response))


class CompanyDataHandler(tornado.web.RequestHandler):
    def post(self):
        file_name = data.company_file
        with open(file_name, 'rb') as f:
            info = pickle.load(f)
        response = info
        response['status'] = 'ok'
        self.write(json_encode(response))


class CateAddHandler(tornado.web.RequestHandler):
    def post(self):
        cid = json_decode(self.get_argument('cid'))
        name = json_decode(self.get_argument('name'))
        order = json_decode(self.get_argument('order'))
        desc = json_decode(self.get_argument('desc'))
        row = {'cid': int(cid), 'name': name, 'ord': int(order), 'description': desc}
        res = datalayer.insert('category', row)
        data.category = datalayer.get_all('category')
        if res:
            response = {'status': 'ok'}
        else:
            response = {'status': 'err'}
        self.finish(json_encode(response))


class CateDelHandler(tornado.web.RequestHandler):
    def post(self):
        cid = json_decode(self.get_argument('cid'))
        con = {'cid': int(cid)}
        res = datalayer.delete('category', con)

        if res:
            response = {'status': 'ok'}
            data.category = datalayer.get_all('category')
        else:
            response = {'status': 'err'}
        self.finish(json_encode(response))


class CateDataHandler(tornado.web.RequestHandler):
    def post(self):
        print data.category
        res = {'status': 'ok', 'cate': data.category}
        self.finish(json_encode(res))


class DietAddHandler(tornado.web.RequestHandler):
    def post(self):
       #attention to variable type
        did = int(self.get_argument('did'))
        name = str(self.get_argument('name'))
        price = float(self.get_argument('price'))
        base = float(self.get_argument('base'))
        cid = int(self.get_argument('cid'))
        order = int(self.get_argument('order'))
        desc = str(self.get_argument('desc'))
        picture = ''

        if self.request.files:
            metas = self.request.files['picture']
            for meta in metas:

                file_name = meta['filename']
                content = meta['body']
                ext = os.path.splitext(file_name)[-1]
                picture = str(uuid.uuid4()) + ext
                full_path = os.path.join(os.path.dirname(__file__), 'static/pictures/' + picture)
                with open(full_path, 'wb') as f:
                    f.write(content)
        # store into database

        res = datalayer.insert('diet', {'did': did, 'name': name, 'price': price, 'base': base, 'cid': cid, 'ord': order, 'description': desc, 'picture': picture})
        if res is None and picture:
            os.remove(os.path.join(os.path.dirname(__file__), 'static/pictures/' + picture))

        data.diet = datalayer.get_all('diet')
        response = {'status': 'ok'}
        self.finish(json_encode(response))


class DietDelHandler(tornado.web.RequestHandler):
    def post(self):
        did = int(json_decode(self.get_argument('did')))
        res = datalayer.get('diet', {'did': did})
        print res
        if res and res[0]:
            picture = res[0]['picture']
            full_path = os.path.join(os.path.dirname(__file__), 'static/pictures/' + picture)
            os.remove(full_path)
            datalayer.delete('diet', {'did': did})
            data.diet = datalayer.get_all('diet')
            response = {'status': 'ok'}
            self.finish(json_encode(response))
            return
        response = {'status': 'err'}
        self.finish(json_encode(response))


class DietDataHandler(tornado.web.RequestHandler):
    def post(self):
        res = datalayer.get_all('diet')
        response = {'status': 'ok', 'diet': res}
        self.finish(json_encode(response))


class DeskAddHandler(tornado.web.RequestHandler):
    def post(self):
        desk = json_decode(self.get_argument('desk'))
        desk = desk.upper()
        res = datalayer.insert('desks', {'desk': desk})
        if res:
            path = os.path.dirname(__file__) + '/static/desks/' + desk + '.png'
            img = qrcode.make(desk)
            img.save(path)

        res = datalayer.get_all('desks')
        data.desks = []
        for row in res:
            data.desks.append(row['desk'])

        response = {'status': 'ok'}
        self.write(json_encode(response))


class DeskDelHandler(tornado.web.RequestHandler):
    def post(self):
        desk = json_decode(self.get_argument('desk'))
        desk = desk.upper()
        res = datalayer.get_all('desks')
        data.desks = []
        for row in res:
            data.desks.append(row['desk'])
        if desk in data.desks:
            path = os.path.dirname(__file__) + '/static/desks/' + desk + '.png'
            os.remove(path)
            data.desks.remove(desk)
            datalayer.delete('desks', {'desk': desk})
        response = {'status': 'ok'}
        self.write(json_encode(response))


class DeskDataHandler(tornado.web.RequestHandler):
    def post(self):
        res = datalayer.get_all('desks')
        data.desks = []
        for row in res:
            data.desks.append(row['desk'])
        response = {'status': 'ok', 'desks': data.desks}
        self.write(json_encode(response))


class DownloadHandler(tornado.web.RequestHandler):
    def post(self):
        self.set_header('Content-Type', 'application/octet-stream')
        self.set_header('Content-Disposition', 'attachment; filename=qrcode.tar')

        dir_path = os.path.dirname(__file__) + '/static/desks'
        files = []
        for d, s, f in os.walk(dir_path):
            files.extend(f)
        tar_path = 'qrcode.tar'
        try:
            os.remove(tar_path)
        except Exception as e:
            pass
        out = tarfile.open(tar_path, 'w')
        try:
            for f in files:

                full_path = dir_path + '/' + f
                out.add(full_path)
        finally:
            out.close()
        with open(tar_path, 'rb') as f:
            while True:
                d = f.read(1024*1024)
                if not d:
                    break
                self.write(d)
        self.finish()


class TarHandler(tornado.web.RequestHandler):
    def post(self):
        dir_path = os.path.dirname(__file__) + '/static/desks'
        files = []
        for d, s, f in os.walk(dir_path):
            files.extend(f)
        tar_path = os.path.dirname(__file__) + '/static/qrcode.tar'
        try:
            if os.path.exists(tar_path):
                os.remove(tar_path)
        except Exception as e:
            pass
        out = tarfile.open(tar_path, mode='w')
        try:
            for f in files:

                full_path = dir_path + '/' + f
                out.add(full_path)
        finally:
            out.close()
        self.finish(json_encode({'status': 'ok'}))


class FacultyAddHandler(tornado.web.RequestHandler):
    def post(self):
        fid = json_decode(self.get_argument('fid'))
        name = json_decode(self.get_argument('name'))
        role = json_decode(self.get_argument('role'))
        password = json_decode(self.get_argument('passwd'))
        datalayer.insert('faculty', {'fid': fid, 'name': name, 'role': role, 'password': password})
        data.faculty = datalayer.get_all('faculty')
        response = {'status': 'ok'}
        self.finish(json_encode(response))


class FacultyDelHandler(tornado.web.RequestHandler):
    def post(self):
        fid = json_decode(self.get_argument('fid'))
        datalayer.delete('faculty', {'fid': fid})
        data.faculty = datalayer.get_all('faculty')
        response = {'status': 'ok'}
        self.finish(json_encode(response))


class FacultyDataHandler(tornado.web.RequestHandler):
    def post(self):
        data.faculty = datalayer.get_all('faculty')
        response = {'status': 'ok', 'faculty': data.faculty}
        self.finish(json_encode(response))


class PeriodHandler(tornado.web.RequestHandler):
    def post(self):
        time_from = json_decode(self.get_argument('from'))
        time_to = json_decode(self.get_argument('to'))
        time_from = util.strtostamp(time_from)
        time_to = util.strtostamp(time_to)
        order_history = datalayer.get_order(time_from, time_to)
        feedback = datalayer.get_feedback(time_from, time_to)
        response = {'status': 'ok', 'order': order_history, 'feedback': feedback}
        self.write(json_encode(response))


class TrendHandler(tornado.web.RequestHandler):
    def post(self):
        num = json_decode(self.get_argument('num'))
        base = json_decode(self.get_argument('base'))
        res = datalayer.get_trend(int(num), base)
        response = {'status': 'ok', 'trend': res}
        self.write(json_encode(response))


class CookInfoHandler(tornado.web.RequestHandler):
    def post(self):
        time_from = json_decode(self.get_argument('from'))
        time_to = json_decode(self.get_argument('to'))
        res = datalayer.get_cookinfo(time_from, time_to)
        response = {'status': 'ok', 'cook': res}
        self.write(json_encode(response))


class OneCookInfoHandler(tornado.web.RequestHandler):
    def post(self):
        time_from = json_decode(self.get_argument('from'))
        time_to = json_decode(self.get_argument('to'))
        fid = json_decode(self.get_argument('fid'))
        res = datalayer.get_onecookinfo(fid, time_from, time_to)
        response = {'status': 'ok', 'onecook': res}
        self.write(json_encode(response))