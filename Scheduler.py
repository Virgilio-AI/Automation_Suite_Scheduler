
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
	windowsOut=str(subprocess.check_output(['wmctrl', '-l']))
	windowsOutByLines = splitStringByString(windowsOut,'\\')
	nameOfWindow=""
	for line in windowsOutByLines:
		words = line.split(' ')
		if words[len(words)-1] == "Brave" :
			#print(line)
			nameOfWindow += words[5]
			for element in range(6, len(words)):
				nameOfWindow += " " + words[element]
				#print(line[element])
	return nameOfWindow
