#coding=gbk
from datetime import timedelta

HEADERS = {"Content-type":"application/x-www-form-urlencoded; charset=UTF-8","token":": FB7JTSSTWB06095250","Host":"seat.lib.whu.edu.cn:80","Connection":"Keep-Alive"}
BOOKHEADERS = {"Content-type":"application/x-www-form-urlencoded; charset=UTF-8",'Content-Length':0,"token":": FB7JTSSTWB06095250","Host":"seat.lib.whu.edu.cn:80","Connection":"Keep-Alive","Expect": "100-continue"}
LOGINURLH = '/rest/auth?username='
LOGINURLM = '&password='
CHKURL = '/rest/v2/user/reservations'
BOOKURL = '/rest/v2/freeBook'
CANCELURL = '/rest/v2/cancel/'
CHECKINURL = '/rest/v2/checkIn'
HOST = 'seat.lib.whu.edu.cn'

#设置危险时间默认为10min
defaultTD = timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=10, hours=0, weeks=0)	#
halfHourTD = timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=30, hours=0, weeks=0)
oneHourTD = timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=1, weeks=0)
oneDayTD = timedelta(days=1, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0)

seatDict_MainZone = {95:14408,96:14449,61:13406,62:13440,30:4188,29:4189}
