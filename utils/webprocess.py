import requests
import threading
from lib import lang
from handlers import log, orderlog

class WebRequestThread(threading.Thread):
    """docstring for WebRequestThread"""
    def __init__(self, queue):
        super(WebRequestThread, self).__init__()
        self.queue = queue
        print '%s process is init' % self.getName()
    
    def run(self):
        while True:
            try:
                url = self.queue.get()
                headers = {'User-Agent': 'form lemon'}
                r = requests.get(url, headers=headers, timeout=15)
                orderlog.info('%s: forwardurl:[%s],[%s]' % (self.getName(), url, r.status_code))
            except:
                log.error("forwardTo request error:%s" % lang.trace_back())
