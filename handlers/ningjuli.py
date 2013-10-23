from base import BaseHandler
from handlers import orderlog, log
from utils import unionapi
from lib import lang
from lib.base import route


@route(r'/spimpl/ivr/hnjl/receive')
class NingjuliIvrHandler(BaseHandler):
    def get(self):
        servicecode = "ivr-hnjl1003"
        status = 1
        try:
            remote_ip = self.request.remote_ip
            # if remote_ip != '211.151.66.84' and remote_ip != '127.0.0.1':
            #     log.info("[%s], errorip:[%s], query:[%s]" % (servicecode, remote_ip, self.request.query))
            #     self.write('')
            #     return

            mobile = self.get_argument("mobile", None)
            orderdest = self.get_argument("lnum", None)
            starttime = self.get_argument("starttime", None)
            endtime = self.get_argument("endtime", None)
            ivrtotal = self.get_argument("lmin", None)
            ivrtotal = lang.num(ivrtotal)
            serviceOrderId = lang.uuid()
            msg = dict(
                serviceOrderId=serviceOrderId,
                servicecode=servicecode,
                status=status,
                statusstring='',
                mobile=mobile,
                orderdest=orderdest,
                starttime=starttime,
                endtime=endtime,
                ivrtotal=ivrtotal,
            )

            orderlog.info(
                "receive:[%s],[%s],[%s],[%s],ok" % (serviceOrderId, servicecode, self.request.uri, self.request.query))
            unionapi.serviceProcess(msg)

        except:
            orderlog.error("receive:[%s],[%s],err" % (self.request.uri, self.request.query))
            self.finish("0")
        finally:
            self.finish('ok')


@route(r'/spimpl/smsdb/hnjl/receive')
class NingjuliSmsHandler(BaseHandler):
    def get(self):
        status = 1
        try:
            remote_ip = self.request.remote_ip
            # if remote_ip != '211.151.66.84' and remote_ip != '127.0.0.1':
            #     log.info("[%s], errorip:[%s], query:[%s]" % ('ivr-zyhl1001-2,5', remote_ip, self.request.query))
            #     self.write('')
            #     return
            linkid = self.get_argument("linkid", None)
            cmdid = self.get_argument("content", None)
            mobile = self.get_argument("mobile", None)
            status = self.get_argument("state", None)
            starttime = lang.now()
            endtime = starttime

            if cmdid == 'DMM1':
                servicecode = "smsdb-hnjl001"
            elif cmdid == 'DMT1':
                servicecode = "smsdb-hnjl002"
            elif cmdid == 'DMM6':
                servicecode = "smsdb-hnjl003"
            elif cmdid == 'DMM7':
                servicecode = "smsdb-hnjl004"
            elif cmdid == 'DMM9':
                servicecode = "smsdb-hnjl005"
            elif cmdid == 'HYT4':
                servicecode = "smsdb-hnjl-2-1"
            elif cmdid == 'DMT3':
                servicecode = "smsdb-hnjl006"
            elif cmdid == 'HYT3':
                servicecode = "smsdb-hnjl-2-2"
            elif cmdid == 'HYT1':
                servicecode = "smsdb-hnjl-2-3"
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
