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
# =============
# ==== buttons =====
# =============

def addButton(yearStart,monthStart,dayStart,daysActive,actionTime,EventType):

	if( yearStart.isnumeric() and monthStart.isnumeric() and dayStart.isnumeric() and daysActive.isnumeric() and actionTime.isnumeric() ):
		firstAction = "mariadb --execute=\"use automation_suite ; insert into Event(actionTime,EventTypeId) values("+str(actionTime)+",(select id from EventType where name == '"+str(EventType)+"')) ;\" "
		secondAction = "mariadb --execute=\"use automation_suite ; insert into WeeklyEvents(EventId,yearStart,monthStart,dayStart,daysActive) values((select count(id) from Event),"+str(yearStart)+","+str(monthStart)+","+str(dayStart)+","+str(daysActive)+") ;\" "

def add
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
	add_button = Button(buttonsFrame,text="add task",command=lambda: addButton(yearStart.get(),monthStart.get(),dayStart.get(),daysActive.get(),actionTime.get(),EventType.get()))
	add_button.pack(side=TOP)


def addUniqueTaskButton():
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
	add_button = Button(buttonsFrame,text="add task",command=lambda: addUniqueButton(year,month,day,hour,minute,actionTime,EventType))
	add_button.pack(side=TOP)


def deleteTasks():
	print("hola")

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
	addUniqueTaskButton = Button(frame,text="add unique task",command=addUniqueTaskButton).pack(side=TOP)

	# opt parameters = fg="color",bg="color",command=somFunction
	deleteButton = Button(frame,text="delete or alter weekly tasks",command=deleteTasks)
	deleteButton.pack(side=TOP)

	# opt parameters = fg="color",bg="color",command=somFunction
	close = Button(backFrame,text="exit",command=exitProgram)
	close.pack(side=TOP)


	

	root.mainloop()


root = Tk()
frame = Frame(root)
# pack is for piling elements and grid is like a spread sheet
frame.pack()

main()





