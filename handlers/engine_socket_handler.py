#!/usr/bin/env python
import tornado.websocket
import logging
import uuid
from engine.bidict import biDict
import datetime

class EngineSocketHandler(tornado.websocket.WebSocketHandler):
    
    waiters = {}

    def initialize(self, database):
        self.DBI = database

    def get_compression_options(self):
        # Non-None enables compression with default options.
        return {}

    def open(self):
        EngineSocketHandler.waiters[self] = self.get_secure_cookie("user")

    def on_close(self):
        del EngineSocketHandler.waiters[self]
        # Remove player from lfg
        self.DBI.user_left_room(self.get_secure_cookie("user"))

    @classmethod
    def send_updates(cls, chat):
        logging.info("sending message to %d waiters", len(cls.waiters))
        for waiter in cls.waiters:
            try:
                waiter.write_message(chat)
            except:
                logging.error("Error sending message", exc_info=True)

    def on_message(self, message):
        logging.info("got message %r", message)
        if message[0] == "/":
            # process request
            chat = {
                "id": str(uuid.uuid4()),
                "user": "System",
                "body": parsed,
                "time": datetime.datetime.now()
            }
            chat["html"] = tornado.escape.to_basestring(
                self.render_string("message.html", message=chat))
            
            self.write_message(chat)
            
        else:
            parsed = tornado.escape.json_decode(message)
            
            chat = {
                "id": str(uuid.uuid4()),
                "user": EngineSocketHandler.waiters[self],
                "body": parsed,
                "time": str(datetime.datetime.now())
                }
 
            chat["html"] = tornado.escape.to_basestring(
                self.render_string("message.html", message=chat))
            EngineSocketHandler.send_updates(chat)
            
            
            
