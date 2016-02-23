#!/usr/bin/env python

import tornado.web
import logging

from handlers.base_handler import BaseHandler

class ProfileHandler(BaseHandler):
    
    @tornado.web.authenticated
    def get(self, user=None):
        if user is None:
            user = self.get_secure_cookie("user")
        self.render("profile.html")
