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
        
    @tornado.web.authenticated
    def get(self):
        self.DBI.cursor.execute("SELECT * FROM user_lfg_status WHERE username=?",(self.get_current_user(),))
        uls_res = str(self.DBI.cursor.fetchone()) + "\n"
        self.DBI.cursor.execute("SELECT * FROM lfg")
        uls_res += str(self.DBI.cursor.fetchone())
        self.render("lobby.html", info=self.info, lfg=uls_res)
    
    @tornado.web.authenticated
    def post(self):
        self.DBI.update_match_making(self.get_current_user())
        self.DBI.cursor.execute("SELECT * FROM user_lfg_status WHERE username=?",(self.get_current_user(),))
        uls_res = str(self.DBI.cursor.fetchone()) + "\n"
        self.DBI.cursor.execute("SELECT * FROM lfg")
        uls_res += str(self.DBI.cursor.fetchone())
        self.render("lobby.html", info=self.info, lfg=uls_res)
