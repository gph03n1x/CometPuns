#!/usr/bin/env python
import Queue
import threading


class Engine(threading.Thread):
    def __init__(self, dbi):
        # inheritance of the python tread
        threading.Thread.__init__(self)
        self.dbi = dbi


    def run(self):
        # override of the run class
        # which does nothing at the moment
        try:
            pass
        except Exception:
            # log error & restart the run
            self.run()
