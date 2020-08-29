
#coding=gbk
#success in log in and book and checkReservation

from datetime import datetime
from datetime import timedelta
import time
import http.client
import urllib
import os
import json
import dataContent
'''
函数名：initConnection
参数：urlAdd 要访问的目标地址
			userid 登陆用户名(str)
			userpassword 登陆密码(str)
返回值： http.client http链接实例

'''
def initConnection(urlAdd,userid,userpassword):
	loginUrl = dataContent.LOGINURLH + userid + dataContent.LOGINURLM + userpassword		#生成完整url请求
	
	httpcon = http.client.HTTPConnection(urlAdd)
	httpcon.request('GET',loginUrl,'',dataContent.HEADERS)
	httpres = httpcon.getresponse()
	resp_dat = httpres.read()
	print (httpres.status)
	print (httpres.reason)
	print (resp_dat)
	resp_dict = json.loads(str(resp_dat, encoding = 'utf-8'))
	print (resp_dict)
	if(resp_dict['status'] != 'success'):
		with open('/usr/local/reserveSeats/Errors.log','a+') as e:
			e.write('in testHttp4.initConnection, Request to Server failed:\n\r')
			e.write(str(resp_dict))
			e.write('\n\r\n\r')
		return None
	dataContent.HEADERS['token'] = dataContent.BOOKHEADERS['token'] = resp_dict['data']['token']
	print ('newToken:'+dataContent.HEADERS['token'])
	
	return httpcon;


'''
函数名：reserveSeat
参数：link-http.client 	请求实例，已经登陆的
			date	datetime实例，要预约的日期
'''


def reserveSeat(link, date, startTime, endTime, seat):
	a = date.strftime('%Y-%m-%d')
	databuf = '\"t=1&startTime=' + str(startTime) + '&endTime=' + str(endTime) + '&seat=' + str(seat) + '&date=' + a + '&t2=2\"'
	print ('dataToSend:' + databuf)
	dataContent.BOOKHEADERS['Content-Length'] = len(databuf)
	link.request('POST',dataContent.BOOKURL,'',dataContent.BOOKHEADERS)
	'''
	linkres = link.getresponse()
	if(linkres.status != 100):
		print ('postFailed!\n\r')
		print (linkres.status)
		print (linkres.reason)
		return False;
	'''
	link.send( databuf.encode(encoding='utf-8'))
	linkres = link.getresponse()
	respon = linkres.read()
	if(linkres.status != 200):
		with open('Errors.log','a+') as e:
			e.write('in testHttp4.reserveSeat, Http request failed:\n\r')
			e.write(linkres.status + ' ' + linkres.reason)
			e.write('\n\r\n\r')
		return False;
	
	print (str(respon, encoding = 'utf-8'))
	print ('success!')
	return True



'''
函数名：checkReservation(link)
参数:link-http.client实例，已经连接服务器并且注册
返回值：-1 HTTP请求错误
				-2 JSON内容错误
				0  无预约
				1  状态正常（预约无超时危险或正常履约）
				2  即将违约
				3  暂离
'''
def checkReservation(link):
	responseData_dict = getReserveData(link)
	if(responseData_dict == None):
		return -1
	
	if(responseData_dict['status'] != 'success'):
		return -2
	if(responseData_dict['data'] == None):
		return 0
	
	reserveMsg = responseData_dict['data'][0]
	
	if(reserveMsg['status'] == 'CHECK_IN'):###############如果正常使用则返回1
		return 1
	
	beginTime = datetime.strptime(reserveMsg['onDate'] + ' ' + reserveMsg['begin'],'%Y-%m-%d %H:%M')
	delta = abs(beginTime + dataContent.halfHourTD - datetime.now())
	
	if(reserveMsg['status'] == 'AWAY'):##################如果离开则返回3
		return 3
		
	elif(reserveMsg['status'] == 'RESERVE' and delta < dataContent.defaultTD):
		return 2
	else:
		return 1



'''
函数名:getReserveData
参数： l-http.client http链接实例
返回值： Data_dict 字典，为json解码（或者None如果出错)

'''
def getReserveData(l):
	l.request('GET',dataContent.CHKURL,'',dataContent.HEADERS)
	linkres = l.getresponse()
	responseData = linkres.read()
	if(linkres.status != 200):
		with open('Errors.log','a+') as e:
			e.write('in testHttp4.getReserveData, Http request failed:\n\r')
			e.write(linkres.status + ' ' + linkres.reason + ' ' + responseData)
			e.write('\n\r\n\r')
		print (linkres.status)
		print (linkres.reason)
		print (str(responseData, encoding = 'utf-8'))
		return None
	
	Data_dict = json.loads(str(responseData, encoding = 'utf-8'))
	print (Data_dict)
	return Data_dict

'''
函数名:cancelReservation
参数：link-http.client http实例，已经登陆
返回值：1成功
				0请求失败
				-1json请求失败

'''
def cancelReservation(link, resid):
	link.request('GET',dataContent.CANCELURL + str(resid),'',dataContent.HEADERS)
	linkres = link.getresponse()
	if(linkres.status != 200):
		print ('取消预约座位失败\n\r错误信息：')
		print (linkres.status)
		print (linkres.reason)
		print (linkres.read())
		return 0
	resDat_json = json.loads(str(linkres.read(), encoding = 'utf-8'))
	if(resDat_json['status'] == 'success'):
		return 1
	else:
		print ('取消预约座位失败\n\rJson信息错误\n\r错误信息：')
		print (resDat_json)
		return -1

'''
函数名:checkInReservation
参数：link-http.client http实例，已经登陆
返回值：1成功
				0请求失败
				-1json请求失败

'''
def checkInReservation(link):
	link.request('GET',dataContent.CHECKINURL,'',dataContent.HEADERS)
	linkres = link.getresponse()
	if(linkres.status != 200):
		print ('返回座位失败\n\r错误信息：')
		print (linkres.status)
		print (linkres.reason)
		print (str(linkres.read(), encoding = 'utf-8'))
		return 0
	resDat_json = json.loads(str(linkres.read(), encoding = 'utf-8'))
	if(resDat_json['status'] == 'success'):
		print ('message:')
		print (resDat_json['message'])
		return 1
	else:
		print ('返回座位失败\n\rJson信息错误\n\r错误信息：')
		print (resDat_json)
		return -1
	


if __name__ == '__main__':
	conn = initConnection('seat.lib.whu.edu.cn','2016301470030','164016')
	a = checkReservation(conn)
	if(a==0):
		print('无预约')
	elif(a==1):
		print('状态正常(有预约无超时危险或正常自习)')
	elif(a==2):
		print('预约即将过期')
	elif(a==3):
		print('暂时离开')
	elif(a==-1):
		print('HTTP连接错误')
	elif(a==-2):
		print('请求错误')
	
	a = cancelReservation(conn)
	if(a==0):
		print('http请求失败')
	elif(a==1):
		print('成功')
	elif(a==-1):
		print('JSON请求失败')
	
	
	conn.close()
	os._exit(0)
