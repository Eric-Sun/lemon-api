from base import BaseHandler
from handlers import orderlog, log
from lib import lang
from lib.base import route
from utils import unionapi
import datetime
import StringIO
from xml.dom import minidom

@route(r'/spimpl/ivr/lbxz/receive')
class LBXZHandler(BaseHandler):
    def get(self):
        servicecode = "ivr-lbxz1002-1"
        try:
            remote_ip = self.request.remote_ip
            if remote_ip != '221.174.25.62' and remote_ip != '221.174.25.59' and remote_ip != '127.0.0.1':
                log.info("[%s], errorip:[%s], query:[%s]" % (servicecode, remote_ip, self.request.query))
                self.write('')
                return

            mobile = self.get_argument("ivrsrcnum", None)
            orderdest = self.get_argument("ivrdesnum", None)
            starttime = self.get_argument("stime", None)
            starttime = datetime.datetime.strptime(starttime, '%Y%m%d%H%M%S')
            ivrtotal = self.get_argument("feetime", None)
            ivrtotal = lang.num(ivrtotal)
            endtime = starttime + datetime.timedelta(minutes=ivrtotal)
            endtime = endtime.strftime('%Y-%m-%d %H:%M:%S')
            starttime = starttime.strftime('%Y-%m-%d %H:%M:%S')
            serviceOrderId=lang.uuid()

            msg = dict(
                    serviceOrderId=serviceOrderId,
                    servicecode=servicecode,
                    status=1,
                    statusstring='',
                    mobile=mobile,
                    orderdest=orderdest,
                    starttime=starttime,
                    endtime=endtime,
                    ivrtotal=ivrtotal,
                    ivrunit=60,
                )

            orderlog.info("receive:[%s],[%s],[%s],[%s],ok" % (serviceOrderId, servicecode, self.request.query))
            #unionapi.serviceProcess(msg)
        except:
            orderlog.error("receive:[%s],[%s],[%s],err" % (servicecode, self.request.query, lang.trace_back()))
        finally:
            self.finish('OK')


    def post(self):
        servicecode = "ivr-lbxz1002"
        content = self.request.body
        try:
            remote_ip = self.request.remote_ip
            if remote_ip != '221.174.25.62' and remote_ip != '221.174.25.59' and remote_ip != '127.0.0.1':
                log.info("[%s], errorip:[%s], query:[%s]" % (servicecode, remote_ip, content))
                self.write('')
                return

            ssock = StringIO.StringIO(content)
            xmldoc = minidom.parse(ssock)
            ssock.close()
            callNum = xmldoc.getElementsByTagName('callNum')[0].firstChild.data
            calledNum = xmldoc.getElementsByTagName('calledNum')[0].firstChild.data
            #serviceId = xmldoc.getElementsByTagName('serviceId')[0].firstChild.data
            #fee = xmldoc.getElementsByTagName('fee')[0].firstChild.data
            #tradeId = xmldoc.getElementsByTagName('tradeId')[0].firstChild.data
            tradeId=lang.uuid()
            startTime = xmldoc.getElementsByTagName('startTime')[0].firstChild.data
            starttime = datetime.datetime.strptime(startTime, '%Y%m%d%H%M%S')
            endTime = xmldoc.getElementsByTagName('endTime')[0].firstChild.data
            endtime = datetime.datetime.strptime(endTime, '%Y%m%d%H%M%S')
            #md5str = xmldoc.getElementsByTagName('md5')[0].firstChild.data
            #siteType = xmldoc.getElementsByTagName('siteType')[0].firstChild.data
            #serviceKey = '3ecdad1d-40e0-4a5e-bc85-e35b649ef9a7'
            #verify = hashlib.md5('%s%s%s' % (callNum, endTime, serviceKey)).hexdigest()

            msg = dict(
                    serviceOrderId=tradeId,
                    servicecode=servicecode,
                    status=1,
                    statusstring='',
                    mobile=callNum,
                    orderdest=calledNum,
                    starttime=starttime,
                    endtime=endtime,
                    ivrtotal=30,
                    ivrunit=60,
                )
            orderlog.info("receive:[%s],[%s],[%s],[%s],ok" % (tradeId, servicecode, self.request.uri, content))
            unionapi.serviceProcess(msg)
        except:
            orderlog.error("receive:[%s],[%s],[%s],err" % (servicecode, content, lang.trace_back()))
        finally:
            self.finish('<?xml version = "1.0" encoding="utf-8"?><spserviceresp><status>ok</status></spserviceresp>')

@route(r'/spimpl/ivr/hnxl/receive')
class HNXLHandler(BaseHandler):
    def get(self):
        servicecode = "ivr-hnxl1003"
        try:
            report = self.get_argument("report", None)
            if(report != 'DELIVRD'):
                return

            mobile = self.get_argument("mobile", None)
            orderdest = self.get_argument("spnum", None)
            momsg = self.get_argument("msg", None)
            if len(momsg) > 5:
                momsg = momsg[5:]
            else:
                momsg = '0'
            orderdest = orderdest+momsg
            ivrtotal = 30
            endtime = datetime.datetime.now()
            endtime = endtime.strftime('%Y-%m-%d %H:%M:%S')
            starttime = datetime.datetime.now()
            starttime = starttime.strftime('%Y-%m-%d %H:%M:%S')
            serviceOrderId=lang.uuid()

            msg = dict(
                    serviceOrderId=serviceOrderId,
                    servicecode=servicecode,
                    status=1,
                    statusstring='',
                    mobile=mobile,
                    orderdest=orderdest,
                    starttime=starttime,
                    endtime=endtime,
                    ivrtotal=ivrtotal,
                    ivrunit=9999,
                )

            orderlog.info("receive:[%s],[%s],[%s],[%s],ok" % (serviceOrderId, servicecode, orderdest, self.request.query))
            unionapi.serviceProcess(msg)
        except:
            orderlog.error("receive:[%s],[%s],[%s],err" % (servicecode, self.request.query, lang.trace_back()))
        finally:
            self.finish('OK')
