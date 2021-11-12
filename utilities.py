
# Fecha: 10/November/2021 - Wednesday
# Autor: Virgilio Murillo Ochoa
# personal github: Virgilio-AI
# linkedin: https://www.linkedin.com/in/virgilio-murillo-ochoa-b29b59203
# contact: virgiliomurilloochoa1@gmail.com


# python imports
import subprocess
import pyautogui as pg
import pandas as pd
from datetime import datetime
import os
import time as t
import traceback
from gtts import gTTS
import presets

def waitUntilFound(timeLimit,img):
	counter=0
	while 1:
		counter+=0.2
		if counter == timeLimit:
			print("not found")
			return -1
		try:
			x,y=pg.locateCenterOnScreen(img,confidence=0.9)
			print(x,y)
			break
		except:
			t.sleep(0.2)
			pass
def clickUntilFound(timeLimit,img):
	counter=0
	while 1:
		counter+=0.2
		if counter == timeLimit:
			print("not found")
			return -1
		try:
			x,y=pg.locateCenterOnScreen(img,confidence=0.9)
			pg.moveTo(x,y,0.1)
			pg.click()
			print(x,y)
			break
		except:
			t.sleep(0.2)
			pass


def moveToMonitorOnLeft():
	pg.keyDown('win')
	pg.keyDown('shift')
	pg.keyDown('<')
	pg.keyUp('<')
	pg.keyUp('win')
	pg.keyUp('shift')



def moveToMonitorOnRight():
	pg.keyDown('win')
	pg.keyDown('shift')
	pg.keyDown('>')
	pg.keyUp('>')
	pg.keyUp('win')
	pg.keyUp('shift')

def forceCreateDirectory(parentDirectory): # ex: name/name2
	subprocess.check_call(['mkdir', '-p', ''+parentDirectory+''])


def giveWarning(time,message):
	volumePercentage = subprocess.getoutput('pamixer --get-volume')
	t.sleep(0.01)
	os.system("pactl set-sink-mute @DEFAULT_SINK@ false ; pactl -- set-sink-volume 0 100%")
	counter = 0
	language = 'en'
	sound = gTTS(text=message,lang=language,slow=False)
	nameOfFile = "sounds/" + message.replace(" ","_") + ".mp3"
	forceCreateDirectory("sounds")
	sound.save(nameOfFile)
	while counter < time:
		os.system("notify-send \""+message+"\"")
		os.system("mpv \""+nameOfFile+"\"")
		t.sleep(1)
		counter+=1
	os.system("pactl -- set-sink-volume 0 "+volumePercentage+"%") # set the volume to 80%
	t.sleep(0.01)

def closeWindow():
	t.sleep(0.01)
	pg.keyDown('win')
	t.sleep(0.01)
	pg.keyDown('shift')
	t.sleep(0.01)
	pg.keyDown('c')
	t.sleep(0.01)
	pg.keyUp('c')
	t.sleep(0.01)
	pg.keyUp('win')
	t.sleep(0.01)
	pg.keyUp('shift')
	t.sleep(0.01)

# =============
# ==== get the time =====
# =============
def getDayOfTheWeek():
	return int(str(subprocess.check_output(['date','+%u']).decode('utf-8')))
def getMonth():
	return int(str(subprocess.check_output(['date','+%m']).decode('utf-8')))
def getHour():
	hour=int(str(subprocess.check_output(['date','+%H']).decode('utf-8')))
	minute=int(str(subprocess.check_output(['date','+%M']).decode('utf-8')))
	return hour,minute
def getDayOfTheMonth():
	return int(str(subprocess.check_output(['date','+%d']).decode('utf-8')))

# %%
# to get an hour from a string that is in the csv
def getStringHour(strin):
	return strin.split(':')[1],strin.split(':')[2]


# =============
# ==== check if avaliable =====
# =============

def checkIfActive():
	dayOfTheWeek = getDayOfTheWeek()
	if dayOfTheWeek == 1:
		return presets.mondayPresets
	if dayOfTheWeek == 2:
		return presets.tuesdayPresets
	if dayOfTheWeek == 3:
		return presets.wednesdayPresets
	if dayOfTheWeek == 4:
		return presets.thursdayPresets
	if dayOfTheWeek == 5:
		return presets.fridayPresets
	if dayOfTheWeek == 6:
		return presets.saturdayPresets
	if dayOfTheWeek == 7:
		return presets.sundayPresets


giveWarning(1,"hola mundo")
