#!/usr/bin/env python

import tornado.web
import logging

from handlers.base_handler import BaseHandler
import handlers.localization as localization

class LeaderBoardHandler(BaseHandler):
    @tornado.web.authenticated

    def get(self):
        pass