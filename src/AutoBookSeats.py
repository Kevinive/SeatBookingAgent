
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
��������initConnection
������urlAdd Ҫ���ʵ�Ŀ���ַ
			userid ��½�û���(str)
			userpassword ��½����(str)
����ֵ�� http.client http����ʵ��

'''
def initConnection(urlAdd,userid,userpassword):
	loginUrl = dataContent.LOGINURLH + userid + dataContent.LOGINURLM + userpassword		#��������url����
	
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
��������reserveSeat
������link-http.client 	����ʵ�����Ѿ���½��
			date	datetimeʵ����ҪԤԼ������
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
��������checkReservation(link)
����:link-http.clientʵ�����Ѿ����ӷ���������ע��
����ֵ��-1 HTTP�������
				-2 JSON���ݴ���
				0  ��ԤԼ
				1  ״̬������ԤԼ�޳�ʱΣ�ջ�������Լ��
				2  ����ΥԼ
				3  ����
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
	
	if(reserveMsg['status'] == 'CHECK_IN'):###############�������ʹ���򷵻�1
		return 1
	
	beginTime = datetime.strptime(reserveMsg['onDate'] + ' ' + reserveMsg['begin'],'%Y-%m-%d %H:%M')
	delta = abs(beginTime + dataContent.halfHourTD - datetime.now())
	
	if(reserveMsg['status'] == 'AWAY'):##################����뿪�򷵻�3
		return 3
		
	elif(reserveMsg['status'] == 'RESERVE' and delta < dataContent.defaultTD):
		return 2
	else:
		return 1



'''
������:getReserveData
������ l-http.client http����ʵ��
����ֵ�� Data_dict �ֵ䣬Ϊjson���루����None�������)

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
������:cancelReservation
������link-http.client httpʵ�����Ѿ���½
����ֵ��1�ɹ�
				0����ʧ��
				-1json����ʧ��

'''
def cancelReservation(link, resid):
	link.request('GET',dataContent.CANCELURL + str(resid),'',dataContent.HEADERS)
	linkres = link.getresponse()
	if(linkres.status != 200):
		print ('ȡ��ԤԼ��λʧ��\n\r������Ϣ��')
		print (linkres.status)
		print (linkres.reason)
		print (linkres.read())
		return 0
	resDat_json = json.loads(str(linkres.read(), encoding = 'utf-8'))
	if(resDat_json['status'] == 'success'):
		return 1
	else:
		print ('ȡ��ԤԼ��λʧ��\n\rJson��Ϣ����\n\r������Ϣ��')
		print (resDat_json)
		return -1

'''
������:checkInReservation
������link-http.client httpʵ�����Ѿ���½
����ֵ��1�ɹ�
				0����ʧ��
				-1json����ʧ��

'''
def checkInReservation(link):
	link.request('GET',dataContent.CHECKINURL,'',dataContent.HEADERS)
	linkres = link.getresponse()
	if(linkres.status != 200):
		print ('������λʧ��\n\r������Ϣ��')
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
		print ('������λʧ��\n\rJson��Ϣ����\n\r������Ϣ��')
		print (resDat_json)
		return -1
	


if __name__ == '__main__':
	conn = initConnection('seat.lib.whu.edu.cn','2016301470030','164016')
	a = checkReservation(conn)
	if(a==0):
		print('��ԤԼ')
	elif(a==1):
		print('״̬����(��ԤԼ�޳�ʱΣ�ջ�������ϰ)')
	elif(a==2):
		print('ԤԼ��������')
	elif(a==3):
		print('��ʱ�뿪')
	elif(a==-1):
		print('HTTP���Ӵ���')
	elif(a==-2):
		print('�������')
	
	a = cancelReservation(conn)
	if(a==0):
		print('http����ʧ��')
	elif(a==1):
		print('�ɹ�')
	elif(a==-1):
		print('JSON����ʧ��')
	
	
	conn.close()
	os._exit(0)
