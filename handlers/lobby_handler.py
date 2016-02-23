import tornado.web
import logging

from handlers.base_handler import BaseHandler
import handlers.localization as localization


class LobbyHandler(BaseHandler):


    @tornado.web.authenticated
    def get(self):
        # fetches user room id
        roomid = str(self.DBI.get_user_room(self.get_current_user()))
        # renders the lobby
        self.render("lobby.html", info=self.info, room_id=roomid, user=self.get_current_user())
    
