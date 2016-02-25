#!/usr/bin/env python
import tornado.websocket
import logging
import uuid
from engine.bidict import biDict
import datetime

class EngineSocketHandler(tornado.websocket.WebSocketHandler):
    
    waiters = {}
    users = {}

    def initialize(self, database, puns):
        self.DBI = database
        self.DBP = puns

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
                    
    def inform_room_about(self, room_id, chat):
        users = self.DBI.list_room_users(room_id)
        if users:
            
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
        try:
            if parsed[0] == "/":
                # process request
                logging.debug("Command: " + parsed)
                chat = {
                    "id": str(uuid.uuid4()),
                    "user": "System",
                    "body": "Sorry that command doesn't exist",
                    "time": str(datetime.datetime.now().replace(microsecond=0))
                }
                parsed = parsed.split()
                if parsed[0] == "/leave":
                    room_id = self.DBI.user_left_room(self.get_secure_cookie("user"))
                    if room_id > 0:
                        self.inform_room_users(room_id, chat)
                        chat["body"] = "/channel -1"
                
                if parsed[0] == "/create":
                    room_id = self.DBI.create_room_and_join(EngineSocketHandler.waiters[self])
                    if room_id:
                        self.inform_room_users(room_id, chat)
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
                        
                if parsed[0] == "/ready":
                    room_id = self.DBI.get_user_room(EngineSocketHandler.waiters[self])
                    if room_id:
                        self.DBI.user_is_ready(EngineSocketHandler.waiters[self])
                        chat["body"] = "/isready " + EngineSocketHandler.waiters[self]
                        self.inform_room_about(room_id, chat)
                        
                        if self.DBI.everyone_is_ready(room_id):
                            opener = self.DBP.get_random_opener()
                            chat["body"] = "/opener"
                            chat["opener_id"] = str(opener[0])
                            chat["opener_body"] = str(opener[1])
                            chat["opener_html"] = tornado.escape.to_basestring(
                                self.render_string("opener.html", message=chat))
                            
                            self.inform_room_about(room_id, chat)
                            
                
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
        except IndexError:
            logging.error("Message which caused indexError")
            logging.error(str(message))
