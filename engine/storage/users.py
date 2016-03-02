#!/usr/bin/env python
import sqlite3
import hashlib
import datetime
import ast
import inspect
import ConfigParser
import logging
import random

config = ConfigParser.RawConfigParser() 
config.read('cometpuns.cfg') 


class databaseInteractions:
    def __init__(self, dbfile):
        # creates a class attribute with a connection
        # to the database file
        self.connection = sqlite3.connect(dbfile)
        # creates an attribute which includes the cursor
        self.cursor = self.connection.cursor()
        # sets the max users allowed by the system in a channel
        self.max_users_per_room = config.get('GENERAL', 'MAX_USERS_PER_ROOM')


    def get_user_room(self, player_name):
        # searches the user_room for a room_id
        # associated with the given username
        self.cursor.execute("SELECT * FROM user_room WHERE username=?",(player_name,))
        user_room = self.cursor.fetchone()
        if user_room:
            # if there are results we return them
            return user_room[1]
        # else the user doesn't exist because
        # if he did we would return id = -1 since
        # since he isn't inside a channel
        return None
    
    def get_users_by_diff_choice(self, room_id, choice_id):
        self.cursor.execute("SELECT * FROM user_room WHERE room_id=? AND choice!=?", (room_id, choice_id))
        users = self.cursor.fetchall()
        if users:
            # if there are users then we return them
            return users
        # else we return None hence the channel doesn't exist
        return None
    
    
    def is_ready(self, player_name):
        self.cursor.execute("SELECT * FROM user_room WHERE username=?",(player_name,))
        result = self.cursor.fetchone()
        if result is not None:
            if int(result[3]) == 1:
                return True
        return False
    
    
    
    def update_score_by_choice_id(self, player_name, choice_id):
        room_id = self.get_user_room(player_name)
        
        if room_id is not None and self.is_ready(player_name):
            self.cursor.execute("UPDATE user_room SET score=score+1 WHERE room_id=? AND choice=?", (room_id, choice_id))
            self.cursor.execute("UPDATE user_room SET ready=0 WHERE username=?", (player_name,))
        
        
    def user_possible_choices(self, player_name, choices):
        self.execute_raw("UPDATE user_room SET choices=?, choice=0 WHERE username=?",(choices, player_name))
        
        
    def user_choice(self, player_name, choice):
        self.execute_raw("UPDATE user_room SET choice=? WHERE username=?",(choice, player_name))
        
    
    def everyone_chose(self, room_id):
        users = self.list_room_users(room_id)
        self.cursor.execute("SELECT * FROM game_room WHERE id=?",(room_id,))
        user_count = self.cursor.fetchone()
        if not user_count or not users:
            return False
        
        choice_count = 0
        
        for user in users:
            if int(user[5]) != 0:
                choice_count = choice_count + 1
                
        if choice_count == int(user_count[1]):
            return True
        return False
        

    def user_left_room(self, player_name):
        # we get user's current room
        user_room = self.get_user_room(player_name)
        # if there isn't any we return -1
        if not user_room:
            return -1
        
        # we set him as not ready 
        self.execute_raw("UPDATE user_room SET ready=0 WHERE username=?",(player_name, ))
        # if the room's id isn't -1
        if int(user_room) != -1:
            # we subtract 1 from the game_room users
            self.cursor.execute("SELECT * FROM game_room WHERE id=?", (user_room,))
            room = self.cursor.fetchone()
            self.execute_raw("UPDATE game_room SET users=? WHERE id=?", (int(room[1])-1, room[0]))
            # we now associate the user with an empty room
            self.execute_raw("UPDATE user_room SET room_id=-1 WHERE username=?",(player_name, ))
            if int(room[1])-1 == 0:
                # if the game_room has 0 users we remove it from the database
                self.execute_raw("DELETE FROM game_room WHERE users=0")
            # we return the room's id 
            return room[0]


    def quick_join_room(self, player_name):
        # we remove the user from his current room
        self.user_left_room(player_name)
        # we search for rooms which are open to join
        # and haven't reached yet max users
        self.cursor.execute("SELECT * FROM game_room WHERE (users<=? and open='TRUE') ORDER BY users DESC",
                            (self.max_users_per_room,))
        room = self.cursor.fetchone()
        if room:
            # if there is such a room we increment its users
            # and we associate the user with his new room
            room_id = room[0]
            self.execute_raw("UPDATE game_room SET users=? WHERE id=?", (int(room[1])+1, room[0]))
            self.execute_raw("UPDATE user_room SET room_id=?, ready=0 WHERE username=?",(room[0], player_name))
        else:
            # else we create a new one and we join it ourselves
            room_id = self.create_room_and_join(player_name)
        return room_id


    def create_room_and_join(self, player_name):
        # we remove the user from his current room
        self.user_left_room(player_name)
        # we create a new room for him
        room_id = self.execute_raw(
            "INSERT INTO game_room (users, open, details) VALUES (1, 'TRUE', ?)", (str({}), )
                                )
        # and we are associating him with it
        self.execute_raw("UPDATE user_room SET room_id=? WHERE username=?",(str(room_id), player_name))
        return room_id
    
    
    def list_room_users(self, room_id):
        # Executes an sql query which fetches
        # all users in a room
        self.cursor.execute("SELECT * FROM user_room WHERE room_id=?",(room_id,))
        users = self.cursor.fetchall()
        if users:
            # if there are users then we return them
            return users
        # else we return None hence the channel doesn't exist
        return None
    
    
    def join_player_room(self, player_name, target_player):
        # Fetches the id of the room from the user
        # we want to join
        room_id = self.get_user_room(target_player)
        if room_id:
            # if he is in a room then we leave our current room
            # and then we join the room with the new id
            self.user_left_room(player_name)
            self.execute_raw("UPDATE game_room SET users=users+1 WHERE id=?", (room_id, ))
            self.execute_raw("UPDATE user_room SET room_id=? WHERE username=?",(room_id, player_name))
            return room_id
        
        
    def invite_player_room(self, player_name, target_player):
        pass
        

    def user_is_ready(self, player_name):
        self.execute_raw("UPDATE user_room SET ready=1 WHERE username=?",(player_name, ))
    

    def everyone_is_ready(self, room_id):
        users = self.list_room_users(room_id)
        self.cursor.execute("SELECT * FROM game_room WHERE id=?",(room_id,))
        user_count = self.cursor.fetchone()
        if not user_count or not users:
            return False
        
        ready_count = 0
        for user in users:
            logging.debug("Engine:Storage:Users: "+str(int(user[3])))
            if int(user[3]) == 1:
                ready_count = ready_count + 1
                
        logging.debug("Engine:Storage:Users: ready_count "+str(ready_count))
        logging.debug("Engine:Storage:Users: user_count[1] "+str(user_count[1]))
        if ready_count == int(user_count[1]):
            return True
        return False
            

    def authenticate(self, email, password):
        # Fetches any row in the database where
        # the email and the password match
        self.cursor.execute("SELECT * FROM users WHERE email=? AND password=?", (email,password))
        return self.cursor.fetchone()
    
    
    def get_user_uuid(self, username):
        # Fetches the current uuid
        self.cursor.execute("SELECT uuid FROM users WHERE username=?", (username,))
        return self.cursor.fetchone()
    
    
    def update_uuid(self, username, _uuid):
        # Update the uuid field of the user
        self.execute_raw("UPDATE users SET uuid=? WHERE username=?",(str(_uuid),username))


    def register(self, username, email, password):
        # Checks if there are already entries with the same email or the same username
        self.cursor.execute("SELECT * FROM users WHERE email=? OR username=?", (email,username))
        if str(self.cursor.fetchone()) == "None":
            # If there aren't any then we create a new user row along with a user_room association
            self.execute_raw("INSERT INTO users (username, email, password) VALUES (?,?,?)", (username, email, password))
            self.execute_raw("INSERT INTO user_room (username, room_id, score, ready, choices, choice, vote) VALUES (?,-1,0,0,0,0,0)", (username,))
            return True
        # return false since the user already exists
        return False


    def execute_raw(self, *query):
        # method for executing queries and fetching the
        # lastrowid so we can do that in one line and we
        # can avoid cluttering
        self.cursor.execute(*query)
        self.connection.commit()
        return self.cursor.lastrowid
