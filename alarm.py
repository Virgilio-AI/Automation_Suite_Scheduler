
# Fecha: 07/November/2021 - Sunday
# Autor: Virgilio Murillo Ochoa
# personal github: Virgilio-AI
# linkedin: https://www.linkedin.com/in/virgilio-murillo-ochoa-b29b59203
# contact: virgiliomurilloochoa1@gmail.com

import pyautogui as pg
import os
import time as t
ncmpcppExists='img_alarm/ncmpcppExists.png'
# =============
# ==== helper functions  for playing music =====
# =============
def stuckUntilFound(timeLimit,img):
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

def addPlaylist():
	pg.press('a')
	t.sleep(0.01)
	pg.press("enter")
	t.sleep(0.01)
	pg.press("enter")
	t.sleep(0.01)
def addAllSongs():
	t.sleep(0.01)
	pg.press('2')
	for element in range(0, 10):
		t.sleep(0.01)
		pg.press('j')
		addPlaylist()
def clearMusic():
	pg.press('1')
	t.sleep(0.01)
	pg.press('c')
	t.sleep(0.01)
	pg.press('y')
def enterToPlaylist():
	pg.press("1")
	t.sleep(0.01)
	pg.press("Z")
	t.sleep(0.01)
	pg.press("y")
	t.sleep(0.01)
	pg.press("enter")

# =============
# ==== main functions =====
# =============

def playmusic(info): # the input should be time: [time]
	trash,time = info.split(' ') # get the second part of the string
	openTerminal = 'st -e sh -c ' # open in a new terminal command
	os.system(openTerminal + "'" + "ncmpcpp" +"' &") # execute command for music
	stuckUntilFound(10,ncmpcppExists) # start the program until the image is visible
	clearMusic() # clear all previous music
	addAllSongs() # add all songs to the playlist and shuffle
	enterToPlaylist() # enter to playList
	pg.press('v')
	t.sleep(int(time)) # wait until the timer ends
	pg.press('space')
	clearMusic() # clear all the music again

