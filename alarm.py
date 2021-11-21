
# Fecha: 07/November/2021 - Sunday
# Autor: Virgilio Murillo Ochoa
# personal github: Virgilio-AI
# linkedin: https://www.linkedin.com/in/virgilio-murillo-ochoa-b29b59203
# contact: virgiliomurilloochoa1@gmail.com

import pyautogui as pg
import os
import time as t
import utilities

ncmpcppExists='img_alarm/ncmpcppExists.png'

def addPlaylist():
	t.sleep(0.01)
	pg.press('a')
	t.sleep(0.01)
	pg.press("enter")
	t.sleep(0.01)
	pg.press("enter")
	t.sleep(0.01)
def addAllSongs():
	t.sleep(0.01)
	pg.press('2')
	for element in range(0, 9):
		t.sleep(0.01)
		pg.press('j')
		addPlaylist()
def clearMusic():
	t.sleep(0.01)
	pg.press('1')
	t.sleep(0.01)
	pg.press('c')
	t.sleep(0.01)
	pg.press('y')
def enterToPlaylist():
	t.sleep(0.01)
	pg.press("1")
	t.sleep(0.01)
	pg.press("Z")
	t.sleep(0.01)
	pg.press("y")
	t.sleep(0.01)
	pg.press("enter")
def maximizeVolumeNcmpcpp():
	for it in range(1,30):
		t.sleep(0.01)
		pg.press("right")
# =============
# ==== main functions =====
# =============

# wait the action and if non stop is set apply it

def playmusic(info,actionTime,Volume): # the input should be time: [time]
	openTerminal = 'st -e sh -c ' # open in a new terminal command
	os.system(openTerminal + "'" + "ncmpcpp" +"' &") # execute command for music
	utilities.waitUntilFound(10,ncmpcppExists) # start the program until the image is visible
	os.system("pactl -- set-sink-volume 0 "+str(Volume)+"%") # set the volume to 80%
	maximizeVolumeNcmpcpp()
	clearMusic() # clear all previous music
	addAllSongs() # add all songs to the playlist and shuffle
	enterToPlaylist() # enter to playList
	pg.press('v')
	t.sleep(int(actionTime))
	t.sleep(0.01)
	pg.press('space')
	clearMusic() # clear all the music again
	utilities.closeWindow()
