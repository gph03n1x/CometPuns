import tornado.web
import logging

from handlers.base_handler import BaseHandler
import handlers.localization as localization


class LobbyHandler(BaseHandler):
    @tornado.web.authenticated

    def initialize(self, database):
        self.DBI = database

    def prepare(self):
        self.info = ''
        if self.get_cookie('info') in localization.MSG:
            self.info = localization.MSG[self.get_cookie('info')]
        self.set_cookie('info', '')
    def get(self):
        self.render("lobby.html", info=self.info)

    def post(self):
        DBI.update_match_making(self.get_current_user())
        self.render("lobby.html", info=self.info)
