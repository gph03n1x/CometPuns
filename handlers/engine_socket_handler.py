#!/usr/bin/env python
import tornado.websocket
import logging
import uuid
from engine.bidict import biDict
import datetime

class EngineSocketHandler(tornado.websocket.WebSocketHandler):
    
    waiters = {}
    users = {}

    def initialize(self, database):
        self.DBI = database

    def get_compression_options(self):
        # Non-None enables compression with default options.
        return {}

    def open(self):
        EngineSocketHandler.waiters[self] = self.get_secure_cookie("user")
        EngineSocketHandler.users[self.get_secure_cookie("user")] = self
        

    def inform_room_users(self, room_id, chat):
        users = self.DBI.list_room_users(room_id)
        if users:
            chat["body"] = "/users " + " ".join((str(i[0])+":"+str(i[2])) for i in users)
            logging.debug(chat["body"])
            chat["html"] = tornado.escape.to_basestring(
                self.render_string("message.html", message=chat))
            for i in users:
                try:
                    EngineSocketHandler.users[i[0]].write_message(chat)
                except KeyError:
                    pass
                    
        
    def on_close(self):
        del EngineSocketHandler.waiters[self]
        del EngineSocketHandler.users[self.get_secure_cookie("user")]
        # Remove player from his room
        room_id = self.DBI.get_user_room(self.get_secure_cookie("user"))
        self.DBI.user_left_room(self.get_secure_cookie("user"))
        
        # Inform everyone he left
        if room_id:
            chat = {
                "id": str(uuid.uuid4()),
                "user": "System",
                "body": "Sorry that command doesn't exist",
                "time": str(datetime.datetime.now().replace(microsecond=0))
            }
            self.inform_room_users(room_id, chat)
        
        

    @classmethod
    def send_updates(cls, chat):
        for waiter in cls.waiters:
            try:
                waiter.write_message(chat)
            except:
                logging.error("Error sending message", exc_info=True)

    def on_message(self, message):
        parsed = tornado.escape.json_decode(message)
        logging.debug("message " + parsed)
        if parsed[0] == "/":
            # process request
            logging.debug("process " + parsed[1:7])
            chat = {
                "id": str(uuid.uuid4()),
                "user": "System",
                "body": "Sorry that command doesn't exist",
                "time": str(datetime.datetime.now().replace(microsecond=0))
            }
            parsed = parsed.split()
            
            if parsed[0] == "/create":
                room_id = self.DBI.create_room_and_join(EngineSocketHandler.waiters[self])
                chat["body"] = "/channel " + str(room_id)
                
                
            if parsed[0] == "/join":
                room_id = self.DBI.join_player_room(
                    EngineSocketHandler.waiters[self], parsed[1]
                    )
                if room_id:
                    self.inform_room_users(room_id, chat)
                    chat["body"] = "/channel " + str(room_id)
                    
            if parsed[0] == "/quickjoin":
                room_id = self.DBI.quick_join_room(EngineSocketHandler.waiters[self])
                if room_id:
                    self.inform_room_users(room_id, chat)
                    chat["body"] = "/channel " + str(room_id)
                        
            
            chat["html"] = tornado.escape.to_basestring(
                self.render_string("message.html", message=chat))
            
            self.write_message(chat)
            
        else:
            
            chat = {
                "id": str(uuid.uuid4()),
                "user": EngineSocketHandler.waiters[self],
                "body": parsed,
                "time": str(datetime.datetime.now().replace(microsecond=0))
                }
 
            chat["html"] = tornado.escape.to_basestring(
                self.render_string("message.html", message=chat))
            EngineSocketHandler.send_updates(chat)
            
            
            
