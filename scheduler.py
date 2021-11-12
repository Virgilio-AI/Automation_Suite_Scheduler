# %%
import pandas as pd
import subprocess
import presets
import utilities
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
	month = utilities.getMonth()
	day = utilities.getDayOfTheMonth()
	if ( month == 4 and day <=4 or month < 4) or ( month == 10 and day >=30 or month > 10):
		print("winter")
		ratio = 60/156
		days = getDistanceInCalendar(day,month,30,10)
		addedMinutes = days*ratio - 30
	else:
		ratio = 60/209
		days = getDistanceInCalendar(day,month,4,4)
		addedMinutes = 30 - days*ratio
	print("\nadded minutes: " +str(addedMinutes))
	print("\ndays: " + str(days))

	tempH = presets.circadianRitmHour
	tempM = presets.circadianRitmMinute
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
	# check if you need to updateCircadianRitm
	# return the alarm if the circadian ritm is on

	curHour, curMinute = utilities.getHour()
	if curHour == 5 and curMinute < presets.acceptance:
		updateCircadianWakeUp()
	if int(curHour) == int(presets.circadianRitmHour) and utilities.checkIfActive()[3]:
		print("equal")
		if abs(int(curMinute) - int(presets.circadianRitmMinute)) < presets.acceptance:
			print("equal again: " + str(abs(int(curMinute) - int(presets.circadianRitmMinute))))
			return presets.circadianRithmAlarminfo,presets.circadianRithmAlarmAction,"circadian rithm alarm",presets.circadianRitmActionTime

	timeCol,info,actions,names,actionTimeCol = getTimeLinkColumns()
	for i in range(0, len(timeCol)):
		comHour,comMinute = utilities.getStringHour(timeCol[i])
		print("curHour: " + str(curHour) + "curMinute " + str(curMinute) + "|")
		print("comHour: " + str(comHour) + "comMinute: " + str(comMinute + "|"))
		if curHour == comHour and abs(curMinute - comMinute) < presets.acceptance:
				print("equal " + str(abs(int(curMinute) - int(comMinute))))
				return info[i],actions[i],names[i],actionTimeCol[i]
		if int(curHour) == int(comHour) - 1 and (comMinute + ( 60 - curMinute) ) < presets.acceptance:
				return info[i],actions[i],names[i],actionTimeCol[i]
	return "false", "false" , "false","false" # info,action,name,actionTime


#updateCircadianWakeUp()
#print(str(presets.circadianRitmHour) + ":" + str(presets.circadianRitmMinute))
