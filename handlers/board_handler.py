import tornado.web
import logging

from handlers.base_handler import BaseHandler
import handlers.localization as localization

from engine.nations import NationsToList

class BoardHandler(BaseHandler):
    @tornado.web.authenticated

    def initialize(self, database):
        self.DBI = database

    def get(self):
        pass

    def post(self):
        pass
