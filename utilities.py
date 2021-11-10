
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


