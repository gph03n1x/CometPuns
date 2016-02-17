#!/usr/bin/env python
import Queue
import threading



class Engine(object):
    def __init__(self, dbi):
        self.dbi = dbi

    def validator(self):

        pass

    def cycle(self):
        dbi.cursor.execute("SELECT * FROM matchstatus WHERE completed=0")
        res = dbi.cursor.fetchall()

