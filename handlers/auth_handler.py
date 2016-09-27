#!/usr/bin/env python

import tornado.web
import logging
import uuid

from handlers.base_handler import BaseHandler
import handlers.localization as localization

class AuthHandler(BaseHandler):


    def get(self):
        # if the user is already logged in then
        if self.get_current_user():
            # he gets redirected to the lobby
            self.redirect("/")
        # else the handler renders the login page
        self.render("login.html", info=self.info)


    def post(self):
        # the inputs *R are filled this means that the
        # user wants to register to the website
        if len(self.get_arguments('emailR')) > 0 and len(self.get_arguments('passwordR')) > 0 \
        and len(self.get_arguments('usernameR')) > 0:
            # attempting to register
            register_status = self.DBI.register(self.get_arguments('usernameR')[0],
                                           self.get_arguments('emailR')[0],
                                           self.get_arguments('passwordR')[0])

            if not register_status:
                # if the register returns false this means that
                # there is already one user with the same email
                # or the same username
                self.set_cookie('info', 'SMSG3')
            else:
                # else he successfulled registered
                self.set_cookie('info', 'SMSG4')
            # go back to /auth so that the user can log in
            self.redirect("/auth")

        # if the email and the password inputs are filled
        # we are going to attempt an authentication
        # TODO: code seems broken here.
        if len(self.get_arguments('email')) >0 and len(self.get_arguments('password')) > 0:
            # trying to authenticate with the database
            username = self.DBI.authenticate(self.get_arguments('email')[0], self.get_arguments('password')[0])
            print("L0")
            if username:
                print("L1")
                # if username is not None then
                # the user got authenticated
                # generate a random uuid
                r_uuid = str(uuid.uuid4())

                # set the random uuid for the user
                self.DBI.update_uuid(username[1], r_uuid)
                # update the cookies
                self.set_secure_cookie("user", username[1])
                self.set_secure_cookie("uuid", r_uuid)
                self.set_cookie('info', 'SMSG1')
                # redirect to the lobby
                self.redirect("/")
            else:
                # inform the user his password or username
                # were wrong and redirect back to /auth
                self.set_cookie('info', 'SMSG2')
                self.redirect('/auth')

        else:
            # if the user didnt logged in or registered
            # then he is trying to logout , so we clear
            # the cookies and we get him back to /auth
            self.clear_all_cookies()
            self.redirect('/auth')
