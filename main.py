#!/usr/bin/python

# Fecha: 06/November/2021 - Saturday
# Autor: Virgilio Murillo Ochoa
# personal github: Virgilio-AI
# linkedin: https://www.linkedin.com/in/virgilio-murillo-ochoa-b29b59203
# contact: virgiliomurilloochoa1@gmail.com

import time as t
import screenRecorder
import alarm
import initZoom
import scheduler
import matplotlib.pyplot as plt # for creating 2d plots
import numpy as np # tool for 2d plots
import sys
import os
# browser configurations

# search the link in the csv

semestre = 5

if __name__ == '__main__':
	# search for link in csv
	while 1:
		print("initiated program")
		try:
			info,action,name = scheduler.getInfoActionName()
			print("name: " + name + "\naction: " + action +  "\ninfo: " + info)
			if action == 'music':
				alarm.playmusic(info)
			elif action == 'zoom':
				initZoom.initZoom(info)
				screenRecorder.recordScreen(10000,name,semestre)
				print("enter for cicle: ")
				t.sleep(5400)
				scheduler.closeWindow()
		except:
			print("pass: getInfoActionName() error")
		t.sleep(1800)
	#record the scren

