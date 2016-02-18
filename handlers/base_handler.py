#!/usr/bin/env python
import tornado.web

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        # apokriptografei to cookie "user" kai to epistrefei
        return self.get_secure_cookie("user")
