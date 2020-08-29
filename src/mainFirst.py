#coding=gbk

from datetime import datetime
import AutoBookSeats
import dataContent
import timeTable
import random
import time

if __name__ == '__main__':
#	ran = random.uniform(0,9)
#	time.sleep(ran)
	with open('/usr/local/reserveSeats/Log.log','a+') as f:
		presentTime = datetime.now()
		f.write(str(presentTime) + '\n\r')
		for person in timeTable.timeTable:
			if(person['plan'] == None):
				break
			for p in person['plan']:
				if(p['weekday'] == ((presentTime.weekday() + 1)%7)):
					break
			if (p['timetable'] == None):
				break
			
			f.write('booking for:' + person['id'] + '\n\r')
			conn = AutoBookSeats.initConnection(dataContent.HOST, person['id'], person['password'])
			if(conn == None):
				f.write('Failed to connect!\n\r')
				break
			pp = p['timetable'][0]
			st = AutoBookSeats.reserveSeat(conn, presentTime + dataContent.oneDayTD, pp['start'], pp['end'], dataContent.seatDict_MainZone[pp['seat']])
			if(st):
				f.write('Success!\n\r')
			else:
				f.write('Failed!\n\r')
			
			conn.close()
			f.write('\n\r')
			
		
		f.write('\n\r\n\r')
