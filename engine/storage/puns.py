import sqlite3
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
            # This means our database is empty
            import sys
            sys.exit("[-]Please add openers and responses first")
        
        
    def createTables(self):
        # creates sql tables
        self.execute_raw("CREATE TABLE IF NOT EXISTS openers (id INTEGER PRIMARY KEY, content)")
        self.execute_raw("CREATE TABLE IF NOT EXISTS responses (id INTEGER PRIMARY KEY, content)")
        
        
    def count_openers(self):
        # counts the number of openers there are in the database
        self.cursor.execute("SELECT Count(*) FROM openers")
        rows = self.cursor.fetchone()
        return rows[0]
    
    
    def count_responses(self):
        # counts the number of responses there are in the database
        self.cursor.execute("SELECT Count(*) FROM openers")
        rows = self.cursor.fetchone()
        return rows[0]
    
    
    def get_random_opener(self):
        # generates a random number between 1 and the number of rows
        # and then we fetch the row with id = generater number
        random_id = random.randint(1, self.openers)
        self.cursor.execute("SELECT * FROM openers WHERE id=?",(random_id,))
        return self.cursor.fetchone()
    
    
    def get_random_response(self):
        # generates a random number between 1 and the number of rows
        # and then we fetch the row with id = generater number
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