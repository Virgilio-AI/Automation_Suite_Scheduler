# %%
import pandas as pd
import subprocess
import presets
import utilities
import os
import json
import time as t
# %%
# to get the current day of the week

# %%
# this returns the time,links columns of the day
def getTimeLinkColumns():
	zoom_csv = "ClasesLinks.csv"
	zoom_csv_dt = pd.read_csv(zoom_csv)
	# drop the commented rows
	zoom_csv_dt = zoom_csv_dt.drop(zoom_csv_dt[zoom_csv_dt.time == 'LUNES'].index)
	zoom_csv_dt = zoom_csv_dt.drop(zoom_csv_dt[zoom_csv_dt.time == 'MARTES'].index)
	zoom_csv_dt = zoom_csv_dt.drop(zoom_csv_dt[zoom_csv_dt.time == 'MIERCOLES'].index)
	zoom_csv_dt = zoom_csv_dt.drop(zoom_csv_dt[zoom_csv_dt.time == 'JUEVES'].index)
	zoom_csv_dt = zoom_csv_dt.drop(zoom_csv_dt[zoom_csv_dt.time == 'VIERNES'].index)
	zoom_csv_dt = zoom_csv_dt.drop(zoom_csv_dt[zoom_csv_dt.time == 'SABADO'].index)
	zoom_csv_dt = zoom_csv_dt.drop(zoom_csv_dt[zoom_csv_dt.time == 'DOMINGO'].index)
	# get the day of the week
	dayOfTheWeek = utilities.getDayOfTheWeek()
	print("====== today is: " + str(dayOfTheWeek))
	## drop the days in wich I am not in
	zoom_csv_dt = zoom_csv_dt[zoom_csv_dt.time.str[0] == str(dayOfTheWeek)]
	## creating the list
	times = zoom_csv_dt.time.tolist()
	info = zoom_csv_dt['info'].tolist()
	action = zoom_csv_dt.action.tolist()
	name = zoom_csv_dt.name.tolist()
	actionTime = zoom_csv_dt['time-length'].tolist()
	# return 5 lists of the values of the current day
	return times ,info,action,name,actionTime

def getDistanceInCalendar(curDay,curMonth,dayChange,monthChange):
	if ( monthChange < curMonth or ( monthChange == curMonth and dayChange < monthChange )):
		return ( curDay - dayChange + (curMonth - monthChange)*30)
	else:
		return ( (12 - monthChange + curMonth)*30 - dayChange + curDay)

# the minutes are descending each day, starts half hour more

def updateCircadianWakeUp():
	# open the presets.json file
	with open('presets.json', 'r') as handle:
		fixed_json = ''.join(line for line in handle if not line.startswith('//'))
		# to ignore the comments that are inside the file
		presets_dt = json.loads(fixed_json)
	# get the circadian rithm alarm preset
	circadianRitmAlarmTime = presets_dt["circadianRitmAlarmTime"]
	# get current month and day
	# this circadian ritm alarm is adjusted for mexicos change of time
	month = utilities.getMonth()
	day = utilities.getDayOfTheMonth()
	# don't edit this is you don't know what you are doing
	circadianRitmHour = int(circadianRitmAlarmTime.split(":")[0])
	circadianRitmMinute = int(circadianRitmAlarmTime.split(":")[1])
	
	# action to do if we are in winter
	if ( month == 4 and day <=4 or month < 4) or ( month == 10 and day >=30 or month > 10):
		ratio = 60/156
		days = getDistanceInCalendar(day,month,30,10)
		addedMinutes = days*ratio - 30
	# action to do if we are in summer
	else:
		ratio = 60/209
		days = getDistanceInCalendar(day,month,4,4)
		addedMinutes = 30 - days*ratio
	tempH = circadianRitmHour
	tempM = circadianRitmMinute
	tempM = tempM + int(addedMinutes)
	if tempM < 0: # in case we need to delete minutes from the preset hour and minute
		tempH -=1
		tempM = 60 + tempM
	elif tempM > 60: # in case we need to add minutes to the preset hour and time
		tempH+=1
		tempM = tempM - 60
	# we update the values of the circadian alarm hour and minute
	presets.circadianRitmHour = tempH
	presets.circadianRitmMinute = tempM


def getMissingMinutes(toCompareHour,toCompareMinute,currentHour,currentMinite,acceptance):
	if currentHour==toCompareHour :
		if toCompareMinute - currentMinite >= 0:
			return toCompareMinute - currentMinite
		else:
			return 0
	elif currentHour == toCompareHour - 1 :
		missingMinutes = (currentMinite+(60-toCompareMinute))
		if missingMinutes >acceptance :
			return 30
		else:
			return 0
	return 30

def checkCsvUpdate():
	lastUpdate = ""
	with open('alarmLog/last_csv_update') as file_var:
		for line in file_var:
			lastUpdate = line.rstrip()
	lyear,lyearday = map(int,lastUpdate.split())
	cyear = utilities.getYear()
	cyearDay = utilities.getYearDay()
	difference = 0
	if cyear == lyear:
		difference = cyearDay - lyearday
	elif cyear - lyear >1:
		difference = 400
	else :
		if lyear%4 == 0:
			difference = (366 - lyearday) + cyearDay
		else :
			difference = (365 - lyearday) + cyearDay
	#print(difference)
	if difference > 6:
		updateCsv()


def createTempUniqueTable():
	command = ("""
select UniqueEvents.id as `UniqueEvents id`,Event.actionTime,EventType.name,EventType.actionDescription as `description`,UniqueEvents.year,UniqueEvents.month,UniqueEvents.day,Event.hour,Event.minute as `min`,Event.actionInformation
from EventType
inner join Event on EventType.id = Event.EventTypeId
inner join UniqueEvents on UniqueEvents.EventId = Event.id
""")
	command = utilities.mardbs(command)
	command +="> tempUniqueTable"
	os.system(command)
	tempTable = ""
	table = [[]]

	with open('tempUniqueTable') as tempUniqueTable:
		for line in tempUniqueTable:
			tempLine = line.strip()
			rline = ""
			for char in tempLine:
				if char == '\t':
					rline += ","
				else:
					rline += char
			lineWords = rline.split(',')
			table.append(lineWords)
			tempTable += rline + "\n"
	os.remove('tempUniqueTable')
	return table[1:]

def createTempWeeklyTable():
	command = ("""

select WeeklyEvents.id as `WeeklyEvent_id`,EventType.name,EventType.actionDescription,Event.actionTime,WeeklyEvents.yearStart,
WeeklyEvents.monthStart,WeeklyEvents.dayStart,WeeklyEvents.daysActive,group_concat(DayOfTheWeek.day) as `days`,Event.hour,Event.minute,Event.actionInformation
from DayOfTheWeek
inner join WeeklyEvents_DayOfTheWeek on WeeklyEvents_DayOfTheWeek.DayOfTheWeekId = DayOfTheWeek.id
inner join WeeklyEvents on WeeklyEvents.id = WeeklyEvents_DayOfTheWeek.WeeklyEventsId 
inner join Event on WeeklyEvents.EventId = Event.id
inner join EventType on EventType.id = Event.EventTypeId\n""")
	command+="group by WeeklyEvents.id;"

	command = utilities.mardbs(command)
	command +="> tempWeeklyTable"
	os.system(command)
	tempTable = ""
	table = [[]]

	with open('tempWeeklyTable') as tempUniqueTable:
		for line in tempUniqueTable:
			tempLine = line.strip()
			rline = ""
			for char in tempLine:
				if char == '\t':
					rline += ","
				elif char == ',':
					rline += "|"
				else:
					rline += char
			lineWords = rline.split(',')
			table.append(lineWords)
			tempTable += rline + "\n"

	os.remove('tempWeeklyTable')
	return table[1:]

def addDayOfTheWeek(day):
	stri = ""
	if day == 1:
		stri = "LUNES"
	elif day == 2:
		stri = "MARTES"
	elif day == 3:
		stri = "MIERCOLES"
	elif day == 4:
		stri = "JUEVES"
	elif day == 5:
		stri = "VIERNES"
	elif day == 6:
		stri = "SABADO"
	elif day == 7:
		stri = "DOMINGO"
	return stri


def calculateYearDay(day,month,months):
	ans = 0
	if month > 12 or day > 31:
		return 500

	for i in range(1,month):
		ans+=months[i]
	ans+=day
	return ans

def appendUniqueTasksToCsv(tableUnique,day,dayOfTheWeek,months):
	ans=""
	for row in range(1,len(tableUnique)):
		toCompare =calculateYearDay(int(tableUnique[row][6]),int(tableUnique[row][5]),months)
		if day == toCompare:
			ans+=""+str(dayOfTheWeek)+":"+str(tableUnique[row][7])+":"+str(tableUnique[row][8])+","+str(tableUnique[row][9])+","+str(tableUnique[row][2])+","+str(tableUnique[row][3])+","+str(tableUnique[row][1])+"\n"
	return ans
def checkDayOfTheWeek(daysInTable,dayOfTheWeek):
	if dayOfTheWeek == 1:
		for day in daysInTable:
			if day == 'monday':
				return True
	elif dayOfTheWeek==2:
		for day in daysInTable:
			if day == 'tuesday':
				return True
	elif dayOfTheWeek==3:
		for day in daysInTable:
			if day == 'wednesday':
				return True
	elif dayOfTheWeek==4:
		for day in daysInTable:
			if day == 'thursday':
				return True
	elif dayOfTheWeek==5:
		for day in daysInTable:
			if day == 'friday':
				return True
	elif dayOfTheWeek==6:
		for day in daysInTable:
			if day == 'saturday':
				return True
	elif dayOfTheWeek==7:
		for day in daysInTable:
			if day == 'sunday':
				return True
	return False

def appendWeeklyTasksToCsv(tableWeekly,day,dayOfTheWeek,months):
	ans=""
	for row in range(1,len(tableWeekly)):
		toCompare = calculateYearDay(int(tableWeekly[row][6]),int(tableWeekly[row][5]),months)
		daysInTable = tableWeekly[row][8].split('|')
		dayOfTheWeekb = checkDayOfTheWeek(daysInTable,dayOfTheWeek)
		if day >= toCompare and day < toCompare + int(tableWeekly[row][7]) and dayOfTheWeekb :
#			ans+=""+str(dayOfTheWeek) + ":"+str(tableWeekly[row][9])+":"+str(tableWeekly[row][10])+","+str(tableWeekly[row])+"\n"
#			print(ans)
			ans+=""+str(dayOfTheWeek)+":"+str(tableWeekly[row][9])+":"+str(tableWeekly[row][10])+","+str(tableWeekly[row][11])+","+str(tableWeekly[row][1])+","+str(tableWeekly[row][2])+","+str(tableWeekly[row][3])+"\n"
	return ans



def updateCsv():
	#	fopen("TasksOfTheWeek.csv","w")
	cyear = utilities.getYear()
	cmonth = utilities.getMonth()
	cday = utilities.getDayOfTheMonth()
	WeekDay = utilities.getDayOfTheWeek()
	cyearDay = utilities.getYearDay()

	february = 28
	if cyear%4 == 0: february = 29
	months = {1:31,2:february,3:31,4:30,5:31,6:30,7:31,8:31,9:30,10:31,11:30,12:31}
	UniqueTable = createTempUniqueTable()
	WeeklyTable = createTempWeeklyTable()
	# unique
	# 0 ,1         ,2   ,3          ,4   ,5    ,6  ,7   ,8
	# id,actionTime,name,description,year,month,day,hour,minute

	#Weekly
	# 0 ,1   ,2                ,3         ,4        ,5         ,6       ,7         ,8                ,9   ,10    ,11
	# id,name,actionDescription,actionTime,yearStart,monthStart,dayStart,daysActive,days(of the week),hour,minute,actionInformation

	print(UniqueTable[0])
	print()
	print(WeeklyTable[0])
	startDay = cyearDay - WeekDay
	print("week day: "+str(WeekDay)+"\ncurrent day of the year: "+str(cyearDay)+"")

	ans =""
	ans+="time,info,action,name,time-length\n"
	counter = 1
	for day in range(startDay+1,startDay+8):
		dayWeek = addDayOfTheWeek(day - startDay )
		ans+= ""+str(dayWeek)+","+str(dayWeek)+"\n"
		ans += appendUniqueTasksToCsv(UniqueTable,day,day-startDay,months)
		ans += appendWeeklyTasksToCsv(WeeklyTable,day,day-startDay,months)
		ans+="\n"

	csv_output = open("testCsvFile.csv","w")
	csv_output.write(ans)
	csv_output.close()

	tf = open("alarmLog/last_csv_update","w")
	tf.write(str(cyear) +" " + str(cyearDay))
	tf.close()







def getInfoActionName():
	checkCsvUpdate()
	# acceptance of the algoritm
	ac = presets.acceptance
	# current hour and minute
	hr, mi = utilities.getHour()

	updateCircadianWakeUp()

	#time and hour the circadian ritm alarm is set to
	ch = int(presets.circadianRitmHour)
	cm = int(presets.circadianRitmMinute)

	# debug the comparisons
	os.system("echo \"\n\n#======= month: "+str(utilities.getMonth())+
			"\nday: "+str(utilities.getDayOfTheMonth())+
			"\ncurrent hour: "+str(hr)+ ":" +str(mi)+" |circadianHour: " +str(ch) + ":" +str(cm) +
			"\" >> alarmLog/comparison_log")

	# circadian rithm alarm presets
	cInfo = presets.circadianRitmAlarminfo
	cAction = presets.circadianRitmAlarmAction
	cName = "circadian ritm alarm"
	cTime = presets.circadianRitmActionTime
	cActive = utilities.checkIfActive()[3]

	missingMinutes=getMissingMinutes(ch,cm,hr,mi,ac)
	# check the circadian alarm
	if (cActive and   ( ( hr==ch ) and ( missingMinutes <=ac ))) or (( hr == ch - 1 )  and ( missingMinutes ) < ac ) :
	# append information for the log file and for debugging later
		os.system("echo \"\n#=====Month: "+str(utilities.getMonth())+" |day"+str(utilities.getDayOfTheMonth())+
				"|MissingMinutes: "+str(missingMinutes)+" |action: "+str(cAction)+
				"\ncInfo: "+str(cInfo)+" |current hour: "+str(hr)+ ":" +str(mi)+" |circadianHour: " +str(ch) + ":" +str(cm) +
				"\" >> alarmLog/alarm_log")
		# to execute the action at the correct time
		t.sleep(missingMinutes*60)
		# return the action information for enmediate action
		return cInfo,cAction,cName,cTime
	# get the columns as lists
	timeCol,info,actions,names,actionTimeCol = getTimeLinkColumns()
	# for loop for checking the csv
	for i in range(0, len(timeCol)):
		# hour and minute of the currently analized appointment
		cmH,cmM = utilities.getStringHour(timeCol[i])
		comH = int(cmH)
		comM = int(cmM)


		if((hr==comH)and(abs(mi-comM)<=ac)) or ((hr == comH - 1) and ((mi + ( 60 - comM) ) < ac)):
			# get the minutes for the comparisson
			missingMin = getMissingMinutes(comH,comM,hr,mi,ac)
			# sleep the necessary time
			t.sleep(missingMin*60)
			# return statement
			return info[i],actions[i],names[i],actionTimeCol[i]
	# return false so that when this happens we can get info output
	return "false", "false" , "false","false" # info,action,name,actionTime



table = createTempWeeklyTable()
print(table)
