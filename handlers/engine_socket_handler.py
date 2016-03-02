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
        """
        self.actions = {
            "/leave": self.DBI.user_left_room,
            "/join": self.DBI.,
            "/create":,
            "/quickjoin":,
            "/ready":
        }
        """

    def get_compression_options(self):
        # Non-None enables compression with default options.
        return {}


    def construct_chat(self, user="System", body="Sorry that command doesn't exist"):
        # returns a message dictionary
        chat = {
            "id": str(uuid.uuid4()),
            "user": user,
            "body": body,
            "time": str(datetime.datetime.now().replace(microsecond=0))
        }
        chat["html"] = tornado.escape.to_basestring(
                    self.render_string("message.html", message=chat))
        return chat
    

    def open(self):
        # Add the user to the dictionaries
        EngineSocketHandler.waiters[self] = self.get_secure_cookie("user")
        EngineSocketHandler.users[self.get_secure_cookie("user")] = self
        logging.debug("Handlers:Socket:Engine:open: "+ str(EngineSocketHandler.users))
        
    @staticmethod
    def inform_room_users(users, chat):
        logging.debug("Handlers:Socket:Engine:IRU Users: "+str(users))
        if users is not None:
            chat["body"] = "/users " + " ".join((str(i[0])+":"+str(i[2])+":"+str(i[3])) for i in users)
            logging.debug(chat["body"])
            #chat["html"] = tornado.escape.to_basestring(
            #    cls.render_string("message.html", message=chat))
            for user in users:
                try:
                    EngineSocketHandler.users[user[0]].write_message(chat)
                except KeyError:
                    logging.exception("Handlers:Socket:Engine: KeyError self.USERS: "+str(EngineSocketHandler.users))
                    
    @staticmethod
    def send_updates(chat, users):
        if users:
            for user in users:
                try:
                    EngineSocketHandler.users[user[0]].write_message(chat)
                except KeyError:
                    logging.exception("Handlers:Socket:Engine: KeyError self.USERS: "+str(EngineSocketHandler.users))


    def on_close(self):
        # remove user from the dictionaries
        del EngineSocketHandler.waiters[self]
        del EngineSocketHandler.users[self.get_secure_cookie("user")]
        # Remove player from his room
        room_id = self.DBI.get_user_room(self.get_secure_cookie("user"))
        self.DBI.user_left_room(self.get_secure_cookie("user"))
        
        # Inform everyone he left
        if room_id:
            users = self.DBI.list_room_users(room_id)
            chat = self.construct_chat(body="A user left this room")
            EngineSocketHandler.inform_room_users(users, chat)
        

    def on_message(self, message):
        parsed = tornado.escape.json_decode(message)
        try:
            if parsed[0] == "/":
                # process request
                logging.debug("Command: " + parsed)
                chat = self.construct_chat()
                parsed = parsed.split()
                
                if parsed[0] == "/votefor":
                    self.DBI.update_score_by_choice_id(self.get_secure_cookie("user"), parsed[1])
                    self.DBI.reset_ready(self.get_secure_cookie("user"))
                
                if parsed[0] == "/choice":
                    
                    room_id = self.DBI.get_user_room(self.get_secure_cookie("user"))
                    if room_id:
                        self.DBI.user_choice(
                            self.get_secure_cookie("user"), parsed[1]
                        )
                        
                        if self.DBI.everyone_chose(room_id):
                            chat["body"] = "/clear"
                            users = self.DBI.list_room_users(room_id)
                            EngineSocketHandler.send_updates(chat, users)
                            if users:
                                for user in users:
                                    user[5] # choice
                                    chat["body"] = "/vote"
                                    chat["data_id"] = str(user[5])
                                    chat["data_body"] = str(self.DBP.get_response_by_id(user[5])[1])
                                    chat["data_html"] = tornado.escape.to_basestring(
                                        self.render_string("vote.html", message=chat))
                                    other_users = self.DBI.get_users_by_diff_choice(room_id, user[5])
                                    for other_user in other_users:
                                        self.users[other_user[0]].write_message(chat)
                                        
                
                if parsed[0] == "/leave":
                    room_id = self.DBI.user_left_room(EngineSocketHandler.waiters[self])
                    
                if parsed[0] == "/create":
                    room_id = self.DBI.create_room_and_join(EngineSocketHandler.waiters[self])

                if parsed[0] == "/join":
                    room_id = self.DBI.join_player_room(
                        EngineSocketHandler.waiters[self], parsed[1]
                        )
                    
                if parsed[0] == "/quickjoin":
                    room_id = self.DBI.quick_join_room(EngineSocketHandler.waiters[self])

                
                if parsed[0] == "/ready":
                    room_id = self.DBI.get_user_room(EngineSocketHandler.waiters[self])
                    if room_id:
                        self.DBI.user_is_ready(EngineSocketHandler.waiters[self])
                        
                        if self.DBI.everyone_is_ready(room_id):
                            opener = self.DBP.get_random_opener()
                            chat["body"] = "/opener"
                            chat["data_id"] = str(opener[0])
                            chat["data_body"] = str(opener[1])
                            chat["data_html"] = tornado.escape.to_basestring(
                                self.render_string("opener.html", message=chat))
                            
                            users = self.DBI.list_room_users(room_id)
                            EngineSocketHandler.send_updates(chat, users)

                            r_users = self.DBI.list_room_users(room_id)
                            responses = self.DBP.generate_random_responses(len(r_users))
                            logging.debug("Number of responses : "+str(len(responses)))
                            for user in r_users:
                                user_choices = "#"
                                for option in range(self.DBP.options_per_player):
                                    data = responses.pop()
                                    user_choices += str(data[0])+"#"
                                    chat["body"] = "/choice"
                                    chat["data_id"] = str(data[0])
                                    chat["data_body"] = str(data[1])
                                    chat["data_html"] = tornado.escape.to_basestring(
                                        self.render_string("choice.html", message=chat))
                                    self.users[user[0]].write_message(chat)
                                    
                                    self.DBI.user_possible_choices(
                                        user[0], user_choices
                                    )
                            
                        
                if room_id:
                    users = self.DBI.list_room_users(room_id)
                    EngineSocketHandler.inform_room_users(users, chat)
                    current_room = self.DBI.get_user_room(EngineSocketHandler.waiters[self])
                    chat["body"] = "/channel -1"
                    if current_room:
                        chat["body"] = "/channel " + str(current_room)
                    
                chat["html"] = tornado.escape.to_basestring(
                    self.render_string("message.html", message=chat))
                
                self.write_message(chat)
                
            else:
                room_id = self.DBI.get_user_room(EngineSocketHandler.waiters[self])
                users = self.DBI.list_room_users(room_id)
                EngineSocketHandler.send_updates(
                    self.construct_chat(
                        user=EngineSocketHandler.waiters[self],
                        body=parsed
                    ),
                    users
                )
                
        except IndexError:
            logging.exception("Handlers:Socket:Engine: Message which caused indexError: "+str(message))
        
        except Exception:
            logging.exception("Handlers:Socket:Engine: Unknown error")
