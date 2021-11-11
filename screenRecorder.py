
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
import utilities

def splitStringByString(strin,delimeter):
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

def getNameOfWindowDisplayingTheClass():
	windowsOut=subprocess.check_output(['wmctrl', '-l']).decode('utf-8')
	windowsOutByLines = splitStringByString(windowsOut,'\n')
	nameOfWindow=""
	for line in windowsOutByLines:
		words = line.split(' ')
		if words[len(words)-1] == "Brave" :
			nameOfWindow += words[4]
			for element in range(5, len(words)):
				nameOfWindow += " " + words[element]
	return nameOfWindow
def parseName(strin):
	ans=""
	for a in strin:
		if a == ' ':
			ans+='_'
		else:
			ans+=a
	return ans

def recordScreen(time,materia):
	nameOfWindow = getNameOfWindowDisplayingTheClass()
	dateCommand = subprocess.check_output(['date']).decode('utf-8').split(' ')
	mes = dateCommand[1]
	materia = parseName(materia)
	name = materia + "_" + dateCommand[0] +"_" + dateCommand[2] +"_" + dateCommand[1] +"_" + dateCommand[6][0:len(dateCommand[6])-1]
	parentDirectory = zoomClasesDirectory + "/" + materia + "/" +mes
	try:
		subprocess.check_call(['mkdir', '-p', ''+parentDirectory+''])
	except:
		print("could not create the folder")

	utilities.giveWarning(2,"started to record screen")
	commandForScreenRecord = "ffmpeg -video_size 1366x768 -framerate 25 -f x11grab -i :0.0+1920+0 -f pulse -ac 2 -i alsa_output.pci-0000_00_1f.3.analog-stereo.monitor -t "+str(time)+" "+parentDirectory+"/" + name+".mkv &"
	utilities.giveWarning(2,"ended screen recorging")
	os.system(commandForScreenRecord)
	print(commandForScreenRecord)

