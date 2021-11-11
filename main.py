#!/usr/bin/python

# Fecha: 06/November/2021 - Saturday
# Autor: Virgilio Murillo Ochoa
# personal github: Virgilio-AI
# linkedin: https://www.linkedin.com/in/virgilio-murillo-ochoa-b29b59203
# contact: virgiliomurilloochoa1@gmail.com


# python packages import
import time as t
import matplotlib.pyplot as plt # for creating 2d plots
import numpy as np # tool for 2d plots
import sys
import os
# automation suite imports
import screenRecorder
import alarm
import initZoom
import scheduler
from presets import *
import utilities
# browser configurations



def menu():
	print("\ninitiated cycle")
	os.system("notify-send \"initiated cicle\"")
	# the state of the program
	state = "\nactive: " + str(active) + \
			"\nalarm active: " + str(alarmActive) + \
			"\ntime playing  :" + str(timePlaying) + \
			"\nzoom class record active: " + str(zoomClassRecorderActive) +  \
			"\n zoom class opener: " + str(zoomClassOpener)
	# notify the state
	os.system("notify-send \""+state+"\"")
	print(state)
	# get info = link,action
	# name = name of the action
	# action = action
	info,action,name,actionTime = scheduler.getInfoActionName()
	print("name: " + str(name) + "\naction: " + str(action) +  "\ninfo: " + str(info) + "\naction time: " + str(actionTime))
	# if it is time to execute the alarm
	if action == 'music'  and active and alarmActive:
		utilities.giveWarning(1,"initiating main alarm")
		alarm.playmusic(info,actionTime)
	# if it is time to initiate a meeting
	elif action == 'zoom' and active and zoomClassOpener:
		initZoom.initZoom(info,name,actionTime)
	elif actionTime == 'false':
		print("pass: getInfoActionName() error")
	t.sleep(mainCicleRepetition)



if __name__ == '__main__':
	# search for link in csv
	utilities.giveWarning(1,"automation suite has started")
	while 1:
		menu()
	#record the scren

