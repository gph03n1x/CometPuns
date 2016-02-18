import tornado.web
import logging

from handlers.base_handler import BaseHandler
import handlers.localization as localization


class BoardHandler(BaseHandler):
    @tornado.web.authenticated

    def get(self):
        pass

    def post(self):
        pass
