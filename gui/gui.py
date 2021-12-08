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
	queryUniqueBut = Button(buttonsFrame,text="query with the given constrains",command=lambda: queryWeeklyButton(EventType.get(),actionTime.get(),yearStart.get(),monthStart.get(),dayStart.get()))
	queryUniqueBut.pack(side=TOP)
def queryWeeklyButton(EventType,actionTime,yearStart,monthStart,dayStart):
	command = ("""select WeeklyEvents.id as `WeeklyEvent_id`,EventType.name,EventType.actionDescription,Event.actionTime,WeeklyEvents.yearStart,
WeeklyEvents.monthStart,WeeklyEvents.dayStart,WeeklyEvents.daysActive,group_concat(DayOfTheWeek.day) as `days`,Event.actionInformation 
from DayOfTheWeek
inner join WeeklyEvents_DayOfTheWeek on WeeklyEvents_DayOfTheWeek.DayOfTheWeekId = DayOfTheWeek.id
inner join WeeklyEvents on WeeklyEvents.id = WeeklyEvents_DayOfTheWeek.WeeklyEventsId 
inner join Event on WeeklyEvents.EventId = Event.id
inner join EventType on EventType.id = Event.EventTypeId\n""")
	first =False
	if (EventType != "" or actionTime != "" or yearStart != "" or monthStart != "" or dayStart != ""):
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

	if first:
		command += ")\n"

	command+="group by WeeklyEvents.id;"
	command = mardbs(command)
	print(command)
	
	os.system(command)
	#print(command)
def queryUniqueButton(EventType,actionTime,year,month,day):
	command = ("""

select UniqueEvents.id as `UniqueEvents id`,Event.actionTime,EventType.name,EventType.actionDescription as `description`,UniqueEvents.year,UniqueEvents.month,UniqueEvents.day,Event.hour,Event.minute as `min`,Event.hour,Event.minute,Event.actionInformation
from EventType
inner join Event on EventType.id = Event.EventTypeId
inner join UniqueEvents on UniqueEvents.EventId = Event.id """)
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
	os.system(command)
	#print(command)
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
def deleteWeeklyButton(EventType,actionTime,yearStart,monthStart,dayStart):
	command = ("""select WeeklyEvents.id as `WeeklyEvent_id`,EventType.name,EventType.actionDescription,Event.actionTime,WeeklyEvents.yearStart,
WeeklyEvents.monthStart,WeeklyEvents.dayStart,WeeklyEvents.daysActive,group_concat(DayOfTheWeek.day) as `days`, Event.actionInformation
from DayOfTheWeek
inner join WeeklyEvents_DayOfTheWeek on WeeklyEvents_DayOfTheWeek.DayOfTheWeekId = DayOfTheWeek.id
inner join WeeklyEvents on WeeklyEvents.id = WeeklyEvents_DayOfTheWeek.WeeklyEventsId 
inner join Event on WeeklyEvents.EventId = Event.id
inner join EventType on EventType.id = Event.EventTypeId\n""")
	first =False
	if (EventType != "" or actionTime != "" or yearStart != "" or monthStart != "" or dayStart != ""):
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

	if first:
		command += ")\n"

	command+="group by WeeklyEvents.id;"
	command = mardbs(command)
	print(command)
	
	#os.system(command)
	#print(command)
def deleteUniqueButton(EventType,actionTime,year,month,day):
	command = ""
	if EventType == "" and actionTime == "" and year == "" and month == "" and day == "" :
		command = "delete * from Event "
	else :
		first = True
		command += "delete from Event where Event.id = ( select EventId from UniqueEvents where("
		if actionTime != "" :
			if first:
				command += "UniqueEvents.actionTime = "+str(actionTime)+" "
				first=False
			else:
				command += " and UniqueEvents.actionTime = "+str(actionTime)+" "
		if year != "":
			if first:
				first=False
				command += "UniqueEvents.year = "+str(year)+""
			else:
				command += " and UniqueEvents.year = "+str(year)+""
		if month != "":
			if first:
				first=False
				command += "UniqueEvents.month = "+str(month)+""
			else:
				command += " and UniqueEvents.month = "+str(month)+""
		if day != "":
			if first:
				first=False
				command += "UniqueEvents.day = "+str(day)+""
			else:
				command += " and UniqueEvents.day = "+str(day)+""
		command += "))"

	command += " ; \n"
	command = mardbs(command)
	os.system(command)

	# print(command)
def deleteWeeklyTasks():
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
	deleteWeeklyBut = Button(buttonsFrame,text="delete with the given constrains",command=lambda: deleteWeeklyButton(EventType.get(),actionTime.get(),yearStart.get(),monthStart.get(),dayStart.get()))
	deleteWeeklyBut.pack(side=TOP)
def deleteUniqueTasks():
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
	deleteUniqueTasksButton = Button(buttonsFrame,text="delete with the given constrains ",command=lambda: deleteUniqueButton(EventType.get(),actionTime.get(),year.get(),month.get(),day.get()))
	deleteUniqueTasksButton.pack(side=TOP)

def addButton(layer,yearStart,monthStart,dayStart,daysActive,actionTime,EventType,daysOfTheWeek,hour,minute):
	daysOfTheWeekdic = {1:"monday",2:"thurday",3:"wednesday",4:"tuesday",5:"friday",6:"saturday",7:"sunday"}
	daysOfTheWeekArr = daysOfTheWeek.split(',')
	for it in daysOfTheWeekArr:
		if not ( it in daysOfTheWeekdic.values()):
			errorMsg(layer,"error: "+str(it)+"not in dictionary")
			return

	if( yearStart.isnumeric() and monthStart.isnumeric() and dayStart.isnumeric() and daysActive.isnumeric() and actionTime.isnumeric() and hour.isnumeric() and minute.isnumeric() ):
		firstAction = mardb("insert into Event(actionTime,EventTypeId,hour,minute) values("+str(actionTime)+",(select id from EventType where name = '"+str(EventType)+"' ),"+str(hour)+","+str(minute)+") ; ")
		os.system(firstAction)
		secondAction = mardb("insert into WeeklyEvents(EventId,yearStart,monthStart,dayStart,daysActive) values((select count(id) from Event),"+str(yearStart)+","+str(monthStart)+","+str(dayStart)+","+str(daysActive)+") ;")
		os.system(secondAction)
		print(firstAction)
		print(secondAction)



		for element in range(0, len(daysOfTheWeekArr)):
			tempAction = mardb("insert into WeeklyEvents_DayOfTheWeek(WeeklyEventsId,DayOfTheWeekId) values((select count(id) from WeeklyEvents),(select id from DayOfTheWeek where day = '"+str(daysOfTheWeekArr[element])+"'));")
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
	# start entering EventTypermation
	EventType = tk.StringVar()
	EventTypeTextBox = tk.Entry(level_add_task, width = 50, textvariable = EventType)
	EventTypeTextBox.pack(side=TOP)

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
	add_button = Button(buttonsFrame,text="add task",command=lambda: addButton(level_add_task,yearStart.get(),monthStart.get(),dayStart.get(),daysActive.get(),actionTime.get(),EventType.get(),daysOfTheWeek.get(),hour.get(),minute.get()))
	add_button.pack(side=TOP)

def addUniqueButton(layer,year,month,day,hour,minute,actionTime,EventType):
	if( year.isnumeric() and month.isnumeric() and day.isnumeric() and hour.isnumeric() and minute.isnumeric() and actionTime.isnumeric() ):
		firstAction = mardb("insert into Event(actionTime,EventTypeId,hour,minute) values("+str(actionTime)+",(select id from EventType where name = '"+str(EventType)+"'),"+str(hour)+","+str(minute)+") ; ")

		secondAction = mardb("insert into UniqueEvents(EventId,year,month,day) values((select count(id) from Event ),"+str(year)+","+str(month)+","+str(day)+") ;")
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


	# EventType label
	EventTypeLabel = Label(level_add_task,text="EventType:")
	EventTypeLabel.pack(side=TOP)
	# start entering EventTypermation
	EventType = tk.StringVar()
	EventTypeTextBox = tk.Entry(level_add_task, width = 50, textvariable = EventType)
	EventTypeTextBox.pack(side=TOP)

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
	add_button = Button(buttonsFrame,text="add task",command=lambda: addUniqueButton(level_add_task,year.get(),month.get(),day.get(),hour.get(),minute.get(),actionTime.get(),EventType.get()))
	add_button.pack(side=TOP)

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
	deleteWeeklyButton = Button(frame,text="delete weekly tasks",command=deleteWeeklyTasks)
	deleteWeeklyButton.pack(side=TOP)

	# opt parameters = fg="color",bg="color",command=somFunction
	deleteUniqueButton = Button(frame,text="delete unique tasks",command=deleteUniqueTasks)
	deleteUniqueButton.pack(side=TOP)

#	# opt parameters = fg="color",bg="color",command=somFunction
#	deleteButton = Button(frame,text="delete or alter weekly tasks",command=deleteWeeklyTasks)
#	deleteButton.pack(side=TOP)
#
#	# opt parameters = fg="color",bg="color",command=somFunction
#	deleteUniqueButton = Button(frame,text="delete or alter unique tasks",command=deleteUniqueTasks)
#	deleteUniqueButton.pack(side=TOP)

	# opt parameters = fg="color",bg="color",command=somFunction
	close = Button(backFrame,text="exit",command=exitProgram)
	close.pack(side=TOP)

	root.mainloop()

root = Tk()
frame = Frame(root)
# pack is for piling elements and grid is like a spread sheet
frame.pack()
main()
