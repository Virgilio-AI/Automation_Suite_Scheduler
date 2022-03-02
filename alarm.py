
# Fecha: 07/November/2021 - Sunday
# Autor: Virgilio Murillo Ochoa
# personal github: Virgilio-AI
# linkedin: https://www.linkedin.com/in/virgilio-murillo-ochoa-b29b59203
# contact: virgiliomurilloochoa1@gmail.com

import pyautogui as pg
import os
import time as t
from utilities import Utilities

ncmpcppExists='img_alarm/ncmpcppExists.png'
class Alarm():
	def addPlaylist(s):
		t.sleep(0.01)
		pg.press('a')
		t.sleep(0.01)
		pg.press("enter")
		t.sleep(0.01)
		pg.press("enter")
		t.sleep(0.01)
	def addAllSongs(s):
		t.sleep(0.01)
		pg.press('2')
		for element in range(0, 9):
			t.sleep(0.01)
			pg.press('j')
			s.addPlaylist()
	def clearMusic(s):
		t.sleep(0.01)
		pg.press('1')
		t.sleep(0.01)
		pg.press('c')
		t.sleep(0.01)
		pg.press('y')
	def enterToPlaylist(s):
		t.sleep(0.01)
		pg.press("1")
		t.sleep(0.01)
		pg.press("Z")
		t.sleep(0.01)
		pg.press("y")
		t.sleep(0.01)
		pg.press("enter")
	
		t.sleep(0.1)
		# pause the plating song
		pg.press('space')
	
	def maximizeVolumeNcmpcpp(s):
		pg.keyDown("right")
		t.sleep(2)
		pg.keyUp("right")
	# =============
	# ==== main functions =====
	# =============
	
	# wait the action and if non stop is set apply it
	def echoTime(s):
		hr,mn = Utilities().getHour()
		Utilities().giveWarningNoVolChange(4,"the time is "+str(hr)+" "+str(mn))
	def echoTimeAndPlayMusic(s,Volume,dividedBy,multipliedBy,intervals):
		os.system("pactl -- set-sink-volume 0 "+str(int(Volume*multipliedBy/dividedBy + 10))+"%") # set the volume to 80%
		t.sleep(0.5)
		s.echoTime()
		os.system("pactl -- set-sink-volume 0 "+str(int(Volume*multipliedBy/dividedBy))+"%") # set the volume to 80%
		t.sleep(0.5)
		pg.press('space')
		t.sleep(intervals)
		pg.press('space')
	
	def playmusic(s,info,actionTime,Volume): # the input should be time: [time]
		if Volume > 100:
			Volume = 100
		openTerminal = 'st -e sh -c ' # open in a new terminal command
		os.system(openTerminal + "'" + "ncmpcpp" +"' &") # execute command for music
		Utilities().clickUntilFound(5,ncmpcppExists) # start the program until the image is visible
		s.maximizeVolumeNcmpcpp()
		s.clearMusic() # clear all previous music
		s.addAllSongs() # add all songs to the playlist and shuffle
		s.enterToPlaylist() # enter to playList
		pg.press('v')
		# delay the time and work in the hours
		intervals=int(actionTime/4)+1
		# t.sleep(0.5)
		# pg.press('space')
		s.echoTimeAndPlayMusic(Volume,4,2,intervals)
		s.echoTimeAndPlayMusic(Volume,4,3,intervals)
		s.echoTimeAndPlayMusic(Volume,4,4,intervals)
		s.clearMusic() # clear all the music again
		Utilities().closeWindow()

# playmusic("this is the music",300,80)

# al = Alarm()
# al.playmusic("information",5,100)
