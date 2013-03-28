from base import BaseHandler
from handlers import orderlog, log
from utils import unionapi
from lib import lang
from lib.base import route


@route(r'/spimpl/ivr/125966800/receive\.jsp')
class ZYHandler(BaseHandler):
    def get(self):
        servicecode = "ivr-zyhl1001"
        status = 1
        try:
            remote_ip = self.request.remote_ip
            if remote_ip != '211.151.66.84' and remote_ip != '127.0.0.1':
                log.info("[%s], errorip:[%s], query:[%s]" % (servicecode, remote_ip, self.request.query))
                self.write('')
                return

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

            orderlog.info("receive:[%s],[%s],[%s],[%s],ok" % (serviceOrderId, servicecode, self.request.uri, self.request.query))
            unionapi.serviceProcess(msg)

        except:
            orderlog.error("receive:[%s],[%s],err" % (self.request.uri, self.request.query))
        finally:
            self.finish('1')


@route(r'/spimpl/ivr/125966860/receive')
class ZYIVR2Handler(BaseHandler):
    def get(self):
        servicecode = "ivr-zyhl1001-2"
        status = 1
        try:
            remote_ip = self.request.remote_ip
            if remote_ip != '211.151.66.84' and remote_ip != '127.0.0.1':
                log.info("[%s], errorip:[%s], query:[%s]" % (servicecode, remote_ip, self.request.query))
                self.write('')
                return

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

            orderlog.info("receive:[%s],[%s],[%s],[%s],ok" % (serviceOrderId, servicecode, self.request.uri, self.request.query))
            unionapi.serviceProcess(msg)

        except:
            orderlog.error("receive:[%s],[%s],err" % (self.request.uri, self.request.query))
        finally:
            self.finish('1')


@route(r'/spimpl/smsdb/10658032/receive')
class ZY2Handler(BaseHandler):
    def get(self):
        status = 1
        try:
            remote_ip = self.request.remote_ip
            # if remote_ip != '211.151.66.84' and remote_ip != '127.0.0.1':
            #     log.info("[%s], errorip:[%s], query:[%s]" % ('ivr-zyhl1001-2,5', remote_ip, self.request.query))
            #     self.write('')
            #     return
            linkid = self.get_argument("linkid", None)
            cmdid = self.get_argument("cmdid", None)
            mobile = self.get_argument("mobileid", None)
            status = self.get_argument("state", None)
            starttime = lang.now()
            endtime = starttime

            if cmdid == 'HYT':
                servicecode = "smsdb-zyhl1001-2-1"
            elif cmdid == 'HYT2':
                servicecode = "smsdb-zyhl1001-2"
            elif cmdid == 'DMT2':
                servicecode = "smsdb-zyhl1001-5"
            elif cmdid == 'DMT4':
                servicecode = "smsdb-zyhl1001-5-2"
            elif cmdid == 'DMT5':
                servicecode = "smsdb-zyhl1001-5-3"
            elif cmdid == 'DMT6':
                servicecode = "smsdb-zyhl1001-5-4"
            elif cmdid == 'DMM4':
                servicecode = "smsdb-zyhl1001-5-5"
            elif cmdid == 'DMM3':
                servicecode = "smsdb-zyhl1001-5-6"
            else:
                orderlog.info("receive:[%s],[%s],[%s],[%s],[%s],error" % (linkid, 0, servicecode, self.request.uri, self.request.query))
                return
            status = 1 if status == 'DELIVRD' else 0
            if status != 1:
                orderlog.info("receive:[%s],[%s],[%s],[%s],[%s],error" % (linkid, 0, servicecode, self.request.uri, self.request.query))
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

            orderlog.info("receive:[%s],[%s],[%s],[%s],[%s],ok" % (linkid, serviceOrderId, servicecode, self.request.uri, self.request.query))
            unionapi.serviceProcess(msg)

        except:
            orderlog.error("receive:[%s],[%s],err: %s" % (self.request.uri, self.request.query, lang.trace_back()))
        finally:
            self.finish('1')
