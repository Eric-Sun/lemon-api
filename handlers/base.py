# -*- encoding: utf-8 -*-
from lib.session import session
from lib.base import BaseHandler

class BaseHandler(BaseHandler):

    @session
    def get_current_user(self):
        return None
