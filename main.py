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
	print("\nactive: " + str(active) + "\nalarm active: " + str(alarmActive) + "\ntime playing  :" + str(timePlaying) + "\nzoom class record active: " + str(zoomClassRecorderActive) + "\n zoom class opener: " + str(zoomClassOpener))
	info,action,name = scheduler.getInfoActionName()
	print("name: " + name + "\naction: " + action +  "\ninfo: " + info)
	if action == 'music'  and active and alarmActive:
		alarm.playmusic(info)
	elif action == 'zoom' and active and zoomClassOpener:
		print("enter zoom")
		utilities.giveWarning(1,"initiating zoom meeting")
		initZoom.initZoom(info)
		if zoomClassRecorderActive:
			screenRecorder.recordScreen(10000,name)
		print("enter for cicle: ")
		t.sleep(5400)
		scheduler.closeWindow()
	elif action == 'false':
		print("pass: getInfoActionName() error")
	t.sleep(mainCicleRepetition)



if __name__ == '__main__':
	# search for link in csv
	utilities.giveWarning(1,"automation suite has started")
	while 1:
		menu()
	#record the scren

