#!/usr/bin/env python
import logging.config
import os

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from . import config
from .account import handler as account_handler

app = tornado.web.Application([
    (r'/register', account_handler.RegisterUserHandler, None, 'register'),
    (r'/login', account_handler.LoginHandler, None, 'login'),
    (r'/isLogined', account_handler.IsLoginedHandler),
    (r'/logout', account_handler.LogoutHandler, None, 'logout'),
    (r'/account/edit', account_handler.EditUserHandler),
    (r'/account/info', account_handler.AccountInfoHandler),
], **config.APP)

if __name__ == '__main__':
    tornado.options.define('port', default=8888, type=int,
                           help='listen port')
    tornado.options.define('numprocs', default=0, type=int,
                           help='number of subprocess to fork')
    tornado.options.options.logging = None
    tornado.options.parse_command_line()

    if not os.path.exists(config.PATH_LOG):
        os.makedirs(config.PATH_LOG)

    if not os.path.exists(config.PATH_UPLOAD):
        os.makedirs(config.PATH_UPLOAD)

    logging.config.dictConfig(config.LOGGING)

    server = tornado.httpserver.HTTPServer(app, xheaders=True)
    if config.DEBUG:
        server.listen(tornado.options.options.port)
    else:
        server.bind(tornado.options.options.port)
        server.start(tornado.options.options.numprocs)
    tornado.ioloop.IOLoop.current().start()
