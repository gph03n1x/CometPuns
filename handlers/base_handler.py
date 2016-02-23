#!/usr/bin/env python
import tornado.web
import handlers.localization as localization


class BaseHandler(tornado.web.RequestHandler):
    
    def initialize(self, database):
        # Associates the handler with the database object
        self.DBI = database
        
    def prepare(self):
        # resets the info attribute
        self.info = ''
        
        if self.get_cookie('info') in localization.MSG:
            # matches the string inside "info" with a complete
            # message from localization.MSG
            # sets the info attribute with the message
            self.info = localization.MSG[self.get_cookie('info')]
        # clears the cookie
        self.set_cookie('info', '')    
        
    def get_current_user(self):
        # verifies the existance of the of the cookie "user"
        # and that, this user does have an uuid
        if self.get_secure_cookie("user") and self.DBI.get_user_uuid(self.get_secure_cookie("user")):
            # if the user uuid is the same with the one in the cookie
            # which means this is the most recent authenticated device
            if self.DBI.get_user_uuid(self.get_secure_cookie("user"))[0] == self.get_secure_cookie("uuid"):
                # then return the username
                return self.get_secure_cookie("user")
        # else this user session has expired or
        # he hasn't registered yet
        return None
