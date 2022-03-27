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
from screenRecorder import ScreenRecorder
from alarm import Alarm
from initZoom import InitZoom
from scheduler import Scheduler
# import scheduler
import presets
from utilities import Utilities
# browser configurations

def buildStateMessage():
	state=""
	if not presets.active:
		state+="\nactive: " + str(presets.active)
	if not presets.alarmActive:
		state += "\nalarm active: " +str(presets.alarmActive)
	if not presets.zoomClassOpener:
		state += "\nzoomClassOpener: " +str(presets.zoomClassOpener)
	if state != "":
		state += "\ntime playing: " +str(presets.timePlaying)
	return state

def menu():
	os.system("notify-send \"initiated cicle\"")
	# the state of the program
	state = buildStateMessage()
	# notify the state
	if state != "":
		os.system("notify-send \""+state+"\"")
		print(state)

	# get info = link,action
	# name = name of the action
	# action = action
	info,action,name,actionTime,Description = Scheduler().getInfoActionName()
	print("name: " + str(name) + "\naction: " + str(action) +  "\ninfo: " + str(info) + "\naction time: " + str(actionTime) + "Description: " + str(Description))
	# if it is time to execute the alarm
	if action == 'alarm'  and presets.active and presets.alarmActive and Utilities().checkIfActive()[1]:
		if Utilities().InternetConnection():
			Utilities().giveWarning(1,"initiating main alarm")
			print(presets.youtubeUrls_minTime)
			Utilities().playYoutubeVideos(presets.youtubeUrls_minTime)
			Alarm().playmusic(info,int(actionTime),presets.circadianRitmAlarmVolume)
			if presets.schedulePrint:
				Utilities().schedulePrint()
		else:
			Utilities().giveWarning(1,"initiating main alarm")
			Alarm().playmusic(info,int(actionTime),presets.circadianRitmAlarmVolume)
			if presets.schedulePrint:
				Utilities().schedulePrint()
	# if it is time to initiate a meeting
	elif action == 'zoom' and presets.active and presets.zoomClassOpener and Utilities().checkIfActive()[0]:
		InitZoom().initZoom(info,name,actionTime,Description)
	elif action == 'alert' and presets.active and presets.alertActive and Utilities().checkIfActive()[2]:
		Utilities().giveWarning(actionTime,info)
	elif actionTime == 'false':
		print("pass: getInfoActionName() error")
	t.sleep(presets.mainCicleRepetition)


if __name__ == '__main__':
	presets.init()
	Utilities().deleteSoundDirectory()
	while 1:
		try:
			presets.init()
			menu()
		except Exception as e:
			os.system("echo \"=============\n\n"+str(e)+"\n\n==========\" >> Log/exceptionLog")
			Utilities().giveWarning(1,"an exception has ocured")
			t.sleep(30)

