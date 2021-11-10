# %%
import pandas as pd
import subprocess

# %%
# to get the current day of the week
def getDayOfTheWeek():
	return int(str(subprocess.check_output(['date','+%u']))[2])
# %%
# to get the current hour
def getHour():
	hour=int(str(subprocess.check_output(['date','+%H']))[2:4])
	minute=int(str(subprocess.check_output(['date','+%M']))[2:4])
	return hour,minute


# %%
# to get an hour from a string that is in the csv
def getStringHour(strin):
	return strin.split(':')[1],strin.split(':')[2]

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
	dayOfTheWeek = getDayOfTheWeek()
	print("====== today is: " + str(dayOfTheWeek))
	## drop the days in wich I am not in
	zoom_csv_dt = zoom_csv_dt[zoom_csv_dt.time.str[0] == str(dayOfTheWeek)]
	## creating the list
	times = zoom_csv_dt.time.tolist()
	info = zoom_csv_dt['info'].tolist()
	action = zoom_csv_dt.action.tolist()
	name = zoom_csv_dt.name.tolist()
	return times ,info,action,name

def getInfoActionName():
	timeCol,info,actions,names = getTimeLinkColumns()
	curHour, curMinute = getHour()
	for i in range(0, len(timeCol)):
		comHour,comMinute = getStringHour(timeCol[i])
		print("curHour: " + str(curHour) + "curMinute " + str(curMinute) + "|")
		print("comHour: " + str(comHour) + "comMinute: " + str(comMinute + "|"))
		if int(curHour) == int(comHour):
			print("equal")
			if abs(int(curMinute) - int(comMinute)) < 40:
				print("equal again: " + str(abs(int(curMinute) - int(comMinute))))
				return info[i],actions[i],names[i]
		if int(curHour) == int(comHour) - 1:
				return info[i],actions[i],names[i]
	return "false"

#def closeWindow():
	# missing to finish

