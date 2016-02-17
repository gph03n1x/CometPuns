#!/usr/bin/env python
import sqlite3
import hashlib
import datetime
import ast
import inspect

class databaseInteractions:
    def __init__(self, dbfile):
        self.connection = sqlite3.connect(dbfile)
        self.cursor = self.connection.cursor()


    def update_match_making(self, player_name):

        self.cursor.execute("SELECT * FROM user_lfg_status WHERE username=?",(player_name,))
        uls_res = self.cursor.fetchone()

        if uls_res[1] == -1: # User not in lfg
            self.cursor.execute("SELECT * FROM lfg WHERE num<>6 ORDER BY num DESC")
            res = self.cursor.fetchone()

            if res is None:
                self.cursor.execute("INSERT INTO lfg (players,num) VALUES (?,?)", (str([]), 0))
                self.connection.commit()
                self.cursor.execute("SELECT * FROM lfg WHERE num<>6 ORDER BY num DESC")
                res = self.cursor.fetchone()

            players_d = ast.literal_eval(res[1])
            players_d.append(player_name)
            self.cursor.execute("UPDATE lfg SET players=?,num=? WHERE id=?",(str(players_d), str(int(res[2])+1), res[0]))
            self.connection.commit()
            self.cursor.execute("UPDATE user_lfg_status SET lfg_id=? WHERE username=?",(res[0], player_name))
            self.connection.commit()
            return "LMSG1"

        else: # User wants to leave lfg
            self.cursor.execute("SELECT * FROM lfg WHERE id=?", (uls_res[1],))
            res = self.cursor.fetchone()
            players_d = ast.literal_eval(res[1])
            players_d.remove(player_name)
            self.cursor.execute("UPDATE lfg SET players=?,num=? WHERE id=?",(str(players_d), str(int(res[2])-1), res[0]))
            self.connection.commit()
            self.cursor.execute("UPDATE user_lfg_status SET lfg_id=-1 WHERE username=?",(player_name,))
            self.connection.commit()
            return "LMSG2"

    def authenticate(self, email, password):
        #print "Auth call for \'{0}\'".format(email)
        self.cursor.execute("SELECT * FROM users WHERE email=? AND password=?", (email,password))
        return self.cursor.fetchone()

    def register(self, username, email, password):
        self.cursor.execute("SELECT * FROM users WHERE email=?", (email,))
        if str(self.cursor.fetchone()) == "None":
            self.cursor.execute("INSERT INTO users (username, email, password) VALUES (?,?,?)", (username, email, password))
            self.connection.commit()
            self.cursor.execute("INSERT INTO user_lfg_status (username, lfg_id) VALUES (?,0)", (username,))
            self.connection.commit()
            return True
        else:
            return False

    def execute_raw(self, query):
        self.cursor.execute(query)
        self.connection.commit()


