#!/usr/bin/env python

import tornado.web
import logging

from handlers.base_handler import BaseHandler
import handlers.localization as localization

class AdminHandler(BaseHandler):
    @tornado.web.authenticated

    def initialize(self, database):
        self.DBI = database

    def get(self):
        pass
