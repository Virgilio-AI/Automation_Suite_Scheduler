#!/usr/bin/python
# Fecha: 05/November/2021 - Friday
# Autor: Virgilio Murillo Ochoa
# personal github: Virgilio-AI
# linkedin: https://www.linkedin.com/in/virgilio-murillo-ochoa-b29b59203
# contact: virgiliomurilloochoa1@gmail.com
# python imports
import pyautogui as pg
import pandas as pd
from datetime import datetime
import os
import time as t
import traceback
# local python files imports
from utilities import Utilities
from presets import *
from screenRecorder import ScreenRecorder
class InitZoom():
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

	def forkIfDifferent(s,time,signed):
		counter=0
		while 1:
			counter+=0.2
			if counter == time:
				print("not found")
				return -1
			try:
				xb,yb = pg.locateCenterOnScreen(signed,confidence=0.9)
				x,y = pg.locateCenterOnScreen(s.finalJoinButton,confidence=0.9)
				pg.moveTo(x,y,0.1)
				pg.click()
				return 1
			except:
				pass
			try:
				x,y = pg.locateCenterOnScreen(s.singInButton,confidence=0.9)
				pg.moveTo(x,y,0.1)
				pg.click()
				return 2
			except:
				pass
			t.sleep(0.2)
	def closeAllBrowserTabs(s,time):
		counter=0
		while 1:
			counter+=0.5
			print(int(counter))
			if int(counter) == time:
				return
			try:
				x,y=pg.locateCenterOnScreen(s.tabBrowserCloseButton,confidence=0.9)
				pg.moveTo(x,y,0.1)
				pg.click()
				print(x,y)
				counter=0
			except:
				t.sleep(0.2)
				pass
	def initZoom(s,link,name,actionTime,Description):
		# explorer options
		defaultBrowser='brave'
		openTerminal = 'st -e sh -c '
		bashCommands = defaultBrowser + " '" + link + "'"
		openExplorer = bashCommands + " &"
		# main program
		# warnings and information
		print("enter zoom")
		Utilities().giveWarning(3,"initiating zoom meeting")
		Utilities().giveWarning(1,"name of class, " + Description)
		Utilities().giveWarning(1,"zoom is about to start")
		# open brave with zoom and init session
		os.system(openExplorer)
		Utilities().clickUntilFound(30,s.cancelButton)
		Utilities().clickUntilFound(3,s.cancelButton)
		Utilities().clickUntilFound(5,s.joinFromBrowserButton)
		if s.forkIfDifferent(5,s.signed) == 2:
			Utilities().clickUntilFound(5,s.userButton)
			t.sleep(1)
			s.closeAllBrowserTabs(2)
			initZoom(link,name,actionTime)
		# move window to the right
		Utilities().moveToMonitorOnRight()
		# if recording is set
		if zoomClassRecorderActive:
			ScreenRecorder().recordScreen(actionTime,Description)
			print("action time:" +str(actionTime))
		print("enter for cicle: ")
		t.sleep(actionTime)
		print("close all browser tabs")
		s.closeAllBrowserTabs(2)

