#!/usr/bin/env python


import sys
try:
    sys.argv[1]
except IndexError:
    pass
else:
    import tests
    sys.exit(0)



import os.path
import tornado.web
import tornado.ioloop
import tornado.websocket
import json
import logging
import uuid

import handlers.localization as localization

from handlers.base_handler import BaseHandler
from handlers.auth_handler import AuthHandler
from handlers.admin_handler import AdminHandler
from handlers.lobby_handler import LobbyHandler
from handlers.board_handler import BoardHandler
from handlers.chat_socket_handler import ChatSocketHandler

from engine.security import databaseInteractions
from engine.engine import Engine

print "[*] Connecting with the database ..."
DBI = databaseInteractions("database/crisk.db")
DBI.execute_raw("CREATE TABLE IF NOT EXISTS puns (id INTEGER PRIMARY KEY, message)")
DBI.execute_raw("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username, email, password)")
DBI.execute_raw("CREATE TABLE IF NOT EXISTS user_lfg_status (username, lfg_id)")
DBI.execute_raw("CREATE TABLE IF NOT EXISTS match_status (id INTEGER PRIMARY KEY, turn, teams, details, completed)")
DBI.execute_raw("CREATE TABLE IF NOT EXISTS lfg (id INTEGER PRIMARY KEY, players, num, match_key)")
print "[*] Conection successfull !!!"

Engine(DBI)

settings = {
    "cookie_secret": "sVvW58QWgjAld7DK2FnOUzZLmoQgvlqDIh6mPYC8HDWanE5GqYy6v3Uu2ivKG36O",
    "login_url": "/auth",
}

application = tornado.web.Application(
    [
        (r"/", LobbyHandler, dict(database=DBI)),
        (r"/auth", AuthHandler, dict(database=DBI)),
        (r"/board", BoardHandler, dict(database=DBI)),
        (r"/admin", AdminHandler, dict(database=DBI)),
        (r"/chatsocket", ChatSocketHandler, dict(database=DBI)),

    ],
    debug=True,
    template_path = os.path.join(os.path.dirname(__file__), "resources/templates"),
    static_path = os.path.join(os.path.dirname(__file__), "resources/static"),
    **settings
)

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.current().start()
