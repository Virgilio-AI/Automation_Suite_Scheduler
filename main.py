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
import presets
import utilities
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
	print("\ninitiated cycle")
	print("circadian alarm: " + str(presets.circadianRitmHour) + ":" + str(presets.circadianRitmMinute))
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
	info,action,name,actionTime = scheduler.getInfoActionName()
	print("name: " + str(name) + "\naction: " + str(action) +  "\ninfo: " + str(info) + "\naction time: " + str(actionTime))
	# if it is time to execute the alarm
	if action == 'music'  and presets.active and presets.alarmActive and utilities.checkIfActive()[1]:
		utilities.giveWarning(1,"initiating main alarm")
		alarm.playmusic(info,actionTime,presets.circadianRithmAlarmVolume)
	# if it is time to initiate a meeting
	elif action == 'zoom' and presets.active and presets.zoomClassOpener and utilities.checkIfActive()[0]:
		initZoom.initZoom(info,name,actionTime)
	elif action == 'alert' and presets.active and presets.alertActive and utilities.checkIfActive()[2]:
		utilities.giveWarning(actionTime,info)
	elif actionTime == 'false':
		print("pass: getInfoActionName() error")
	t.sleep(presets.mainCicleRepetition)



if __name__ == '__main__':
	# search for link in csv
	presets.init()
	utilities.giveWarning(1,"automation suite has started")
	while 1:
		try:
			presets.init()
			menu()
		except:
			utilities.giveWarning(1,"an exception has ocured")
			t.sleep(30)
	#record the scren

