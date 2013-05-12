from base import BaseHandler
from utils import unionapi
from lib.base import route
from handlers import db, log, webRequestQueue

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

@route(r'/common/clearData')
class ClearData(BaseHandler):
    def get(self):
        sql = "update lem_webowner set today_count=0";
        db.execute(sql);
        sql = "update webowner_province set today_count=0";
        db.execute(sql);
        log.info(" clear data ok.")

import tornado
#@route(r'.*')
class PageNotFoundHandler(BaseHandler):
    def get(self):
        raise tornado.web.HTTPError(404)
