#coding=gbk
'''
testHttpMain.py
功能；1、查询状态是否正常
				（如果无res 是否需要预定下一个res）
				（如果有res 是否快违约）
				（如果快违约，取消，是否续订？）

'''

from datetime import datetime
import timeTable
import AutoBookSeats
import dataContent

def calcMinutes(dt):
	return ((dt.hour*60) + (dt.minute))


if __name__ == '__main__':
	with open('/usr/local/reserveSeats/Log.log','a+') as f:
		presentTime = datetime.now()
		f.write(str(presentTime) + '\n\r')				#
		for person in timeTable.timeTable:
			f.write('checking at:' + person['id'] + '\n\r')			#
			conn = AutoBookSeats.initConnection(dataContent.HOST, person['id'], person['password'])
			st = AutoBookSeats.checkReservation(conn)
			if (st == 3):
				f.write('state:Away......\t')
				result = AutoBookSeats.checkInReservation(conn)
				if (result == 1):
					f.write('successfully CheckIn!')
				elif(result == 0):
					f.write('failed to CheckIn, Http Connection problem.')
				elif(result == -1):
					f.write('failed to CheckIn, Server Refused problem.')
			
			elif ((st == 1) or (st == 0 and person['plan'] == None)):
				f.write('state:Normal......!')
			elif (st == 2):
				f.write('state:Dangerous......\n\rProcessing cancel procedure......\n\r')
				resData = AutoBookSeats.getReserveData(conn)
				result = AutoBookSeats.cancelReservation(conn, resData['data'][0]['id'])
				if (result == 1):
					f.write('successfully Cancel!')
				elif(result == 0):
					f.write('failed to Cancel, Http Connection problem.')
				elif(result == -1):
					f.write('failed to Cancel, Server Refused problem.')
				f.write('\n\rrebooking another reservation:')
				
				
				originBeginTime = datetime.strptime(resData['data'][0]['onDate'] + ' ' + resData['data'][0]['begin'],'%Y-%m-%d %H:%M')
				originEndTime = datetime.strptime(resData['data'][0]['onDate'] + ' ' + resData['data'][0]['end'],'%Y-%m-%d %H:%M')
				seatid = resData['data'][0]['seatId']
				
				result = AutoBookSeats.reserveSeat(conn, presentTime, str(calcMinutes(originBeginTime+dataContent.oneHourTD)), str(calcMinutes(originEndTime)), seatid)
				if (result == 1):
					f.write('successfully rebooked!')
				elif(result == 0):
					f.write('failed to rebook, Http Connection problem.')
				elif(result == -1):
					f.write('failed to rebook, Server Refused problem.')
			
			elif (st == 0 and person['plan'] != None):
				f.write('state:NoReservation......\n\rChecking plan......\n\r')
				presentMinute = calcMinutes(presentTime)
				for i in person['plan']:
					if(i['weekday'] == presentTime.weekday()):
						break
				
				for k in i['timetable']:
					if(k['start'] > presentMinute):
						f.write('booking next reservation......')
						seat = k['seat']
						result = AutoBookSeats.reserveSeat(conn, presentTime, k['start'], k['end'], dataContent.seatDict_MainZone[seat])
						if (result == 1):
							f.write('successfully booked!')
						elif(result == 0):
							f.write('failed to book, Http Connection problem.')
						elif(result == -1):
							f.write('failed to book, Server Refused problem.')
						break
				
			
			elif (st == -1):
				f.write('failed to Check the status, HTTP Connection problem.')
			else:			#回复 status 错误
				f.write('failed to Check the status, Server Refused problem.')
			
			f.write('\n\r')
			conn.close();
			
		f.write('\n\r')
		
	
