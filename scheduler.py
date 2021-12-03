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
	circadianRithmAlarmTime = presets_dt["circadianRithmAlarmTime"]
	# get current month and day
	# this circadian ritm alarm is adjusted for mexicos change of time
	month = utilities.getMonth()
	day = utilities.getDayOfTheMonth()
	# don't edit this is you don't know what you are doing
	circadianRitmHour = int(circadianRithmAlarmTime.split(":")[0])
	circadianRitmMinute = int(circadianRithmAlarmTime.split(":")[1])
	
	# action to do if we are in winter
	if ( month == 4 and day <=4 or month < 4) or ( month == 10 and day >=30 or month > 10):
		ratio = 60/156
		days = getDistanceInCalendar(day,month,30,10)
		addedMinutes = days*ratio - 30
	# action to do if we are in summer
	else:
		print("summer")
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


def getMissingMinutes(toCompareHour,toCompareMinute,currentHour,currentMinite):
	if currentHour==toCompareHour :
		if toCompareMinute - currentMinite >= 0:
			return toCompareMinute - currentMinite
		else:
			return 0
	elif currentHour == toCompareHour - 1 :
		missingMinutes = (currentMinite+(60-toCompareMinute))
		if missingMinutes >ac :
			return 30
		else:
			return 0
	return 30

def getInfoActionName():
	# acceptance of the algoritm
	ac = presets.acceptance
	# current hour and minute
	hr, mi = utilities.getHour()

	updateCircadianWakeUp()

	#time and hour the circadian ritm alarm is set to
	ch = int(presets.circadianRitmHour)
	cm = int(presets.circadianRitmMinute)

	# debug the comparisons
	os.system("echo \"
			\n\n#======= month: "+str(utilities.getMonth())+
			"\nday: "+str(utilities.getDayOfTheMonth())+
			"\ncurrent hour: "+str(hr)+ ":" +str(mi)+" |circadianHour: " +str(ch) + ":" +str(cm) +
			"\" >> alarmLog/comparison_log")

	# circadian rithm alarm presets
	cInfo = presets.circadianRithmAlarminfo
	cAction = presets.circadianRithmAlarmAction
	cName = "circadian ritm alarm"
	cTime = presets.circadianRitmActionTime
	cActive = utilities.checkIfActive()[3]

	missingMinutes=getMissingMinutes(ch,cm,hr,mi)
	# check the circadian alarm
	if (cActive and   ( ( hr==ch ) and ( missingMinutes <=ac ))) or (( hr == ch - 1 )  and ( missingMinutes ) < ac ) :
	# append information for the log file and for debugging later
		os.system("echo \"
				\n#=====Month: "+str(utilities.getMonth())+" |day"+str(utilities.getDayOfTheMonth())+
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
			missingMin = getMissingMinutes(comH,comM,hr,mi)
			# sleep the necessary time
			t.sleep(missingMin*60)
			# return statement
			return info[i],actions[i],names[i],actionTimeCol[i]
	# return false so that when this happens we can get info output
	return "false", "false" , "false","false" # info,action,name,actionTime

