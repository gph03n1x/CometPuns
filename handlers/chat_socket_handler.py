#!/usr/bin/env python
import tornado.websocket
import logging
import uuid

class ChatSocketHandler(tornado.websocket.WebSocketHandler):

    waiters = {}
    cache = []
    cache_size = 200

    def initialize(self, database):
        self.DBI = database

    def get_compression_options(self):
        # Non-None enables compression with default options.
        return {}

    def open(self):
        ChatSocketHandler.waiters[self] = self.get_secure_cookie("user")

    def on_close(self):
        del ChatSocketHandler.waiters[self]
        # Remove player from lfg
        self.DBI.update_match_making(self.get_secure_cookie("user"))


    @classmethod
    def update_cache(cls, chat):
        cls.cache.append(chat)
        if len(cls.cache) > cls.cache_size:
            cls.cache = cls.cache[-cls.cache_size:]

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
        parsed = tornado.escape.json_decode(message)
        chat = {
            "id": str(uuid.uuid4()),
            "user": ChatSocketHandler.waiters[self],
            "body": parsed,
            }
        chat["html"] = tornado.escape.to_basestring(
            self.render_string("message.html", message=chat))

        ChatSocketHandler.update_cache(chat)
        ChatSocketHandler.send_updates(chat)
