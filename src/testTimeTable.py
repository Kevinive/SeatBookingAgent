import timeTable

for a in timeTable.timeTable:
	print ('id = ' + a['id'])
	print ('password = ' + a['password'])
	for i in a['plan']:
		print ('\tweekday = ' + str(i['weekday']))
		if (i['timetable'] == None):
			continue
		for k in i['timetable']:
			print ('\t\tmessage = ' + k['msg'])
			print ('\t\tstart = ' + str(k['start']))
			print ('\t\tend = ' + str(k['end']))
			print ('\t\tseat = ' + str(k['seat']))
			print ('\t\trebooknum = ' + str(k['rebooknum']) + '\n\r')
