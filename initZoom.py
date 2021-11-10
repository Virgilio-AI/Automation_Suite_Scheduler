#!/usr/bin/python

# Fecha: 05/November/2021 - Friday
# Autor: Virgilio Murillo Ochoa
# personal github: Virgilio-AI
# linkedin: https://www.linkedin.com/in/virgilio-murillo-ochoa-b29b59203
# contact: virgiliomurilloochoa1@gmail.com

import pyautogui as pg
import pandas as pd
from datetime import datetime
import os
import time as t
import traceback

cancelButton='img_initZoom/cancelButton.png'
userButton='img_initZoom/userButton.png'
closeBraveButton='img_initZoom/closeBraveButton.png'
singInButton='img_initZoom/singInButton.png'
finalJoinButton='img_initZoom/finalJoinButton.png'
notSingned='img_initZoom/notSingned.png'
signed='img_initZoom/signed.png'
joinFromBrowserButton='img_initZoom/joinFromBrowserButton.png'
tabBrowserCloseButton='img_initZoom/tabBrowserCloseButton.png'

test='img_initZoom/test.png'



def forkIfDifferent(time,signed):
	counter=0
	while 1:
		counter+=0.2
		if counter == time:
			print("not found")
			return -1
		try:
			xb,yb = pg.locateCenterOnScreen(signed,confidence=0.9)
			x,y = pg.locateCenterOnScreen(finalJoinButton,confidence=0.9)
			pg.moveTo(x,y,0.1)
			pg.click()
			return 1
		except:
			pass
		try:
			x,y = pg.locateCenterOnScreen(singInButton,confidence=0.9)
			pg.moveTo(x,y,0.1)
			pg.click()
			return 2
		except:
			pass
		t.sleep(0.2)

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

def closeAllBrowserTabs(time):
	counter=0
	while 1:
		counter+=0.5
		print(int(counter))
		if int(counter) == time:
			return
		try:
			x,y=pg.locateCenterOnScreen(tabBrowserCloseButton,confidence=0.9)
			pg.moveTo(x,y,0.1)
			pg.click()
			print(x,y)
			counter=0
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


def initZoom(link):
	# explorer options
	defaultBrowser='brave'
	openTerminal = 'st -e sh -c '
	bashCommands = defaultBrowser + " '" + link + "'"
	openExplorer = bashCommands + " &"
	# main program
	os.system(openExplorer)
	clickUntilFound(30,cancelButton)
	clickUntilFound(5,joinFromBrowserButton)
	if forkIfDifferent(5,signed) == 2:
		clickUntilFound(5,userButton)
		t.sleep(1)
		closeAllBrowserTabs(5)
		initZoom(link)
	moveToMonitorOnRight()
#		os.system(openExplorer)
#		clickUntilFound(5,cancelButton)
#		clickUntilFound(5,joinFromBrowserButton)
#		clickUntilFound(5,finalJoinButton)

