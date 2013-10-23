from base import BaseHandler
from handlers import orderlog, log
from utils import unionapi
from lib import lang
from lib.base import route




@route(r'/spimpl/smsdb/yihui/receive')
class YihuiSmsHandler(BaseHandler):
    def get(self):
        status = 1
        try:
            remote_ip = self.request.remote_ip
            # if remote_ip != '211.151.66.84' and remote_ip != '127.0.0.1':
            #     log.info("[%s], errorip:[%s], query:[%s]" % ('ivr-zyhl1001-2,5', remote_ip, self.request.query))
            #     self.write('')
            #     return
            linkid = self.get_argument("Linkid", None)
            cmdid = self.get_argument("MO_Msg", None)
            mobile = self.get_argument("statphone", None)
            status = self.get_argument("stat", None)
            starttime = lang.now()
            endtime = starttime

            if cmdid == '02042':
                servicecode = "smsdb-gzyh1001-1"
            else:
                orderlog.info("receive:[%s],[%s],[%s],[%s],[%s],error" % (
                    linkid, 0, servicecode, self.request.uri, self.request.query))
                return
            status = 1 if status == 'DELIVRD' else 0
            if status != 1:
                orderlog.info("receive:[%s],[%s],[%s],[%s],[%s],error" % (
                    linkid, 0, servicecode, self.request.uri, self.request.query))
                return

            serviceOrderId = lang.uuid()
            msg = dict(
                serviceOrderId=serviceOrderId,
                servicecode=servicecode,
                status=status,
                statusstring='',
                mobile=mobile,
                starttime=starttime,
                endtime=endtime,
                ivrtotal=1,
            )

            orderlog.info("receive:[%s],[%s],[%s],[%s],[%s],ok" % (
                linkid, serviceOrderId, servicecode, self.request.uri, self.request.query))
            unionapi.serviceProcess(msg)

        except:
            orderlog.error("receive:[%s],[%s],err: %s" % (self.request.uri, self.request.query, lang.trace_back()))
            self.finish("0")
        finally:
            self.finish('ok')
