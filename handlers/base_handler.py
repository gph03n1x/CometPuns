#!/usr/bin/env python
import tornado.web

class BaseHandler(tornado.web.RequestHandler):
    
    def initialize(self, database):
        self.DBI = database
        
    def get_current_user(self):
        # apokriptografei to cookie "user" kai to epistrefei
        if self.get_secure_cookie("user"):
            #print self.DBI.get_user_uuid(self.get_secure_cookie("user"))
            if self.DBI.get_user_uuid(self.get_secure_cookie("user"))[0] == self.get_secure_cookie("uuid"):
                return self.get_secure_cookie("user")
        return None
