# Fecha: 21/November/2021 - Sunday
# Autor: Virgilio Murillo Ochoa
# personal github: Virgilio-AI
# linkedin: https://www.linkedin.com/in/virgilio-murillo-ochoa-b29b59203
# contact: virgiliomurilloochoa1@gmail.com
from tkinter import *
import tkinter as tk
import sys
import os
import keyboard
import matplotlib.pyplot as plt
import subprocess
# =============
# ==== utilities for the gui =====
# =============

def center(tempWindow,window_width,window_height):
	tempWindow.attributes('-type','dialog')
	screen_width = tempWindow.winfo_screenwidth()
	screen_height = tempWindow.winfo_screenheight()
	x_pos = int((screen_width - window_width)/2)
	y_pos = int((screen_height - window_height)/2)
	geometry = str(window_width)+"x"+str(window_height)  + "+" + str(x_pos) + "+" + str(y_pos)
	tempWindow.geometry(geometry)
def errorMsg(LowLevel,message):
	errorWin = Toplevel(LowLevel)
	center(errorWin,300,300)
	# the error message
	messageLabel = Label(errorWin,text=message,bg="blue",fg="red",font=40)
	messageLabel.pack(side=TOP)
	errorWin.bind("<Return>",lambda event: deleteTopLevel(errorWin))
def testing(event):
	print("hello")
def exitProgram():
	sys.exit(0)
def deleteTopLevel(frame):
	frame.destroy()
def sur(stri):
	return '\\"' + stri + '\\"'

def exTerm(stri):
	return "st -g \"160x50+0+0\" -e sh -c \"" + str(stri) + " ; read -n1 \" & "

def mardb(stri):
	return "mariadb --execute=\" use automation_suite ; "+str(stri)+"\""
def mardbs(stri):
	return "mariadb --execute=' use automation_suite ; "+str(stri)+"'"


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

	command = mardbs(command)
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



# =============
# ==== buttons =====
# =============
def queryWeeklyTasks():
# setting labels and text boxes for the page
	level_add_task = Toplevel(frame)
	center(level_add_task,300,500)


	# the abel 
	title_of_window = Label(level_add_task,text="input all the information")
	title_of_window.pack(side=TOP)



	# test label 
	newLine = Label(level_add_task,text="")
	newLine.pack(side=TOP)

	EventTypeLabel = Label(level_add_task,text="EventType:")
	EventTypeLabel.pack(side=TOP)
	# start entering information
	EventType = tk.StringVar()
	EventTypeTextBox = tk.Entry(level_add_task, width = 50, textvariable = EventType)
	EventTypeTextBox.pack(side=TOP)

	actionTimeLabel = Label(level_add_task,text="actionTime:")
	actionTimeLabel.pack(side=TOP)
	# start entering information
	actionTime = tk.StringVar()
	actionTimeTextBox = tk.Entry(level_add_task, width = 50, textvariable = actionTime)
	actionTimeTextBox.pack(side=TOP)

	yearStartLabel = Label(level_add_task,text="yearStart:")
	yearStartLabel.pack(side=TOP)
	# start entering information
	yearStart = tk.StringVar()
	yearStartTextBox = tk.Entry(level_add_task, width = 50, textvariable = yearStart)
	yearStartTextBox.pack(side=TOP)

	monthStartLabel = Label(level_add_task,text="monthStart:")
	monthStartLabel.pack(side=TOP)
	# start entering information
	monthStart = tk.StringVar()
	monthStartTextBox = tk.Entry(level_add_task, width = 50, textvariable = monthStart)
	monthStartTextBox.pack(side=TOP)

	dayStartLabel = Label(level_add_task,text="dayStart:")
	dayStartLabel.pack(side=TOP)
	# start entering information
	dayStart = tk.StringVar()
	dayStartTextBox = tk.Entry(level_add_task, width = 50, textvariable = dayStart)
	dayStartTextBox.pack(side=TOP)


	WeeklyIdLabel = Label(level_add_task,text="id:")
	WeeklyIdLabel.pack(side=TOP)
	# start entering information
	WeeklyId = tk.StringVar()
	WeeklyIdTextBox = tk.Entry(level_add_task, width = 50, textvariable = WeeklyId)
	WeeklyIdTextBox.pack(side=TOP)

	# =============
	# ==== the frame for the buttoms =====
	# =============
	# the frame for the buttons
	buttonsFrame = Frame(level_add_task)
	buttonsFrame.pack()

	# back button
	# opt parameters = fg="color",bg="color",command=somFunction
	back_button = Button(buttonsFrame,text="back",command=lambda: deleteTopLevel(level_add_task))
	back_button.pack(side=BOTTOM)


	# add button, action to do when pressed
	# opt parameters = fg="color",bg="color",command=somFunction
	queryUniqueBut = Button(buttonsFrame,text="query with the given constrains",command=lambda: queryWeeklyButton(EventType.get(),actionTime.get(),yearStart.get(),monthStart.get(),dayStart.get(),WeeklyId.get()))
	queryUniqueBut.pack(side=TOP)

	# the button to delete with the given constrains
	# opt parameters = fg="color",bg="color",command=lambda: function(params)
	deleteWeeklyBut = Button(buttonsFrame,text="delete with the given constrains",command=lambda: deleteWeeklyButton(EventType.get(),actionTime.get(),yearStart.get(),monthStart.get(),dayStart.get(),WeeklyId.get())).pack(side=TOP)

def queryWeeklyButton(EventType,actionTime,yearStart,monthStart,dayStart,WeeklyId):
	command = ("""select WeeklyEvents.id as `WeeklyEvent_id`,EventType.name,EventType.id,Event.actionTime,WeeklyEvents.yearStart,
WeeklyEvents.monthStart,WeeklyEvents.dayStart,WeeklyEvents.daysActive,group_concat(substring(DayOfTheWeek.day,1,3)) as `days`,Event.Description,Event.hour as 'hr',Event.minute as 'mn'
from DayOfTheWeek
inner join WeeklyEvents_DayOfTheWeek on WeeklyEvents_DayOfTheWeek.DayOfTheWeekId = DayOfTheWeek.id
inner join WeeklyEvents on WeeklyEvents.id = WeeklyEvents_DayOfTheWeek.WeeklyEventsId 
inner join Event on WeeklyEvents.EventId = Event.id
inner join EventType on EventType.id = Event.EventTypeId\n""")
	first =False
	if (EventType != "" or actionTime != "" or yearStart != "" or monthStart != "" or dayStart != "" or WeeklyId != ""):
		command+="where "

	if EventType != "":
		command += "EventType.name = \""+str(EventType)+"\" "
		
		first = True

	if actionTime != "":
		if first:
			command+="and (Event.actionTime = '"+str(actionTime)+"') "
		else:
			command+="(Event.actionTime = '"+str(actionTime)+"') "
			first = True

	if yearStart != "":
		if first:
			command+="and (WeeklyEvents.yearStart = '"+str(yearStart)+"') "
		else:
			command+="(WeeklyEvents.yearStart = '"+str(yearStart)+"') "
			first = True

	if monthStart != "":
		if first:
			command+="and (WeeklyEvents.monthStart = '"+str(monthStart)+"') "
		else:
			command+="(WeeklyEvents.monthStart = '"+str(monthStart)+"') "
			first = True

	if dayStart != "":
		if first:
			command+="and (WeeklyEvents.dayStart = '"+str(dayStart)+"') "
		else:
			command+="(WeeklyEvents.dayStart = '"+str(dayStart)+"') "
			first = True

	if WeeklyId != "":
		if first:
			command+="and (WeeklyEvents.id = '"+str(WeeklyId)+"') "
		else:
			command+="(WeeklyEvents.id = '"+str(WeeklyId)+"') "
			first = True

	if first:
		command += "\n"

	command+="group by WeeklyEvents.id;"
	command = mardbs(command)
	print(command)
	os.system(command)
def queryUniqueButton(EventType,actionTime,year,month,day):
	command = ("""

select UniqueEvents.id as `UniqueEvents id`,Event.actionTime,EventType.name,EventType.actionDescription as `description`,UniqueEvents.year,UniqueEvents.month,UniqueEvents.day,Event.hour,Event.minute as `min`,Event.hour,Event.minute,Event.Description
from EventType
inner join Event on EventType.id = Event.EventTypeId
inner join UniqueEvents on UniqueEvents.EventId = Event.id\n""")
	first =False
	if (EventType != "" or actionTime != "" or year != "" or month != "" or day != ""):
		command+="where ("

	if EventType != "":
		command += "(EventType.name = '"+str(EventType)+"')"
		first = True

	if actionTime != "":
		if first:
			command+="and (Event.actionTime = '"+str(actionTime)+"') "
		else:
			command+="(Event.actionTime = '"+str(actionTime)+"') "
			first = True

	if year != "":
		if first:
			command+="and (UniqueEvents.year = '"+str(year)+"') "
		else:
			command+="(UniqueEvents.year = '"+str(year)+"') "
			first = True

	if month != "":
		if first:
			command+="and (UniqueEvents.month = '"+str(month)+"') "
		else:
			command+="(UniqueEvents.month = '"+str(month)+"') "
			first = True

	if day != "":
		if first:
			command+="and (UniqueEvents.day = '"+str(day)+"') "
		else:
			command+="(UniqueEvents.day = '"+str(day)+"') "
			first = True

	if first:
		command += ")\n"

	command += " ; \n"
	command = mardbs(command)
	print(command)
	os.system(command)

def queryUniqueTasks():
	level_add_task = Toplevel(frame)
	center(level_add_task,300,500)

	# the abel 
	title_of_window = Label(level_add_task,text="input all the information")
	title_of_window.pack(side=TOP)

	# test label 
	newLine = Label(level_add_task,text="")
	newLine.pack(side=TOP)

	EventTypeLabel = Label(level_add_task,text="EventType:")
	EventTypeLabel.pack(side=TOP)
	# start entering information
	EventType = tk.StringVar()
	EventTypeTextBox = tk.Entry(level_add_task, width = 50, textvariable = EventType)
	EventTypeTextBox.pack(side=TOP)

	actionTimeLabel = Label(level_add_task,text="actionTime:")
	actionTimeLabel.pack(side=TOP)
	# start entering information
	actionTime = tk.StringVar()
	actionTimeTextBox = tk.Entry(level_add_task, width = 50, textvariable = actionTime)
	actionTimeTextBox.pack(side=TOP)

	yearLabel = Label(level_add_task,text="year:")
	yearLabel.pack(side=TOP)
	# start entering information
	year = tk.StringVar()
	yearTextBox = tk.Entry(level_add_task, width = 50, textvariable = year)
	yearTextBox.pack(side=TOP)

	monthLabel = Label(level_add_task,text="month:")
	monthLabel.pack(side=TOP)
	# start entering information
	month = tk.StringVar()
	monthTextBox = tk.Entry(level_add_task, width = 50, textvariable = month)
	monthTextBox.pack(side=TOP)

	dayLabel = Label(level_add_task,text="day:")
	dayLabel.pack(side=TOP)
	# start entering information
	day = tk.StringVar()
	dayTextBox = tk.Entry(level_add_task, width = 50, textvariable = day)
	dayTextBox.pack(side=TOP)

	# =============
	# ==== the frame for the buttoms =====
	# =============
	# the frame for the buttons
	buttonsFrame = Frame(level_add_task)
	buttonsFrame.pack()

	# back button
	# opt parameters = fg="color",bg="color",command=somFunction
	back_button = Button(buttonsFrame,text="back",command=lambda: deleteTopLevel(level_add_task))
	back_button.pack(side=BOTTOM)


	# add button, action to do when pressed
	# opt parameters = fg="color",bg="color",command=somFunction
	queryUniqueBut = Button(buttonsFrame,text="query with the given constrains",command=lambda: queryUniqueButton(EventType.get(),actionTime.get(),year.get(),month.get(),day.get()))
	queryUniqueBut.pack(side=TOP)

	# opt parameters = fg="color",bg="color",command=lambda: function(params)
	deleteUniqueBut = Button(buttonsFrame,text="delete with given constrains",command=lambda: deleteUniqueButton(EventType.get(),actionTime.get(),year.get(),month.get(),day.get())).pack(side=TOP)

def deleteUniqueButton(EventType,actionTime,year,month,day):
	ans = input("are you sure you want to delete??(yes)")
	if ans != "yes":
		return
	command=("""
	delete from Event where id in (select EventId from UniqueEvents)
	\n""")
	first = False
	if EventType != "" or actionTime != "" or year != "" or month != "" or day != "":
		command = ("""
		delete from Event where  id in (select EventId from UniqueEvents where ( """)
	else:
		command = ("""
		delete from Event where  id in (select EventId from UniqueEvents) """)

	if EventType != "":
		command += "EventTypeId = (select id from EventType where name = \""+str(EventType)+"\" )"
		first = True

	if actionTime != "":
		if first:
			command+="and (actionTime = "+str(actionTime)+") "
		else:
			command+="(actionTime = "+str(actionTime)+") "
			first = True

	if year != "":
		if first:
			command+="and (year = "+str(year)+") "
		else:
			command+="(year = "+str(year)+" ) "
			first = True

	if month != "":
		if first:
			command+="and (month = "+str(month)+") "
		else:
			command+="(month = "+str(month)+") "
			first = True

	if day != "":
		if first:
			command+="and day = "+str(day)+") "
		else:
			command+="(day = "+str(day)+") "
			first = True

	if first:
		command += ")) ;\n"

	command = mardbs(command)
	print(command)
	os.system(command)

def deleteWeeklyButton(EventType,actionTime,yearStart,monthStart,dayStart,WeeklyId):

	ans = input("are you sure you want to delete??(yes)")
	if ans != "yes":
		return
	first =False
	if (EventType != "" or actionTime != "" or yearStart != "" or monthStart != "" or dayStart != "" or WeeklyId != ""):
		command = ("""
		delete from Event where  id in (select EventId from WeeklyEvents where ( """)
	else:
		command = ("""
		delete from Event where  id in (select EventId from WeeklyEvents) """)

	if EventType != "":
		command += "EventTypeId = (select id from EventType where name = \""+str(EventType)+"\" )"
		first = True

	if actionTime != "":
		if first:
			command+="and (actionTime = "+str(actionTime)+") "
		else:
			command+="(actionTime = "+str(actionTime)+") "
			first = True

	if yearStart != "":
		if first:
			command+="and (yearStart = "+str(yearStart)+") "
		else:
			command+="(yearStart = "+str(yearStart)+" ) "
			first = True

	if monthStart != "":
		if first:
			command+="and (monthStart = "+str(monthStart)+") "
		else:
			command+="(monthStart = "+str(monthStart)+") "
			first = True

	if dayStart != "":
		if first:
			command+="and (dayStart = "+str(dayStart)+") "
		else:
			command+="(dayStart = "+str(dayStart)+") "
			first = True

	if WeeklyId != "":
		if first:
			command+="and (id = "+str(WeeklyId)+") "
		else:
			command+="(id = "+str(WeeklyId)+") "
			first = True

	if first:
		command += ")) ;\n"

	command = mardbs(command)
	print(command)
	os.system(command)


	# print(command)

def addButton(layer,yearStart,monthStart,dayStart,daysActive,actionTime,EventType,daysOfTheWeek,hour,minute,actionInformation,Description):
	daysOfTheWeekdic = {1:"monday",2:"tuesday",3:"wednesday",4:"thursday",5:"friday",6:"saturday",7:"sunday"}
	daysOfTheWeekArr = daysOfTheWeek.split(',')
	for it in daysOfTheWeekArr:
		if not ( it in daysOfTheWeekdic.values()):
			errorMsg(layer,"error: "+str(it)+"not in dictionary")
			return

	if( yearStart.isnumeric() and monthStart.isnumeric() and dayStart.isnumeric() and daysActive.isnumeric() and actionTime.isnumeric() and hour.isnumeric() and minute.isnumeric() ):
		firstAction = mardb("insert into Event(actionTime,EventTypeId,hour,minute,actionInformation,Description) values("+str(actionTime)+",(select id from EventType where name = '"+str(EventType)+"' ),"+str(hour)+","+str(minute)+",'"+str(actionInformation)+"','"+str(Description)+"') ; ")
		os.system(firstAction)
		print(firstAction)
		secondAction = mardb("insert into WeeklyEvents(EventId,yearStart,monthStart,dayStart,daysActive) values((select max(id) from Event),"+str(yearStart)+","+str(monthStart)+","+str(dayStart)+","+str(daysActive)+") ;")
		os.system(secondAction)
		print(secondAction)



		for element in range(0, len(daysOfTheWeekArr)):
			tempAction = mardb("insert into WeeklyEvents_DayOfTheWeek(WeeklyEventsId,DayOfTheWeekId) values((select max(id) from WeeklyEvents),(select id from DayOfTheWeek where day = '"+str(daysOfTheWeekArr[element])+"'));")
			os.system(tempAction)
			print(tempAction)
		errorMsg(layer,"task added succesfully")

	else:
		errorMsg(layer,"a variable has been passed as int and it had to be str")
		return
def addWeeklyTask():
# setting labels and text boxes for the page
	level_add_task = Toplevel(frame)
	center(level_add_task,300,500)


	# the abel 
	title_of_window = Label(level_add_task,text="input all the required information")
	title_of_window.pack(side=TOP)



	# test label 
	newLine = Label(level_add_task,text="")
	newLine.pack(side=TOP)

	# yearStart label
	yearStartLabel = Label(level_add_task,text="yearStart:")
	yearStartLabel.pack(side=TOP)
	# start entering information
	yearStart = tk.StringVar()
	yearStartTextBox = tk.Entry(level_add_task, width = 50, textvariable = yearStart)
	yearStartTextBox.pack(side=TOP)

	# monthStart label
	monthStartLabel = Label(level_add_task,text="monthStart:")
	monthStartLabel.pack(side=TOP)
	# start entering monthStartrmation
	monthStart = tk.StringVar()
	monthStartTextBox = tk.Entry(level_add_task, width = 50, textvariable = monthStart)
	monthStartTextBox.pack(side=TOP)

	# dayStart label
	dayStartLabel = Label(level_add_task,text="dayStart:")
	dayStartLabel.pack(side=TOP)
	# start entering dayStartrmation
	dayStart = tk.StringVar()
	dayStartTextBox = tk.Entry(level_add_task, width = 50, textvariable = dayStart)
	dayStartTextBox.pack(side=TOP)

	# weeks label
	daysActiveLabel = Label(level_add_task,text="daysActive:")
	daysActiveLabel.pack(side=TOP)
	# start entering daysActivermation
	daysActive = tk.StringVar()
	daysActiveTextBox = tk.Entry(level_add_task, width = 50, textvariable = daysActive)
	daysActiveTextBox.pack(side=TOP)

	# EventType label
	EventTypeLabel = Label(level_add_task,text="EventType:")
	EventTypeLabel.pack(side=TOP)

	EventTypes = [
	"alarm",
	"alert",
	"zoom",
	"circadian-alert",
	"circadian-zoom",
	"circadian-alarm",
	"human-task"
	] #etc
	
	
	EventType = tk.StringVar()
	EventType.set(EventTypes[0]) # default value
	
	EventTypeDropMenu = OptionMenu(level_add_task, EventType, *EventTypes)
	EventTypeDropMenu.pack()

	# actionTime label
	actionTimeLabel = Label(level_add_task,text="actionTime:")
	actionTimeLabel.pack(side=TOP)
	# start entering actionTimermation
	actionTime = tk.StringVar()
	actionTimeTextBox = tk.Entry(level_add_task, width = 50, textvariable = actionTime)
	actionTimeTextBox.pack(side=TOP)

	# daysOfTheWeek label
	daysOfTheWeekLabel = Label(level_add_task,text="daysOfTheWeek:")
	daysOfTheWeekLabel.pack(side=TOP)
	# start entering daysOfTheWeekrmation
	daysOfTheWeek = tk.StringVar()
	daysOfTheWeekTextBox = tk.Entry(level_add_task, width = 50, textvariable = daysOfTheWeek)
	daysOfTheWeekTextBox.pack(side=TOP)


	# hour label
	hourLabel = Label(level_add_task,text="hour:")
	hourLabel.pack(side=TOP)
	# start entering hourrmation
	hour = tk.StringVar()
	hourTextBox = tk.Entry(level_add_task, width = 50, textvariable = hour)
	hourTextBox.pack(side=TOP)


	# minute label
	minuteLabel = Label(level_add_task,text="minute:")
	minuteLabel.pack(side=TOP)
	# start entering minutermation
	minute = tk.StringVar()
	minuteTextBox = tk.Entry(level_add_task, width = 50, textvariable = minute)
	minuteTextBox.pack(side=TOP)

	# actionInformation label
	actionInformationLabel = Label(level_add_task,text="actionInformation:")
	actionInformationLabel.pack(side=TOP)
	# start entering actionInformationrmation
	actionInformation = tk.StringVar()
	actionInformationTextBox = tk.Entry(level_add_task, width = 50, textvariable = actionInformation)
	actionInformationTextBox.pack(side=TOP)

	
	# Description label
	DescriptionLabel = Label(level_add_task,text="Description:")
	DescriptionLabel.pack(side=TOP)
	# start entering Descriptionrmation
	Description = tk.StringVar()
	DescriptionTextBox = tk.Entry(level_add_task, width = 50, textvariable = Description)
	DescriptionTextBox.pack(side=TOP)

	# =============
	# ==== the frame for the buttoms =====
	# =============
	# the frame for the buttons
	buttonsFrame = Frame(level_add_task)
	buttonsFrame.pack()

	# back button
	# opt parameters = fg="color",bg="color",command=somFunction
	back_button = Button(buttonsFrame,text="back",command=lambda: deleteTopLevel(level_add_task))
	back_button.pack(side=BOTTOM)


	# add button, action to do when pressed
	# opt parameters = fg="color",bg="color",command=somFunction
	add_button = Button(buttonsFrame,text="add task",command=lambda: addButton(level_add_task,yearStart.get(),monthStart.get(),dayStart.get(),daysActive.get(),actionTime.get(),EventType.get(),daysOfTheWeek.get(),hour.get(),minute.get(),actionInformation.get(),Description.get()))
	add_button.pack(side=TOP)

def addUniqueButton(layer,year,month,day,hour,minute,actionTime,EventType,actionInformation,Description):
	if( year.isnumeric() and month.isnumeric() and day.isnumeric() and hour.isnumeric() and minute.isnumeric() and actionTime.isnumeric() ):
		firstAction = mardb("insert into Event(actionTime,EventTypeId,hour,minute,actionInformation,Description) values("+str(actionTime)+",(select id from EventType where name = '"+str(EventType)+"'),"+str(hour)+","+str(minute)+",'"+str(actionInformation)+"','"+str(Description)+"' ) ; ")

		secondAction = mardb("insert into UniqueEvents(EventId,year,month,day) values((select max(id) from Event ),"+str(year)+","+str(month)+","+str(day)+") ;")
		os.system(firstAction)
		os.system(secondAction)
	else:
		errorMsg(layer,"a numeric value has been passed as string")
	

def addUniqueTaskButtonf():
	# setting labels and text boxes for the page
	level_add_task = Toplevel(frame)
	center(level_add_task,300,500)


	# the abel 
	title_of_window = Label(level_add_task,text="input all the required information")
	title_of_window.pack(side=TOP)



	# test label 
	newLine = Label(level_add_task,text="")
	newLine.pack(side=TOP)

	# yearStart label
	yearLabel = Label(level_add_task,text="year:")
	yearLabel.pack(side=TOP)
	# start entering information
	year = tk.StringVar()
	yearTextBox = tk.Entry(level_add_task, width = 50, textvariable = year)
	yearTextBox.pack(side=TOP)

	# month label
	monthLabel = Label(level_add_task,text="month:")
	monthLabel.pack(side=TOP)
	# start entering monthrmation
	month = tk.StringVar()
	monthTextBox = tk.Entry(level_add_task, width = 50, textvariable = month)
	monthTextBox.pack(side=TOP)

	# day label
	dayLabel = Label(level_add_task,text="day:")
	dayLabel.pack(side=TOP)
	# start entering dayrmation
	day = tk.StringVar()
	dayTextBox = tk.Entry(level_add_task, width = 50, textvariable = day)
	dayTextBox.pack(side=TOP)

	# weeks label
	hourLabel = Label(level_add_task,text="hour:")
	hourLabel.pack(side=TOP)
	# start entering hourrmation
	hour = tk.StringVar()
	hourTextBox = tk.Entry(level_add_task, width = 50, textvariable = hour)
	hourTextBox.pack(side=TOP)

	# minute label
	minuteLabel = Label(level_add_task,text="minute:")
	minuteLabel.pack(side=TOP)
	# start entering minutermation
	minute = tk.StringVar()
	minuteTextBox = tk.Entry(level_add_task, width = 50, textvariable = minute)
	minuteTextBox.pack(side=TOP)

	# actionTime label
	actionTimeLabel = Label(level_add_task,text="actionTime:")
	actionTimeLabel.pack(side=TOP)
	# start entering actionTimermation
	actionTime = tk.StringVar()
	actionTimeTextBox = tk.Entry(level_add_task, width = 50, textvariable = actionTime)
	actionTimeTextBox.pack(side=TOP)

	EventTypeTypeLabel = Label(level_add_task,text="EventType:")
	EventTypeTypeLabel.pack(side=TOP)
	
	EventTypes = [
	"alarm",
	"alert",
	"zoom",
	"circadian-alert",
	"circadian-zoom",
	"circadian-alarm"
	]
	
	EventType = tk.StringVar()
	EventType.set(EventTypes[0]) # default value
	
	EventTypeDropMenu = OptionMenu(level_add_task, EventType, *EventTypes)
	EventTypeDropMenu.pack()



	
	# actionInformation label
	actionInformationLabel = Label(level_add_task,text="actionInformation:")
	actionInformationLabel.pack(side=TOP)
	# start entering actionInformationrmation
	actionInformation = tk.StringVar()
	actionInformationTextBox = tk.Entry(level_add_task, width = 50, textvariable = actionInformation)
	actionInformationTextBox.pack(side=TOP)


	# Description label
	DescriptionLabel = Label(level_add_task,text="Description:")
	DescriptionLabel.pack(side=TOP)
	# start entering Descriptionrmation
	Description = tk.StringVar()
	DescriptionTextBox = tk.Entry(level_add_task, width = 50, textvariable = Description)
	DescriptionTextBox.pack(side=TOP)

	# =============
	# ==== the frame for the buttoms =====
	# =============
	# the frame for the buttons
	buttonsFrame = Frame(level_add_task)
	buttonsFrame.pack()

	# back button
	# opt parameters = fg="color",bg="color",command=somFunction
	back_button = Button(buttonsFrame,text="back",command=lambda: deleteTopLevel(level_add_task))
	back_button.pack(side=BOTTOM)


	# add button, action to do when pressed
	# opt parameters = fg="color",bg="color",command=somFunction
	add_button = Button(buttonsFrame,text="add task",command=lambda: addUniqueButton(level_add_task,year.get(),month.get(),day.get(),hour.get(),minute.get(),actionTime.get(),EventType.get(),actionInformation.get(),Description.get()))
	add_button.pack(side=TOP)


def getYear():
	return int(str(subprocess.check_output(['date','+%G']).decode('utf-8')))

def calculateYearDay(day,month,months):
	ans = 0
	if month > 12 or day > 31:
		return 500

	for i in range(1,month):
		ans+=months[i]
	ans+=day
	return ans

def graphWeeklyTasks():
	tempWeeklyTable = createTempWeeklyTable()
	cyear = getYear()
	print(tempWeeklyTable[0])
	# Declaring a figure "gnt"
	fig, gnt = plt.subplots()
	# Setting Y-axis limits
	gnt.set_ylim(0, 80)
	# Setting X-axis limits
	gnt.set_xlim(0, 366)
	# Setting labels for x-axis and y-axis
	gnt.set_xlabel(str(getYear()))
	gnt.set_ylabel('tasks')

	february = 28
	if cyear%4 == 0: february = 29
	months = {1:31,2:february,3:31,4:30,5:31,6:30,7:31,8:31,9:30,10:31,11:30,12:31}

	# Setting graph attribute
	gnt.grid(True)
	# 0 ,1   ,2                ,3         ,4        ,5         ,6       ,7         ,8   ,9   ,10    ,11
	# id,name,actionDescription,actionTime,yearStart,monthStart,dayStart,daysActive,days,hour,minute,actionInformation
	labels = []
	ticks = []
	for row in range(1,len(tempWeeklyTable)):
		dayStart = calculateYearDay(int(tempWeeklyTable[row][6]),int(tempWeeklyTable[row][5]),months)
		gnt.broken_barh([(dayStart,dayStart+int(tempWeeklyTable[row][7]))],(int(row)*8,4))
		labels.append(tempWeeklyTable[row][1]+" hour: "+str(tempWeeklyTable[row][9])+"")
		ticks.append(int(row)*8 + 2)

	gnt.set_yticklabels(labels)
	gnt.set_yticks(ticks)
	plt.show()


def main():
	center(root,300,500)

	backFrame = Frame(root)
	backFrame.pack(side=BOTTOM)

	# opt parameters
	label_window = Label(frame,text="")
	label_window.pack(side=TOP) 

	label_window = Label(frame,text="menu for editing tasks")
	label_window.pack(side=TOP) 

	label_window = Label(frame,text="")
	label_window.pack(side=TOP) 

	label_window = Label(frame,text="")
	label_window.pack(side=TOP) 

	# opt parameters = fg="color",bg="color",command=somFunction
	addButton = Button(frame,text="add weekly task",command=addWeeklyTask)
	addButton.pack(side=TOP)

	# to add unique task
	# opt parameters = fg="color",bg="color",command=lambda: function(params)
	addUniqueTaskButton = Button(frame,text="add unique task",command=addUniqueTaskButtonf)
	addUniqueTaskButton.pack(side=TOP)

	# opt parameters = fg="color",bg="color",command=somFunction
	queryWeeklyButton = Button(frame,text="query weekly tasks",command=queryWeeklyTasks)
	queryWeeklyButton.pack(side=TOP)

	# opt parameters = fg="color",bg="color",command=somFunction
	queryUniqueButton = Button(frame,text="query unique tasks",command=queryUniqueTasks)
	queryUniqueButton.pack(side=TOP)

	# opt parameters = fg="color",bg="color",command=somFunction
	queryUniqueButton = Button(frame,text="graph weekly tasks",command=graphWeeklyTasks)
	queryUniqueButton.pack(side=TOP)

	# opt parameters = fg="color",bg="color",command=somFunction
	close = Button(backFrame,text="exit",command=exitProgram)
	close.pack(side=TOP)

	root.mainloop()

root = Tk()
frame = Frame(root)
# pack is for piling elements and grid is like a spread sheet
frame.pack()
main()
