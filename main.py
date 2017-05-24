__author__ = 'jerry'

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.iostream
import os

from handlers_common import *
from handlers_manager import *
from tornado.options import define, options

define("port", default=8000, help="run on the given port", type=int)
define("debug", default=False, help="run in debug mode")



myhandlers = [  (r'/', EntryHandler),
                (r'/faculty-login', FacultyLoginHandler),
                (r'/faculty-home', FacultyHomeHandler),
                (r'/manager', ManagerHandler),
                (r'/company-info', CompanyInfoHandler),
                (r'/company-data', CompanyDataHandler),
                (r'/cate-add', CateAddHandler),
                (r'/cate-del', CateDelHandler),
                (r'/cate-data', CateDataHandler),
                (r'/diet-add', DietAddHandler),
                (r'/diet-del', DietDelHandler),
                (r'/diet-data', DietDataHandler),
                (r'/desk-add', DeskAddHandler),
                (r'/desk-del', DeskDelHandler),
                (r'/desk-data', DeskDataHandler),
                (r'/download', DownloadHandler),
                (r'/tar', TarHandler),
                (r'/faculty-add', FacultyAddHandler),
                (r'/faculty-del', FacultyDelHandler),
                (r'/faculty-data', FacultyDataHandler),
                (r'/period', PeriodHandler),
                (r'/trend', TrendHandler),
                (r'/cook-info', CookInfoHandler),
                (r'/one-cook-info', OneCookInfoHandler),
              ]

settings = dict(
                cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
                login_url="/",
                template_path=os.path.join(os.path.dirname(__file__), "templates"),
                static_path=os.path.join(os.path.dirname(__file__), "static"),
                xsrf_cookies=False,
                debug=options.debug,
                )


def main():
    tornado.options.parse_command_line()
    application = tornado.web.Application(myhandlers, **settings)
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()

