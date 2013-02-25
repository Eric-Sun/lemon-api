import StringIO,hashlib
from xml.dom import minidom
from datetime import datetime
import requests

def test():
    content = '<Message version="1.0">\
              <callNum>15875500061</callNum>\
              <calledNum>1259078864</calledNum>\
              <serviceId>YW2012000177</serviceId>\
              <startTime>20120703154924</startTime>\
              <endTime>20120703154949</endTime>\
              <tradeId>1001:20120726213127123</tradeId>\
              <fee>1</fee>\
              <siteType>0</siteType>\
              <md5>86968e966f7e947240d496178b126b3d</md5>\
            </Message>'

    ssock = StringIO.StringIO(content)
    xmldoc = minidom.parse(ssock)
    ssock.close()
    callNum = xmldoc.getElementsByTagName('callNum')[0].firstChild.data
    calledNum = xmldoc.getElementsByTagName('calledNum')[0].firstChild.data
    serviceId = xmldoc.getElementsByTagName('serviceId')[0].firstChild.data
    fee = xmldoc.getElementsByTagName('fee')[0].firstChild.data
    tradeId = xmldoc.getElementsByTagName('tradeId')[0].firstChild.data
    startTime = xmldoc.getElementsByTagName('startTime')[0].firstChild.data
    endTime = xmldoc.getElementsByTagName('endTime')[0].firstChild.data
    md5str = xmldoc.getElementsByTagName('md5')[0].firstChild.data
    siteType = xmldoc.getElementsByTagName('siteType')[0].firstChild.data
    serviceKey = 'b35052b8-1911-4fa5-b146-fcfd8f22a8cc'
    verify = hashlib.md5('%s%s%s' % (callNum, endTime, serviceKey)).hexdigest()

    print callNum, calledNum, serviceId, fee, tradeId, startTime, endTime, md5str, siteType, verify

def uuid():
    return datetime.now().strftime('%y%m%d%H%M%S%f')

def postorder(mobile):
    partnerId = 'HZS201200066'
    serviceId = 'YW2012000254'
    mobile = '13552797751'
    tradeId = uuid()
    j_captcha_response = '1'
    url = 'http://ivr.95112.cn/ivr/orderFactoryForClient.do?partnerId=%s&serviceId=%s&mobile=%s&tradeId=%s&j_captcha_response=%s' % (partnerId, serviceId, mobile, tradeId, j_captcha_response)
    r = requests.get(url)
    result = r.text
    status, ivrnum = result.split(',')
    print status, ivrnum, mobile, tradeId

if __name__ == '__main__':
    postorder('123')
