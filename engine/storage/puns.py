import sqlite3
import hashlib
import datetime
import ast
import inspect
import ConfigParser
import logging
import random


class databasePuns:
    
    def __init__(self, dbfile):
        # creates a class attribute with a connection
        # to the database file
        self.connection = sqlite3.connect(dbfile)
        # creates an attribute which includes the cursor
        self.cursor = self.connection.cursor()
        self.createTables()
        # sets the max users allowed by the system in a channel
        self.openers = self.count_openers()
        self.responses = self.count_openers()
        if self.openers < 1 or self.responses < 1:
            import sys
            sys.exit("[-]Please add openers and responses first")
        
        
    def createTables(self):
        self.execute_raw("CREATE TABLE IF NOT EXISTS openers (id INTEGER PRIMARY KEY, content)")
        self.execute_raw("CREATE TABLE IF NOT EXISTS responses (id INTEGER PRIMARY KEY, content)")
        
        
    def count_openers(self):
        self.cursor.execute("SELECT Count(*) FROM openers")
        rows = self.cursor.fetchone()
        return rows[0]
    
    
    def count_responses(self):
        self.cursor.execute("SELECT Count(*) FROM openers")
        rows = self.cursor.fetchone()
        return rows[0]
    
    
    def get_random_opener(self):
        random_id = random.randint(1, self.openers)
        self.cursor.execute("SELECT * FROM openers WHERE id=?",(random_id,))
        return self.cursor.fetchone()
    
    
    def get_random_response(self):
        random_id = random.randint(1, self.responses)
        self.cursor.execute("SELECT * FROM responses WHERE id=?",(random_id,))
        return self.cursor.fetchone()
    
    
    def execute_raw(self, *query):
        # method for executing queries and fetching the
        # lastrowid so we can do that in one line and we
        # can avoid cluttering
        self.cursor.execute(*query)
        self.connection.commit()
        return self.cursor.lastrowid#!/usr/bin/env python

class databasePuns:
    
    def __init__(self, dbfile):
        # creates a class attribute with a connection
        # to the database file
        self.connection = sqlite3.connect(dbfile)
        # creates an attribute which includes the cursor
        self.cursor = self.connection.cursor()
        self.createTables()
        # sets the max users allowed by the system in a channel
        self.openers = self.count_openers()
        self.responses = self.count_openers()
        if self.openers < 1 or self.responses < 1:
            import sys
            sys.exit("Please add openers and responses first")
        
        
    def createTables(self):
        self.execute_raw("CREATE TABLE IF NOT EXISTS openers (id INTEGER PRIMARY KEY, content)")
        self.execute_raw("CREATE TABLE IF NOT EXISTS responses (id INTEGER PRIMARY KEY, content)")
        
        
    def count_openers(self):
        self.cursor.execute("SELECT Count(*) FROM openers")
        rows = self.cursor.fetchone()
        return rows[0]
    
    
    def count_responses(self):
        self.cursor.execute("SELECT Count(*) FROM openers")
        rows = self.cursor.fetchone()
        return rows[0]
    
    
    def get_random_opener(self):
        random_id = random.randint(1, self.openers)
        self.cursor.execute("SELECT * FROM openers WHERE id=?",(random_id,))
        return self.cursor.fetchone()
    
    
    def get_random_response(self):
        random_id = random.randint(1, self.responses)
        self.cursor.execute("SELECT * FROM responses WHERE id=?",(random_id,))
        return self.cursor.fetchone()
    
    
    def execute_raw(self, *query):
        # method for executing queries and fetching the
        # lastrowid so we can do that in one line and we
        # can avoid cluttering
        self.cursor.execute(*query)
        self.connection.commit()
        return self.cursor.lastrowid