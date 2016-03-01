#!/usr/bin/env python


import sys 
try:
    # checks the index of system arguments
    sys.argv[1]
except IndexError:
    # if there is an index error there aren't any
    # system arguments passed to the program
    pass
else:
    # runs the code inside tests/__init__.py
    import tests
    sys.exit(0)
    
    
import json # http://stackoverflow.com/questions/383692/what-is-json-and-why-would-i-use-it
import uuid # for generating random id
import logging # gia tin dimiourgeia logs
import os.path # gia tin dimiourgeia paths se templates kai css
import tornado.web 
import tornado.ioloop
import tornado.websocket
import ConfigParser

logging.basicConfig(filename='error.log', level=logging.DEBUG)
logging.debug("==========Starting new instance==========")

import handlers.localization as localization # afora cookie messages

# kanei import handlers oi opoioi xeirizontai ta urls
from handlers.base_handler import BaseHandler
from handlers.auth_handler import AuthHandler
from handlers.admin_handler import AdminHandler
from handlers.lobby_handler import LobbyHandler
from handlers.board_handler import BoardHandler
from handlers.profile_handler import ProfileHandler
from handlers.engine_socket_handler import EngineSocketHandler

# to engine security einai misleading 
# kai tha eprepe na einai database stuff mono
from engine.storage.users import databaseInteractions
from engine.storage.puns import databasePuns
# to engine pou tha trexei sto background
from engine.engine import Engine

# anoigma tou arxeiou pou xrisimopoieitai os config
config = ConfigParser.RawConfigParser() 
config.read('cometpuns.cfg') 



print "[*] Connecting with the database ..."
# anoigma arxeiwn vasis dedomenon
DBP = databasePuns(config.get('GENERAL', 'PUNS_FILE'))
DBI = databaseInteractions(config.get('GENERAL', 'DATABASE_FILE'))

# dimiourgeia sql tables an den iparxoun idi
DBI.execute_raw("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username, email, password, uuid, role, avatar, bio, score INTEGER)")
DBI.execute_raw("CREATE TABLE IF NOT EXISTS user_room (username, room_id, score INTEGER, ready, choices, choice, vote)")
DBI.execute_raw("CREATE TABLE IF NOT EXISTS game_room (id INTEGER PRIMARY KEY, users INTEGER, open, details)")


print "[+] Conection successfull with database: " + config.get('GENERAL', 'DATABASE_FILE')
print "[+] Conection successfull with puns: " + config.get('GENERAL', 'DATABASE_FILE')
# ekinisi toy engine pou tha trexei sto background
# otan ilopoiithei
Engine(DBI)

# to cookie_secret string einai ena tixaio alpharithmitiko
# pou xrisimopoieitai gia na einai kriptografimena ta cookies
# to login_url einai to url sto opoio tha ginei redirect an o xristis
# den einai sindedemenos
settings = {
    "cookie_secret": "sVvW58QWgjAld7DK2FnOUzZLmoQgvlqDIh6mPYC8HDWanE5GqYy6v3Uu2ivKG36O",
    "login_url": "/auth",
    "xsrf_cookies": True,
}

# sindeei sto app ta urls me tous handlers tous
# kai vriskei ta templates kai ta static (css , js)
application = tornado.web.Application(
    [
        (r"/", LobbyHandler, dict(database=DBI)),
        (r"/auth", AuthHandler, dict(database=DBI)),
        (r"/board", BoardHandler, dict(database=DBI)),
        (r"/admin", AdminHandler, dict(database=DBI)),
        (r"/profile/([^/]+)", ProfileHandler, dict(database=DBI)),
        (r"/engine", EngineSocketHandler, dict(database=DBI, puns=DBP)),

    ],
    debug=True,
    template_path = os.path.join(os.path.dirname(__file__), "resources/templates"),
    static_path = os.path.join(os.path.dirname(__file__), "resources/static"),
    **settings
)

if __name__ == "__main__":
    # ean ekteleitai to programma os kirio programma
    # tote ksekinaei o http server na akouei stin port
    # pou vrisketai sto config
    # kai ksekinaei to IOLoop
    application.listen(config.getint('GENERAL', 'PORT'))
    print "[*] Listening at port: " + config.get('GENERAL', 'PORT')
    tornado.ioloop.IOLoop.current().start()
