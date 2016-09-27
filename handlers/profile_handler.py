#!/usr/bin/env python

import tornado.web
#import urllib2
import logging

from handlers.base_handler import BaseHandler

class ProfileHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self, user=None):
        if user is None:
            user = self.get_secure_cookie("user").decode()
        self.render("profile.html")

"""
    def is_image_valid(self, url):

        response = urllib2.urlopen(HeadRequest(url))
        maintype = response.headers['Content-Type'].split(';')[0].lower()

        if maintype not in ('Image/png', 'Image/pns', 'Image/gif', 'Image/jpg', 'Image/jpeg', 'Image/jpe'):
            logging.debug('invalid type of image')
            return False

        return True


class HeadRequest(urllib2.Request):
    def get_method(self):
        return 'HEAD'
"""
