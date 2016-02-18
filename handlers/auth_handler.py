#!/usr/bin/env python

import tornado.web
import logging
import uuid

from handlers.base_handler import BaseHandler
import handlers.localization as localization

class AuthHandler(BaseHandler):

    def prepare(self):
        self.info = ''
        if self.get_cookie('info') in localization.MSG:
            self.info = localization.MSG[self.get_cookie('info')]
        self.set_cookie('info', '')

    def get(self):
        self.render("login.html", info=self.info)

    def post(self):
        # code for registering new users
        if len(self.get_arguments('emailR')) > 0 and len(self.get_arguments('passwordR')) > 0 \
        and len(self.get_arguments('usernameR')) > 0:
            register_status = self.DBI.register(self.get_arguments('usernameR')[0],
                                           self.get_arguments('emailR')[0],
                                           self.get_arguments('passwordR')[0])

            if not register_status:
                self.set_cookie('info', 'SMSG3')
            else:
                self.set_cookie('info', 'SMSG4')
            self.redirect("/auth")
            
        # code for logging in
        if len(self.get_arguments('email')) >0 and len(self.get_arguments('password')) > 0:
            username = self.DBI.authenticate(self.get_arguments('email')[0], self.get_arguments('password')[0])
            if username:
                r_uuid = str(uuid.uuid4())
                self.DBI.update_uuid(username[1], r_uuid)
                self.set_secure_cookie("user", username[1])
                self.set_secure_cookie("uuid", r_uuid)
                self.set_cookie('info', 'SMSG1')
                self.redirect("/")
            else:
                self.set_cookie('info', 'SMSG2')
                self.redirect('/auth')
