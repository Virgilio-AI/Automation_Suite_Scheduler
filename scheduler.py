# %%
import pandas as pd
import subprocess
import presets
import utilities
import os
import json
# %%
# to get the current day of the week

# %%
# this returns the time,links columns of the day
def getTimeLinkColumns():
	zoom_csv = "ClasesLinks.csv"
	zoom_csv_dt = pd.read_csv(zoom_csv)
	## drop the columns of the days
#	zoom_csv_dt = zoom_csv_dt.drop(['meeting name'],axis=1)
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
	return times ,info,action,name,actionTime

def getDistanceInCalendar(curDay,curMonth,dayChange,monthChange):
	if ( monthChange < curMonth or ( monthChange == curMonth and dayChange < monthChange )):
		return ( curDay - dayChange + (curMonth - monthChange)*30)
	else:
		return ( (12 - monthChange + curMonth)*30 - dayChange + curDay)

# the minutes are descending each day, starts half hour more

def updateCircadianWakeUp():

	with open('presets.json', 'r') as handle:
		fixed_json = ''.join(line for line in handle if not line.startswith('//'))
		presets_dt = json.loads(fixed_json)
	circadianRithmAlarmTime = presets_dt["circadianRithmAlarmTime"]
	month = utilities.getMonth()
	day = utilities.getDayOfTheMonth()
	# don't edit this is you don't know what you are doing
	circadianRitmHour = int(circadianRithmAlarmTime.split(":")[0])
	circadianRitmMinute = int(circadianRithmAlarmTime.split(":")[1])

	if ( month == 4 and day <=4 or month < 4) or ( month == 10 and day >=30 or month > 10):
		print("winter")
		ratio = 60/156
		days = getDistanceInCalendar(day,month,30,10)
		addedMinutes = days*ratio - 30
	else:
		print("summer")
		ratio = 60/209
		days = getDistanceInCalendar(day,month,4,4)
		addedMinutes = 30 - days*ratio
	print("\nadded minutes: " +str(addedMinutes))
	print("\ndays: " + str(days))
	tempH = circadianRitmHour
	tempM = circadianRitmMinute
	tempM = tempM + int(addedMinutes)
	if tempM < 0:
		tempH -=1
		tempM = 60 + tempM
	elif tempM > 60:
		tempH+=1
		tempM = tempM - 60
	print("alarm time: " + str(tempH) + ":" + str(tempM))
	presets.circadianRitmHour = tempH
	presets.circadianRitmMinute = tempM




def getInfoActionName():
	# acceptance of the algoritm
	ac = presets.acceptance
	print("acceptance: " + str(ac))
	# current hour and minute
	hr, mi = utilities.getHour()

	updateCircadianWakeUp()

	#time and hour the circadian ritm alarm is set to
	ch = int(presets.circadianRitmHour)
	cm = int(presets.circadianRitmMinute)

	# debug the comparisons
	os.system("echo \"current hour: "+str(hr)+ ":" +str(mi)+" |circadianHour: " +str(ch) + ":" +str(cm) + "\" >> alarmLog/comparison_log")

	# circadian rim alarm presets
	cInfo = presets.circadianRithmAlarminfo
	cAction = presets.circadianRithmAlarmAction
	cName = "circadian ritm alarm"
	cTime = presets.circadianRitmActionTime
	cActive = utilities.checkIfActive()[3]

	print("hr: " + str(hr) + "mi " + str(mi) + "|")
	print("circadian alarm: " + str(ch) + ":" + str(cm) )
	# check the circadian alarm
	if cActive and (  ( ( hr==ch ) and ( abs( mi-cm ) <=ac )) or (( hr == ch - 1 )  and ( (mi + ( 60 - cm ) ) < ac ) )):
		print("circadian alarm equal")
		os.system("echo \"cInfo: "+str(cInfo)+" |current hour: "+str(hr)+ ":" +str(mi)+" |circadianHour: " +str(ch) + ":" +str(cm) + "\" >> alarmLog/alarm_log")
		return cInfo,cAction,cName,cTime
	# get the columns as lists
	timeCol,info,actions,names,actionTimeCol = getTimeLinkColumns()
	# for loop for checking the csv
	for i in range(0, len(timeCol)):
		# hour and minute of the currently analized appointment
		cmH,cmM = utilities.getStringHour(timeCol[i])
		comH = int(cmH)
		comM = int(cmM)

		print("hr: " + str(hr) + "mi " + str(mi) + "|")
		print("comH: " + str(comH) + "comM: " + str(comM) + "|")

		if((hr==comH)and(abs(mi-comM)<=ac)) or ((hr == comH - 1) and ((mi + ( 60 - comM) ) < ac)):
			print("equal " + str(abs(mi - comM)))
			return info[i],actions[i],names[i],actionTimeCol[i]
	return "false", "false" , "false","false" # info,action,name,actionTime

