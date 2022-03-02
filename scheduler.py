# %%
import pandas as pd
import subprocess
import presets
import os
import json
import time as t
import re
import smtplib 
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders 

from datetime import datetime
from utilities import Utilities
# %%
# to get the current day of the week
# %%
# this returns the time,links columns of the day
class Scheduler():
	def getTimeLinkColumns(s):
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
		print("day")
		dayOfTheWeek = Utilities().getDayOfTheWeek()
		print("====== today is: " + str(dayOfTheWeek))
		## drop the days in wich I am not in
		zoom_csv_dt = zoom_csv_dt[zoom_csv_dt.time.str[0] == str(dayOfTheWeek)]
		## creating the list
		times = zoom_csv_dt.time.tolist()
		info = zoom_csv_dt['info'].tolist()
		action = zoom_csv_dt.action.tolist()
		name = zoom_csv_dt.name.tolist()
		actionTime = zoom_csv_dt['time-length'].tolist()
		Description = zoom_csv_dt['Description'].tolist()
		# return 5 lists of the values of the current day
		return times ,info,action,name,actionTime,Description
	def getDistanceInCalendar(s,curDay,curMonth,dayChange,monthChange):
		if ( monthChange < curMonth or ( monthChange == curMonth and dayChange < monthChange )):
			return ( curDay - dayChange + (curMonth - monthChange)*30)
		else:
			return ( (12 - monthChange + curMonth)*30 - dayChange + curDay)
	# the minutes are descending each day, starts half hour more
	def substractToCircadian(s,comH,comM):
		# get current month and day
		# this circadian ritm alarm is adjusted for mexicos change of time
		month = Utilities().getMonth()
		day = Utilities().getDayOfTheMonth()
		# don't edit this is you don't know what you are doing
		circadianRitmHour = comH
		circadianRitmMinute = comM
		
		# action to do if we are in winter
		if ( month == 4 and day <=4 or month < 4) or ( month == 10 and day >=30 or month > 10):
			ratio = 60/156
			days = s.getDistanceInCalendar(day,month,30,10)
			addedMinutes = days*ratio - 30
		# action to do if we are in summer
		else:
			ratio = 60/209
			days = s.getDistanceInCalendar(day,month,4,4)
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
		# we return the values updated
		return tempH,tempM
	def updateCircadianWakeUp(s):
		# open the presets.json file
		with open('presets.json', 'r') as handle:
			fixed_json = ''.join(line for line in handle if not line.startswith('//'))
			# to ignore the comments that are inside the file
			presets_dt = json.loads(fixed_json)
		# get the circadian rithm alarm preset
		circadianRitmAlarmTime = presets_dt["circadianRitmAlarmTime"]
		# get current month and day
		# this circadian ritm alarm is adjusted for mexicos change of time
		month = Utilities().getMonth()
		day = Utilities().getDayOfTheMonth()
		# don't edit this is you don't know what you are doing
		circadianRitmHour = int(circadianRitmAlarmTime.split(":")[0])
		circadianRitmMinute = int(circadianRitmAlarmTime.split(":")[1])
		
		# action to do if we are in winter
		if ( month == 4 and day <=4 or month < 4) or ( month == 10 and day >=30 or month > 10):
			ratio = 60/156
			days = s.getDistanceInCalendar(day,month,30,10)
			addedMinutes = days*ratio - 30
		# action to do if we are in summer
		else:
			ratio = 60/209
			days = s.getDistanceInCalendar(day,month,4,4)
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
	def getMissingMinutes(s,toCompareHour,toCompareMinute,currentHour,currentMinite,acceptance):
		if currentHour==toCompareHour :
			if toCompareMinute - currentMinite >= 0:
				print("first if")
				return toCompareMinute - currentMinite
			else:
				return 0
		elif currentHour == toCompareHour - 1 :
			missingMinutes = ((60 - currentMinite) +(60-toCompareMinute))
			if missingMinutes >acceptance :
				os.system("echo \"=============\n\ngetMissingMinutes returns a very long parameter\n\n==========\" >> Log/exceptionLog")
			else:
				return missingMinutes
		return 0
	def checkCsvUpdate(s):
		lastUpdate = ""
		with open('Log/last_csv_update') as file_var:
			for line in file_var:
				lastUpdate = line.rstrip()
		lyear,lyearday = map(int,lastUpdate.split())
		cyear = Utilities().getYear()
		cyearDay = Utilities().getYearDay()
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
			s.updateCsv()
	def createTempUniqueTable(s):
		command = ("""
		select UniqueEvents.id as `UniqueEvents id`,Event.actionTime,EventType.name,EventType.actionDescription as `Action description`,UniqueEvents.year,UniqueEvents.month,UniqueEvents.day,Event.hour,Event.minute as `min`,Event.actionInformation,Event.Description
		from EventType
		inner join Event on EventType.id = Event.EventTypeId
		inner join UniqueEvents on UniqueEvents.EventId = Event.id
		""")
		command = Utilities().mardbs(command)
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
	def createTempWeeklyTable(s):
		command = ("""
		
		select WeeklyEvents.id as `WeeklyEvent_id`,EventType.name,EventType.actionDescription,Event.actionTime,WeeklyEvents.yearStart,
		WeeklyEvents.monthStart,WeeklyEvents.dayStart,WeeklyEvents.daysActive,group_concat(DayOfTheWeek.day) as `days`,Event.hour,Event.minute,Event.actionInformation,Event.Description
		from DayOfTheWeek
		inner join WeeklyEvents_DayOfTheWeek on WeeklyEvents_DayOfTheWeek.DayOfTheWeekId = DayOfTheWeek.id
		inner join WeeklyEvents on WeeklyEvents.id = WeeklyEvents_DayOfTheWeek.WeeklyEventsId 
		inner join Event on WeeklyEvents.EventId = Event.id
		inner join EventType on EventType.id = Event.EventTypeId\n""")
		command+="group by WeeklyEvents.id;"
		command = Utilities().mardbs(command)
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
	def addDayOfTheWeek(s,day):
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
	def calculateYearDay(s,day,month,months):
		ans = 0
		if month > 12 or day > 31:
			return 500
		for i in range(1,month):
			ans+=months[i]
		ans+=day
		return ans
	def appendUniqueTasksToCsv(s,tableUnique,day,dayOfTheWeek,months):
		ans=""
		for row in range(1,len(tableUnique)):
			toCompare =s.calculateYearDay(int(tableUnique[row][6]),int(tableUnique[row][5]),months)
			if day == toCompare:
				ans+=""+str(dayOfTheWeek)+":"+str(tableUnique[row][7])+":"+str(tableUnique[row][8])+","+str(tableUnique[row][9])+","+str(tableUnique[row][2])+","+str(tableUnique[row][3])+","+str(tableUnique[row][1])+"," + str(tableUnique[row][10]) +"\n"
		return ans
	def checkDayOfTheWeek(s,daysInTable,dayOfTheWeek):
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
	def appendWeeklyTasksToCsv(s,tableWeekly,day,dayOfTheWeek,months):
		ans=""
		for row in range(1,len(tableWeekly)):
			toCompare = s.calculateYearDay(int(tableWeekly[row][6]),int(tableWeekly[row][5]),months)
			daysInTable = tableWeekly[row][8].split('|')
			dayOfTheWeekb = s.checkDayOfTheWeek(daysInTable,dayOfTheWeek)
			if day >= toCompare and day < toCompare + int(tableWeekly[row][7]) and dayOfTheWeekb :
	#			ans+=""+str(dayOfTheWeek) + ":"+str(tableWeekly[row][9])+":"+str(tableWeekly[row][10])+","+str(tableWeekly[row])+"\n"
	#			print(ans)
				ans+=""+str(dayOfTheWeek)+":"+str(tableWeekly[row][9])+":"+str(tableWeekly[row][10])+","+str(tableWeekly[row][11])+","+str(tableWeekly[row][1])+","+str(tableWeekly[row][2])+","+str(tableWeekly[row][3])+"," + str(tableWeekly[row][12]) + "\n"
		return ans
	def updateCsv(s):
		#	fopen("TasksOfTheWeek.csv","w")
		cyear = Utilities().getYear()
		cmonth = Utilities().getMonth()
		cday = Utilities().getDayOfTheMonth()
		WeekDay = Utilities().getDayOfTheWeek()
		cyearDay = Utilities().getYearDay()
		february = 28
		if cyear%4 == 0: february = 29
		months = {1:31,2:february,3:31,4:30,5:31,6:30,7:31,8:31,9:30,10:31,11:30,12:31}
		UniqueTable = s.createTempUniqueTable()
		WeeklyTable = s.createTempWeeklyTable()
		# unique
		# 0 ,1         ,2   ,3          ,4   ,5    ,6  ,7   ,8
		# id,actionTime,name,description,year,month,day,hour,minute
		#Weekly
		# 0 ,1   ,2                ,3         ,4        ,5         ,6       ,7         ,8                ,9   ,10    ,11
		# id,name,actionDescription,actionTime,yearStart,monthStart,dayStart,daysActive,days(of the week),hour,minute,actionInformation
		if len(UniqueTable) > 0:
			print(UniqueTable[0])
		print()
		if len(WeeklyTable) > 0:
			print(WeeklyTable[0])
		startDay = cyearDay - WeekDay
		print("week day: "+str(WeekDay)+"\ncurrent day of the year: "+str(cyearDay)+"")
		ans =""
		ans+="time,info,action,name,time-length,Description\n"
		counter = 1
		for day in range(startDay+1,startDay+8):
			dayWeek = s.addDayOfTheWeek(day - startDay )
			ans+= ""+str(dayWeek)+","+str(dayWeek)+"\n"
			ans += s.appendUniqueTasksToCsv(UniqueTable,day,day-startDay,months)
			ans += s.appendWeeklyTasksToCsv(WeeklyTable,day,day-startDay,months)
			ans+="\n"
		ans2 =""
		ans2+="time,info,action,name,time-length,Description\n"
		counter = 1
		startDay +=8
		for day in range(startDay+1,startDay+8):
			dayWeek = s.addDayOfTheWeek(day - startDay )
			ans2+= ""+str(dayWeek)+","+str(dayWeek)+"\n"
			ans2 += s.appendUniqueTasksToCsv(UniqueTable,day,day-startDay,months)
			ans2 += s.appendWeeklyTasksToCsv(WeeklyTable,day,day-startDay,months)
			ans2+="\n"
		csv_output = open("horariosSemanales/this.csv","w")
		csv_output.write(ans)
		csv_output.close()
		csv_output2 = open("horariosSemanales/next.csv","w")
		csv_output2.write(ans2)
		csv_output2.close()
		tf = open("Log/last_csv_update","w")
		tf.write(str(cyear) +" " + str(cyearDay))
		tf.close()
		ClasesLinks_file = open("ClasesLinks.csv","w")
		ClasesLinks_file.write(ans)
		ClasesLinks_file.close()
	def logTheAction(s,info,actions,names,actionTimeCol,timeCol):
		logVar = ("echo \"==== "+str(names)+" ====== \n" +
					"=== action: "+str(actions)+"\n"+
					"=== info:"+str(info)+"\n"+
					"=== action-time:"+str(actionTimeCol)+"\n"
					"=== time:"+str(timeCol)+"\n\n\" ")
		if actions == "alert":
			logVar+=">> Log/alert_log"
		elif actions == "alarm":
			logVar+=">> Log/alarm_log"
		else:
			logVar+=">> Log/zoom_log"
		os.system(logVar)
	def sorting(s,times):
		# times[idx][2:]
		hourMin = []
		for i in range(len(times)):
			hourMinute = times[i][2:].split(':')
			datetime_object = datetime.strptime(times[i][2:], '%H:%M')
			hourMin.append([datetime_object,i])
		hourMin.sort()

		return hourMin



	def createNewDaylyFile(s):
		print("missing create new file")
		tomorrowSchedule = open("horariosDiarios/tomorrow.txt","w")
		weekDay = Utilities().getDayOfTheWeek()
		temp = weekDay
		if weekDay == 7:
			weekDay = 1
		else:
			weekDay = weekDay + 1
		if temp == 7:
			zoom_csv = "horariosSemanales/next.csv"
		else:
			zoom_csv = "horariosSemanales/this.csv"
		#zoom_csv = "ClasesLinks.csv"
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
		dayOfTheWeek = weekDay
		## drop the days in wich I am not in
		zoom_csv_dt = zoom_csv_dt[zoom_csv_dt.time.str[0] == str(dayOfTheWeek)]
		## creating the list
		times = zoom_csv_dt.time.tolist()
		info = zoom_csv_dt['info'].tolist()
		action = zoom_csv_dt.action.tolist()
		name = zoom_csv_dt.name.tolist()
		actionTime = zoom_csv_dt['time-length'].tolist()
		description = zoom_csv_dt['Description'].tolist()

		# return 5 lists of the values of the current day
		ans=""
		date_idx = s.sorting(times)
		indices =  []
		for idx in date_idx:
			indices.append(idx[1])
		print(indices)
		print(times)
		for idx in indices:
			ans +=f"""====== {str(times[idx][2:])} | {str(action[idx])} ======
{str(name[idx])} | {str(description[idx])} | {str(actionTime[idx])} | {str(info[idx])}
"""
			# ans+=""+str(times[idx][2:])+" | "+str(action[idx])+" | "+str(name[idx])+" | "+str(actionTime[idx])+""+str(info[idx])+"|\n\n"

		tomorrowSchedule.write(ans)
		tomorrowSchedule.close()
	def updateTodaysSchedule(s):
		year = str(Utilities().getYear())
		month = str(Utilities().getMonth())
		day = str(Utilities().getDayOfTheMonth())
		newFile = "horariosDiarios/history/"+str(day)+"_"+str(month)+"_"+str(year)+".txt"
		oldFile = "horariosDiarios/today.txt"
		os.rename(oldFile,newFile)
		newf = "horariosDiarios/today.txt"
		oldf = "horariosDiarios/tomorrow.txt"
		os.rename(oldf,newf)
		s.createNewDaylyFile()
	def updateTheDaylySchedul(s,today):
		
		s.updateTodaysSchedule()
		updateDayly = open("Log/lastDayUpdateAction","w")
		updateDayly.write(today)
		updateDayly.close()
	def dayUpdate(s):
		lastUpdate=""
		with open('Log/lastDayUpdateAction') as file_var:
			for line in file_var:
				lastUpdate=line.strip()
		today = str(Utilities().getYearDay())
		if str(today) != str(lastUpdate):
			s.updateTheDaylySchedul(today)
			# s.sendTodaysSchedule() will improve with data bases
	def sendTodaysSchedule(s):
		try:
			fromaddr = "" # the adress that will be used to send the message atname@domain.com
			toaddr = "" # the addres that will recieve the messsage
			
			# instance of MIMEMultipart 
			msg = MIMEMultipart() 
			
			# storing the senders email address   
			msg['From'] = fromaddr
			
			# storing the receivers email address  
			msg['To'] = toaddr
			
			# storing the subject  
			msg['Subject'] = "first test"
			
			# string to store the body of the mail 
			body = "body test"
			
			# attach the body with the msg instance 
			msg.attach(MIMEText(body, 'plain')) 
			
			# open the file to be sent  
			filename = "today.txt"
			attachment = open("horariosDiarios/today.txt", "rb") 
			
			# instance of MIMEBase and named as p 
			p = MIMEBase('application', 'octet-stream') 
			
			# To change the payload into encoded form 
			p.set_payload((attachment).read()) 
			
			# encode into base64 
			encoders.encode_base64(p) 
			
			p.add_header('Content-Disposition', "attachment; filename= %s" % filename) 
			
			# attach the instance 'p' to instance 'msg' 
			msg.attach(p) 
			
			# creates SMTP session 
			s = smtplib.SMTP('smtp.gmail.com', 587) 
			  
			# start TLS for security 
			s.starttls() 
			  
			# Authentication 
			s.login(fromaddr, "password") # the password
			  
			# Converts the Multipart msg into a string 
			text = msg.as_string() 
			  
			# sending the mail 
			s.sendmail(fromaddr, toaddr, text) 
			  
			# terminating the session 
			s.quit()
		except:
			print("the email could not be sent")
	def checkDayUpdate(s):
		s.dayUpdate()
	
	def getInfoActionName(s):
		s.checkCsvUpdate()
		s.checkDayUpdate()
		# acceptance of the algoritm
		ac = presets.acceptance
		# current hour and minute
		hr, mi = Utilities().getHour()
		# debug the comparisons
		os.system("echo \"\n\n#======= month: "+str(Utilities().getMonth())+
				"\nday: "+str(Utilities().getDayOfTheMonth())+
				"\ncurrent hour: "+str(hr)+ ":" +str(mi)+
				"\" >> Log/comparison_log")
		# get the columns as lists
		timeCol,info,actions,names,actionTimeCol,DescriptionCol = s.getTimeLinkColumns()
		# for loop for checking the csv
		print(timeCol)
		for i in range(0, len(timeCol)):
			# hour and minute of the currently analized appointment
			cmH,cmM = Utilities().getStringHour(timeCol[i])
			comH = int(cmH)
			comM = int(cmM)
			print("name: " + names[i] + "time: "+str(timeCol) )

			# handle the circadian needs
			if re.match("circadian-.*",actions[i]):
				comH,comM = s.substractToCircadian(comH,comM)
				tempArr = actions[i].split('-')
				actions[i] = tempArr[1]
			if ((hr==comH)and(abs(mi-comM)<=ac)) or ((hr == comH - 1) and ((comM + ( 60 - mi) ) < ac)):
				# get the minutes for the comparisson
				missingMin = s.getMissingMinutes(comH,comM,hr,mi,ac)
				print("waiting " + str(missingMin) + " minutes" )
				# sleep the necessary time
				t.sleep(missingMin*60)
				# return statement
				s.logTheAction(str(info[i] + "|" + str(comH)+":" + str(comM) + "|" + "slept minutes:"+str(missingMin)+" | acceptance="+str(ac)+""),str(actions[i]),str(names[i]),str(actionTimeCol[i]),str(hr) +":" + str(mi))
				return info[i],actions[i],names[i],actionTimeCol[i],DescriptionCol[i]
		# return false so that when this happens we can get info output
		return "false", "false" , "false","false","false" # info,action,name,actionTime



dayOfTheWeek = Utilities().getDayOfTheWeek()
print(dayOfTheWeek)
