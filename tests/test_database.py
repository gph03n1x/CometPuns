#!/usr/bin/env python
import unittest, sqlite3
from engine.database import databaseInteractions

class TestdatabaseInteractions(unittest.TestCase):

    def setUp(self):
        self.dbi = databaseInteractions("database/crisk.db")
        self.dbi.execute_raw("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username, email, password)")
        self.dbi.execute_raw("CREATE TABLE IF NOT EXISTS lfmatch (username, status)")
        self.dbi.execute_raw("CREATE TABLE IF NOT EXISTS matchstatus (id INTEGER PRIMARY KEY, turn, teams, details)")
        self.dbi.execute_raw("CREATE TABLE IF NOT EXISTS chatroom (id INTEGER PRIMARY KEY, username, message, ts timestamp)")

    def test_auth(self):
        self.dbi.register("john", "giannispapcod7@gmail.com", "123")
        self.assertEqual(self.dbi.authenticate("giannispapcod7", "123"), None )



suite = unittest.TestLoader().loadTestsFromTestCase(TestdatabaseInteractions)
unittest.TextTestRunner(verbosity=2).run(suite)
