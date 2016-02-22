import tornado.web
import logging

from handlers.base_handler import BaseHandler
import handlers.localization as localization


class LobbyHandler(BaseHandler):
    @tornado.web.authenticated

    def prepare(self):
        self.info = ''
        if self.get_cookie('info') in localization.MSG:
            self.info = localization.MSG[self.get_cookie('info')]
        self.set_cookie('info', '')
        
    @tornado.web.authenticated
    def get(self):
        roomid = str(self.DBI.get_user_room(self.get_current_user()))
        self.render("lobby.html", info=self.info, room_id=roomid, user=self.get_current_user())
    
    @tornado.web.authenticated
    def post(self):
        self.DBI.quick_join_room(self.get_current_user())
        roomid = str(self.DBI.get_user_room(self.get_current_user()))
        self.render("lobby.html", info=self.info, room_id=roomid, user=self.get_current_user())
