import sqlite3
import logging
import random


class databasePuns:
    def __init__(self, dbfile, options_per_player=5):
        # creates a class attribute with a connection
        # to the database file
        self.connection = sqlite3.connect(dbfile)
        # creates an attribute which includes the cursor
        self.cursor = self.connection.cursor()
        self.createTables()
        # number of options per player
        self.options_per_player = int(options_per_player)
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


    def get_response_by_id(self, response_id):
        self.cursor.execute("SELECT * FROM responses WHERE id=?",(response_id,))
        return self.cursor.fetchone()



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


    def generate_random_responses(self, number_of_players):
        # Create a population of ids from 0<=id<=self.responses
        # and fetch a sample of number_of_players*self.options_per_player
        logging.debug(number_of_players)
        logging.debug(number_of_players*self.options_per_player)
        id_pool = random.sample(range(self.responses), number_of_players*self.options_per_player)
        result_pool = []
        for random_id in id_pool:
            # for each id we fetch their response from the
            # database and we added in the result list
            self.cursor.execute("SELECT * FROM responses WHERE id=?",(random_id,))
            result_pool.append(self.cursor.fetchone())
        return result_pool


    def execute_raw(self, *query):
        # method for executing queries and fetching the
        # lastrowid so we can do that in one line and we
        # can avoid cluttering
        self.cursor.execute(*query)
        self.connection.commit()
        return self.cursor.lastrowid


if __name__ == '__main__':
    pun = databasePuns("database/puns.db")
