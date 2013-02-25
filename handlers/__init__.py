# -*- encoding: utf-8 -*-
import settings as app_config
appConfig = app_config.app_config
log = app_config.log
orderlog = app_config.orderlog

from lib import lemondb
db = lemondb.connect(app_config.database, **app_config.database_types[app_config.database])

from utils import webprocess
from Queue import Queue
webRequestQueue = Queue()
webRequestThreadObj1 = webprocess.WebRequestThread(webRequestQueue)
webRequestThreadObj2 = webprocess.WebRequestThread(webRequestQueue)
webRequestThreadObj1.start()
webRequestThreadObj2.start()

from utils import unionapi
unionapi.initBasic()

from lib.base import Application
from handlers import index, lanbo, zhongya

application = Application(**app_config.settings)
application.load_module(index)
application.load_module(lanbo)
application.load_module(zhongya)
