import os

mysql_settings = dict(
            host="localhost",
            user="lemon",
            passwd="lemon001)(",
            db="lemon",
)

database_types = dict(
    mysql=mysql_settings
)

app_config = dict(
       
)

database = 'mysql'

settings = dict(
            port=7001,
            debug=True,
            autoescape=None,
            xsrf_cookies=False,
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            cookie_secret='32oETzKXQAGaYdkL5gExGeJJFuYh7EQnp4XdTP1o',
            login_url="",
)

logdir = '/data0/logs/service'

import logging
import logging.handlers
orderlog = logging.getLogger("orderlog")
hdlr = logging.handlers.TimedRotatingFileHandler('%s/order' % logdir, 'D', 1, 30)
hdlr.suffix = "%Y%m%d.log"
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s', '%Y-%m-%d %H:%M:%S')
hdlr.setFormatter(formatter)
orderlog.addHandler(hdlr)
orderlog.setLevel(logging.INFO)

log = logging.getLogger("log")
hdlr = logging.handlers.TimedRotatingFileHandler('%s/service' % logdir, 'D', 1, 30)
hdlr.suffix = "%Y%m%d.log"
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s', '%Y-%m-%d %H:%M:%S')
hdlr.setFormatter(formatter)
log.addHandler(hdlr)
log.setLevel(logging.INFO)
console = logging.StreamHandler()
log.addHandler(console)
