#!/usr/bin/env python

import tornado.web
import re
import logging

from handlers.base_handler import BaseHandler

class ProfileHandler(BaseHandler):
    
    @tornado.web.authenticated
    def get(self, user=None):
        if user is None:
            user = self.get_secure_cookie("user")
        self.render("profile.html")

    def test_avatar(self, test_file):
        self.r_image = self.re._compile(r".*\.(jpg|jpeg|jpe|png|pns|gif|)")

        if self.r_image.match(test_file):
            pass
        else:
            self.logging.debug('This in not a valid image type')