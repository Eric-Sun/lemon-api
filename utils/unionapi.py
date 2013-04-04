from handlers import db, log, webRequestQueue
from thread import allocate_lock
from lib import lang
import math

lock = allocate_lock()
adownerDic = dict()
webownerScaleDic = dict()
webownerServiceInfoDic = dict()
webownerMsgCountDic = dict()
whitelist = ''


def initBasic():
    global adownerDic, webownerScaleDic, whitelist, lock, webownerMsgCountDic
    log.info('init basic start')

    adownerList = db.query(
        'SELECT pid, gateway, servicefee, ownerfee, servicecode, ordercode, orderdest from lem_adowner_code where status = 1')
    lock.acquire()
    adownerDic.clear
    for adowner in adownerList:
        adownerDic[adowner.servicecode] = adowner
    lock.release()

    webownerScaleList = db.query('SELECT pid, wid, offbase, offno from lem_webowner_scale where status = 1')
    lock.acquire()
    webownerScaleDic.clear
    for webownerScale in webownerScaleList:
        webownerScaleDic["%s-%s" % (webownerScale.pid, webownerScale.wid)] = webownerScale
    lock.release()

    webownerServiceInfoList = db.query('SELECT wid, channel, serviceurl from lem_webowner_serviceinfo where status = 1')
    lock.acquire()
    webownerServiceInfoDic.clear
    for webownerServiceInfo in webownerServiceInfoList:
        webownerServiceInfoDic["%s-%s" % (webownerServiceInfo.wid, webownerServiceInfo.channel)] = webownerServiceInfo
    lock.release()

    msgCountList = db.query('select wid,msg_count from lem_webowner')
    lock.acquire()
    webownerMsgCountDic.clear()
    for msgCount in msgCountList:
        webownerMsgCountDic[msgCount.wid] = msgCount.msg_count
    lock.release()


whitelist = db.get('SELECT brief from lem_news where id = 162')
if whitelist:
    whitelist = whitelist.brief
else:
    whitelist = ''

log.info('init basic end')


def getAdownerCode(servicecode):
    return adownerDic.get(servicecode)


def getWebownerServiceUrl(wid, channel):
    serviceinfo = webownerServiceInfoDic.get('%s-%s' % (wid, channel))
    if serviceinfo:
        return serviceinfo.get('serviceurl')
    else:
        return None


def getWebownerScale(pid, wid):
    return webownerScaleDic.get('%s-%s' % (pid, wid))


def serviceProcess(msg):
    try:
        pid = 10
        wid = 1000
        channel = ""
        adid = "1000"

        servicecode = msg.get('servicecode')
        mobile = msg.get('mobile')
        feeFlag = 1
        adownerCode = getAdownerCode(servicecode)
        if adownerCode is None:
            log.info("feecenter servicecode is null: " + servicecode + ". adownerDic = " + str(adownerDic))
            adownerCode = dict()

        pid = adownerCode.get("pid")
        gateway = adownerCode.get("gateway")
        ordercode = adownerCode.get('ordercode')
        orderdest = adownerCode.get('orderdest')
        serviceOrderId = msg["serviceOrderId"]
        serviceSubTime = lang.now()
        if pid == 10:
            orderdest = msg.get('orderdest')
            webowner = db.get("select wid, channel from lem_ivr_info where orderdest = %s", orderdest)
            if webowner:
                wid = webowner.wid
                channel = webowner.channel
        elif pid == 11:
            webowner = db.get("select wid, channel from lem_ivr_info where orderdest = %s", orderdest + ordercode)
            if webowner:
                wid = webowner.wid
                channel = webowner.channel
        else:
            order = None
            try:
                order = db.get(
                    "select * from Lez_sms_orderlog where mobile = ? and servicecode = ? order by subtime desc limit 1",
                    mobile, servicecode)
                if order:
                    orderid = order.get('id')
                    db.execute("update sms_order_log set flag = 1 where flag = 0 and id='" + orderid + "'")
            except:
                log.error("feecenter id error:%s" % lang.trace_back())

            if order:
                wid = order.get('wid')
                channel = order.get('channel')
                adid = order.get('adid')

        if not isWhiteMobile(mobile) and isWebNeedDeduct(pid, wid):
            feeFlag = 0

        servicefee = adownerCode.get("servicefee")
        ownerfee = adownerCode.get("ownerfee")
        totalincome = 0
        feeincome = 0

        if pid == 10:
            starttime = msg.get('starttime')
            endtime = msg.get('endtime')
            ivrtotal = msg.get('ivrtotal')
            records = int(math.ceil(float(ivrtotal) / msg.get('ivrunit', 180)))
            totalincome = records * servicefee
            feeincome = records * ownerfee
            sql = "insert lez_ivr_detail(id,wid,channel,mobile,servicecode,orderdest,starttime,endtime,total,totalincome, feeincome, feeflag, subtime) values('%s',%s,'%s','%s','%s','%s','%s','%s',%s,%s,%s,%s,'%s')" % (
                serviceOrderId, wid, channel, mobile, servicecode, orderdest, starttime, endtime, ivrtotal, totalincome,
                feeincome, feeFlag, serviceSubTime)

            db.execute(sql)

        if pid == 11:
            totalincome = servicefee
            feeincome = ownerfee

        # check the msg_count == today_count

        webownerMsgCount = webownerMsgCountDic[wid]
        if webownerMsgCount != 0:
            log.info(
                "msg_count=%s.do check. wid=%s, servicecode=%s" % (webownerMsgCount, wid, servicecode))
            sql = "select today_count from lem_webowner where wid='%s'" % (wid,);
            today_count = db.getint(sql);
            if today_count >= webownerMsgCount:
                log.info("%s 's msg_count=%s, today_count=%s" % (wid, webownerMsgCount, today_count))
                feeFlag = 0
            else:
                sql = "update lem_webowner set today_count=today_count+1 where wid='%s'" % (wid,)
                db.execute(sql)
        else:
            log.info("msg_count=0. jump. wid=%s servicecode=%s" % (wid, servicecode))

        sql = "insert into lez_service_log(id,wid,channel,servicecode,pid,mobile,adid,totalincome,feeincome,status,statusstring,feeflag,gateway,subtime,ordercode,orderdest) values('%s',%s,'%s','%s',%s,'%s','%s',%s,%s,'%s','%s',%s,%s,'%s','%s','%s')" % (
            serviceOrderId, wid, channel, servicecode, pid, mobile, adid, totalincome, feeincome, msg.get('status'),
            msg.get('statusstring'), feeFlag, gateway, serviceSubTime, ordercode, orderdest)
        db.execute(sql)

        if feeFlag == 1:
            forwardToWebowner(wid, lang.num(channel), serviceOrderId, mobile, orderdest, ordercode, feeincome)

    except:
        log.error("serviceprocess error:%s" % lang.trace_back())


def isWhiteMobile(mobile):
    return True if whitelist.find(mobile) > -1 else False


statMap = dict()


def isWebNeedDeduct(pid, wid):
    wid = int(wid)
    if wid == 1000 or wid == 1001:
        return True
    global statMap
    flag = False
    key = '%s-%s' % (pid, wid)
    try:
        offBase = 5
        offNo = 2
        webownerScale = getWebownerScale(pid, wid)
        if webownerScale is None:
            webownerScale = getWebownerScale(pid, 1000)
        if webownerScale:
            offBase = webownerScale.get("offbase")
            offNo = webownerScale.get("offno")

        total = statMap.get(key)
        total = total + 1 if total else 1
        statMap[key] = total

        if (total % offBase + offNo) >= offBase:
            flag = True
    except:
        log.error("deduct error:%s" % lang.trace_back())
    return flag


def forwardToWebowner(wid, channel, serviceOrderId, mobile, orderdest, ordercode, fee):
    try:
        serviceurl = getWebownerServiceUrl(wid, channel)

        if serviceurl:
            serviceurl = '%s?linkid=%s&mobile=%s&orderdest=%s&cmdid=%s&fee=%s' % (
                serviceurl, serviceOrderId, mobile, orderdest, ordercode, fee)
            webRequestQueue.put(serviceurl)
            log.info('forwardToWebowner:[%s]' % (serviceurl))
    except:
        log.error("forwardTo1036 request error:%s" % lang.trace_back())
