
# Fecha: 06/November/2021 - Saturday
# Autor: Virgilio Murillo Ochoa
# personal github: Virgilio-AI
# linkedin: https://www.linkedin.com/in/virgilio-murillo-ochoa-b29b59203
# contact: virgiliomurilloochoa1@gmail.com

import subprocess
import pyautogui as pg
import pandas as pd
from datetime import datetime
import os
import time as t
import sys
import traceback
# local python files import
from presets import *
from utilities import Utilities

class ScreenRecorder():
	def splitStringByString(s,strin,delimeter):
		resultArray=[]
		counter=0
		tempStrin=''
		for element in range(0, len(strin)):
			if strin[element] == delimeter:
				resultArray.append(tempStrin)
				tempStrin=""
			else:
				tempStrin+=strin[element]
		return resultArray
	
	def getNameOfWindowDisplayingTheClass(s):
		windowsOut=subprocess.check_output(['wmctrl', '-l']).decode('utf-8')
		windowsOutByLines = s.splitStringByString(windowsOut,'\n')
		nameOfWindow=""
		for line in windowsOutByLines:
			words = line.split(' ')
			if words[len(words)-1] == "Brave" :
				nameOfWindow += words[4]
				for element in range(5, len(words)):
					nameOfWindow += " " + words[element]
		return nameOfWindow
	def getUpperLeftPossitionWidthHeightOfWindowGivingName(s,name):
		windowsOut=subprocess.check_output(['xwininfo', '-name',''+str(name)+'']).decode('utf-8')
		infoByLines = s.splitStringByString(windowsOut,'\n')
		upperLeftX = ''
		upperLeftY = ''
		width = ''
		height = ''
	
		for line in infoByLines:
			words = line.split(' ')
			if len(words) > 5 and words[2:5] == ['Absolute','upper-left','X:']:
				upperLeftX = words[-1]
			if len(words) > 5 and words[2:5] == ['Absolute','upper-left','Y:']:
				upperLeftY = words[-1]
			if len(words) > 1 and words[2] == 'Width:':
				width = words[-1]
			if len(words) > 1 and words[2] == 'Height:':
				height = words[-1]
		return upperLeftX,upperLeftY,width,height
	
	
	
	def parseName(s,strin):
		ans=""
		for a in strin:
			if a == ' ':
				ans+='_'
			else:
				ans+=a
		return ans
	
	def recordScreen(s,time,materia):
		nameOfWindow = s.getNameOfWindowDisplayingTheClass()
		dateCommand = subprocess.check_output(['date']).decode('utf-8').split(' ')
		hour = subprocess.check_output(['date','+%H']).decode('utf-8').split(' ')
		mes = dateCommand[1]
		day = dateCommand[3]
		materia = s.parseName(materia)
		name = materia + "_" + dateCommand[0] +"_" + day +"_" + dateCommand[1] +"_" + dateCommand[6][0:len(dateCommand[6])-1] + "_hr-"  +str(hour)
		parentDirectory = zoomClasesDirectory + "/" + materia + "/" +mes
		try:
			subprocess.check_call(['mkdir', '-p', ''+parentDirectory+''])
			print(parentDirectory)
		except Exception as e:
			print(e)
			print("could not create the folder")
	
		Utilities().giveWarning(2,"started to record screen")
		print(time)
		winName = s.getNameOfWindowDisplayingTheClass()
		upperLeftX,upperLeftY,width,height = s.getUpperLeftPossitionWidthHeightOfWindowGivingName(winName)
		commandForScreenRecord = "ffmpeg -video_size "+str(width)+"x"+str(height)+" -framerate 25 -f x11grab -i :0.0+"+str(upperLeftX)+"+"+str(upperLeftY)+" -f pulse -ac 2 -i alsa_output.pci-0000_00_1f.3.analog-stereo.monitor -t "+str(time)+" "+parentDirectory+"/" + name+".mkv &"
		print("====== command for record screen === ")
		print(commandForScreenRecord)
		print("===================================")
		os.system(commandForScreenRecord)
		Utilities().giveWarning(2,"ended screen recorging")
