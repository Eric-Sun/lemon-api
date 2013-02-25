from base import BaseHandler
from utils import unionapi
from lib.base import route

@route(r'/common/reloadCacheApi')
class RefreshCacheHandler(BaseHandler):
    def get(self):
        flag = self.get_argument("lucas", None)
        if(flag != "1"):
            return

        unionapi.initBasic()
        webownerScale = unionapi.getWebownerScale(10, 1000)
        if webownerScale :
            offBase = webownerScale.get("offbase")
            offNo = webownerScale.get("offno")
            self.finish('ok--%d-%d' % (offNo, offBase))
        else:
            self.finish('')

import tornado
#@route(r'.*')
class PageNotFoundHandler(BaseHandler):
    def get(self):
        raise tornado.web.HTTPError(404)
