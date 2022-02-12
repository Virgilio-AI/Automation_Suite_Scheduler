
# Fecha: 10/November/2021 - Wednesday
# Autor: Virgilio Murillo Ochoa
# personal github: Virgilio-AI
# linkedin: https://www.linkedin.com/in/virgilio-murillo-ochoa-b29b59203
# contact: virgiliomurilloochoa1@gmail.com


# python imports
import subprocess
import pyautogui as pg
import pandas as pd
from datetime import datetime as dt
import os
import time as t
import traceback

# commented so that the app works without the internet
import pyttsx3 as tts
# from gtts import gTTS
import presets
from selenium import webdriver
from bs4 import BeautifulSoup
from pytube import YouTube
from pytube import Channel
import requests


def waitUntilFound(timeLimit,img):
	counter=0
	while 1:
		counter+=0.2
		if counter >= timeLimit:
			print("not found")
			return -1
		try:
			x,y=pg.locateCenterOnScreen(img,confidence=0.7)
			print("FOUND")
			print(x,y)
			break
		except Exception as e:
			print(e)
			t.sleep(0.2)
			print("not founding")
			pass
def clickUntilFound(timeLimit,img):
	counter=0
	while 1:
		counter+=0.2
		if counter == timeLimit:
			print("not found")
			return -1
		try:
			x,y=pg.locateCenterOnScreen(img,confidence=0.7)
			pg.moveTo(x,y,0.1)
			pg.click()
			print(x,y)
			break
		except Exception as e:
			print(e)
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

def deleteSoundDirectory():
	directory = 'sounds'
	for filename in os.listdir(directory):
		f = os.path.join(directory, filename)
	# checking if it is a file
		if os.path.isfile(f):
			os.remove(f)
def forceCreateDirectory(parentDirectory): # ex: name/name2
	subprocess.check_call(['mkdir', '-p', ''+parentDirectory+''])

def giveWarningNoVolChange(time,message):
	os.system("pactl set-sink-mute @DEFAULT_SINK@ false ")
	counter = 0
	language = 'en'
	nameOfFile = "sounds/" + message.replace(" ","_") + ".mp3"
	eng = tts.init()
	# for the rate
	eng.setProperty('rate',125)
	volume = eng.getProperty('volume')   #getting to know current volume level (min=0 and max=1)
	eng.setProperty('volume',1.5)

#	voices = eng.getProperty('voices')       #getting details of current voice
	eng.setProperty('voice', 'english_rp+f3')

	while counter < time:
		os.system("notify-send \""+message+"\"")
		eng.say(message)
		eng.runAndWait()
		t.sleep(1)
		counter+=1

def giveWarning(time,message):
	volumePercentage = subprocess.getoutput('pamixer --get-volume')
	t.sleep(0.01)
	os.system("pactl set-sink-mute @DEFAULT_SINK@ false ; pactl -- set-sink-volume 0 "+str(presets.alertVolume)+"%")
	counter = 0
	language = 'en'
	nameOfFile = "sounds/" + message.replace(" ","_") + ".mp3"
	eng = tts.init()
	# for the rate
	eng.setProperty('rate',125)
	volume = eng.getProperty('volume')   #getting to know current volume level (min=0 and max=1)
	eng.setProperty('volume',1.5)

#	voices = eng.getProperty('voices')       #getting details of current voice
	eng.setProperty('voice', 'english_rp+f3')


	while counter < time:
		os.system("notify-send \""+message+"\"")
		eng.say(message)
		eng.runAndWait()
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
# ============
def getDayOfTheWeek():
	return int(str(int(dt.today().strftime('%w'))))
def getMonth():
	return int(str(int(dt.today().strftime('%m'))))
def getHour():
	return (int(dt.today().strftime('%H')),int(dt.today().strftime('%M')))
def getDayOfTheMonth():
	return int(str(int(dt.today().strftime('%d'))))
def getYear():
	return int(str(int(dt.today().strftime('%Y'))))
def getYearDay():
	return int(str(int(dt.today().strftime('%j'))))

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

# =============
# ==== utilities for interating with maria db =====
# =============

def mardb(stri):
	return "mariadb --execute=\" use automation_suite ; "+str(stri)+"\""
def mardbs(stri):
	return "mariadb --execute=' use automation_suite ; "+str(stri)+"'"
# =============
# ==== Internet connection =====
# =============
def InternetConnection():
	url = "https://www.google.com"
	timeout = 5
	try:
		request = requests.get(url, timeout=timeout)
		return True
	except (requests.ConnectionError, requests.Timeout) as exception:
		return False
# =============
# ==== connecting to a web scrapper =====
# =============
def playYoutubeVideos(urls):
	os.system("pactl -- set-sink-volume 0 80%") # set the volume to 80%
	videos = urls
	maxLen = 1800
	sumLen=0
	for video in videos:
		channel_info = Channel(video[0])
		channelMinTime= video[1]
		cont = 0
		now = dt.now()
		for url in channel_info.url_generator():
			video_details = YouTube(url)
			videoLen = video_details.length/60
			vidTime=video_details.publish_date
			publish_date = str(video_details.publish_date).split(' ')[0]
			hoursSincePublished = (now-vidTime).total_seconds()/3600
			print("url: " + str(video) )
			print("channel min time: " + str(channelMinTime))
			print("video len: " + str(videoLen))
			print("hours since published: " + str(hoursSincePublished))
			print("now: " + str(now) )
			print("vidTime: " + str(vidTime) )
# 			print("vidInfo: " + str(video_details.vid_info) )
			if hoursSincePublished < 40.0 and channelMinTime < videoLen:
				print("=====")
				print(f'Video URL: {url}')
				print(f'Video Title: {video_details.title}')
				print(f'the video length is: {videoLen}')
				print((now-vidTime).total_seconds()/3600)
				print(f'publish date: {publish_date}')
				print("=====")
				print(video_details.length)
				os.system('st -e sh -c "brave ' + url + '" &')
				yutubeImage='img_utilities/youtubeImage.png'
				waitUntilFound(20,yutubeImage)
				print("=====")
				print(video_details.length)
				t.sleep(video_details.length)
				sumLen+=video_details.length
				print("=====")
				print(video_details.length)
				pg.keyDown('ctrl')
				pg.press('w')
				pg.keyUp('ctrl')
				if maxLen < sumLen:
					break
			elif hoursSincePublished > 31:
				break
			cont+=1
			if cont > 5:
				break

def schedulePrint():
	os.system('lp horariosDiarios/today.txt')




playYoutubeVideos(presets.youtubeUrls_minTime)
