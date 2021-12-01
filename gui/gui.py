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

def addButton(frame,info,action,name,weeks,action_time,hour,minute):
	print(info.get(),action.get(),name.get(),weeks.get(),action_time.get(),hour.get(),minute.get())
	info = info.get()
	action = action.get()
	name = name.get()
	weeks = weeks.get()
	action_time = action_time.get()
	hour = hour.get()
	minute = minute.get()

	if( weeks.isnumeric() and action_time.isnumeric() and hour.isnumeric() and minute.isnumeric()):

		addRecurrentTask = "mariadb --execute=\"use automation_suite ; insert into recurrent_actions_table(info,action,name,weeks,action_time,hour,minute) values("+sur(info) +","+ sur(action) +","+ sur(name) +","+ str(weeks) +","+ str(action_time) +","+ str(hour) +","+ str(minute) +") ;\" "
		print(addRecurrentTask)
		os.system(addRecurrentTask)
	elif ( not weeks.isnumeric() ):
		errorMsg(frame,"weeks has to be a numeric value")
	elif ( not action_time.isnumeric() ):
		errorMsg(frame,"action_time has to be a numeric value")
	elif ( not hour.isnumeric() ):
		errorMsg(frame,"hour has to be a numeric value")
	elif ( notminute.isnumeric() ):
		errorMsg(frame,"minute has to be a numeric value")


def addTask():
	level_add_task = Toplevel(frame)
	center(level_add_task,300,500)


	# the abel 
	title_of_window = Label(level_add_task,text="input all the required information")
	title_of_window.pack(side=TOP)



	# test label 
	newLine = Label(level_add_task,text="")
	newLine.pack(side=TOP)

	# info label
	infoLabel = Label(level_add_task,text="info:")
	infoLabel.pack(side=TOP)
	# start entering information
	info = tk.StringVar()
	infoTextBox = tk.Entry(level_add_task, width = 50, textvariable = info)
	infoTextBox.pack(side=TOP)

	# action label
	actionLabel = Label(level_add_task,text="action:")
	actionLabel.pack(side=TOP)
	# start entering actionrmation
	action = tk.StringVar()
	actionTextBox = tk.Entry(level_add_task, width = 50, textvariable = action)
	actionTextBox.pack(side=TOP)

	# name label
	nameLabel = Label(level_add_task,text="name:")
	nameLabel.pack(side=TOP)
	# start entering namermation
	name = tk.StringVar()
	nameTextBox = tk.Entry(level_add_task, width = 50, textvariable = name)
	nameTextBox.pack(side=TOP)

	# weeks label
	weeksLabel = Label(level_add_task,text="weeks:")
	weeksLabel.pack(side=TOP)
	# start entering weeksrmation
	weeks = tk.StringVar()
	weeksTextBox = tk.Entry(level_add_task, width = 50, textvariable = weeks)
	weeksTextBox.pack(side=TOP)

	# action_time label
	action_timeLabel = Label(level_add_task,text="action_time:")
	action_timeLabel.pack(side=TOP)
	# start entering action_timermation
	action_time = tk.StringVar()
	action_timeTextBox = tk.Entry(level_add_task, width = 50, textvariable = action_time)
	action_timeTextBox.pack(side=TOP)

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


	# add button
	# opt parameters = fg="color",bg="color",command=somFunction
	add_button = Button(buttonsFrame,text="add task",command=lambda: addButton(level_add_task,info,action,name,weeks,action_time,hour,minute))
	add_button.pack(side=TOP)

	print(str(info),str(action),str(name),str(weeks),str(action_time),str(hour),str(minute))





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
	addButton = Button(frame,text="add task",command=addTask)
	addButton.pack(side=TOP)

	# opt parameters = fg="color",bg="color",command=somFunction
	deleteButton = Button(frame,text="delete or alter task",comman=deleteTasks)
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





