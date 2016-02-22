#!/usr/bin/env python
import sqlite3
import hashlib
import datetime
import ast
import inspect
import ConfigParser
import logging

config = ConfigParser.RawConfigParser() 
config.read('cometpuns.cfg') 

class databaseInteractions:
    
    def __init__(self, dbfile):
        self.connection = sqlite3.connect(dbfile)
        self.cursor = self.connection.cursor()
        self.max_users_per_room = config.get('GENERAL', 'MAX_USERS_PER_ROOM')
        
    def get_user_room(self, player_name):
        self.cursor.execute("SELECT * FROM user_room WHERE username=?",(player_name,))
        user_room = self.cursor.fetchone()
        if user_room:
            return user_room[1]
        return None
        
    def user_left_room(self, player_name):
        user_room = self.get_user_room(player_name)
        
        if not user_room:
            return -1
        
        if int(user_room) != -1:
            self.cursor.execute(
                "SELECT * FROM game_room WHERE id=?", (user_room,)
                            )
            
            room = self.cursor.fetchone()
            self.execute_raw("UPDATE game_room SET users=? WHERE id=?", (int(room[1])-1, room[0]))
            self.execute_raw("UPDATE user_room SET room_id=-1 WHERE username=?",(player_name, ))
            if int(room[1]-1) == 0:
                self.execute_raw("DELETE FROM game_room WHERE users=0")
            return room[0]

    def quick_join_room(self, player_name):
        self.user_left_room(player_name)
        self.cursor.execute("SELECT * FROM game_room WHERE (users<=? and open='TRUE') ORDER BY users DESC",
                            (self.max_users_per_room,))
        room = self.cursor.fetchone()
        if room:
            room_id = room[0]
            self.execute_raw("UPDATE game_room SET users=? WHERE id=?", (int(room[1])+1, room[0]))
            self.execute_raw("UPDATE user_room SET room_id=? WHERE username=?",(room[0], player_name))
        else:
            room_id = create_room_and_join(player_name)
        return room_id
        
    def create_room_and_join(self, player_name):
        self.user_left_room(player_name)
        room_id = self.execute_raw(
            "INSERT INTO game_room (users, open, details) VALUES (1, 'TRUE', ?)", (str({}), )
                                )
        self.execute_raw("UPDATE user_room SET room_id=? WHERE username=?",(str(room_id), player_name))
        return room_id
    
    def list_room_users(self, room_id):
        self.cursor.execute("SELECT * FROM user_room WHERE room_id=?",(room_id,))
        users = self.cursor.fetchall()
        if users:
            return users
        return None
    
    def join_player_room(self, player_name, target_player):
        
        room_id = self.get_user_room(target_player)
        if room_id:
            self.user_left_room(player_name)
            self.execute_raw("UPDATE game_room SET users=users+1 WHERE id=?", (room_id, ))
            self.execute_raw("UPDATE user_room SET room_id=? WHERE username=?",(room_id, player_name))
            return room_id
        
        
    def invite_player_room(self, player_name, target_player):
        pass
        
        

    def authenticate(self, email, password):
        #print "Auth call for \'{0}\'".format(email)
        self.cursor.execute("SELECT * FROM users WHERE email=? AND password=?", (email,password))
        return self.cursor.fetchone()
    
    
    def get_user_uuid(self, username):
        self.cursor.execute("SELECT uuid FROM users WHERE username=?", (username,))
        return self.cursor.fetchone()
    
    
    def update_uuid(self, username, _uuid):
        self.execute_raw("UPDATE users SET uuid=? WHERE username=?",(str(_uuid),username))


    def register(self, username, email, password):
        self.cursor.execute("SELECT * FROM users WHERE email=?", (email,))
        if str(self.cursor.fetchone()) == "None":
            self.execute_raw("INSERT INTO users (username, email, password) VALUES (?,?,?)", (username, email, password))
            self.execute_raw("INSERT INTO user_room (username, room_id, score) VALUES (?,-1,0)", (username,))
            return True
        else:
            return False


    def execute_raw(self, *query):
        self.cursor.execute(*query)
        self.connection.commit()
        return self.cursor.lastrowid


