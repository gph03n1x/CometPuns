#!/usr/bin/env python
import Queue
import threading


class Engine(threading.Thread):
    def __init__(self, dbi):
        threading.Thread.__init__(self)
        self.dbi = dbi

    def validator(self):

        pass

    def run(self):
        try:
            self.dbi.cursor.execute("SELECT * FROM matchstatus WHERE completed=0")
            res = self.dbi.cursor.fetchall()
        
        except Exception:
            # log error & restart the run
            self.run()
