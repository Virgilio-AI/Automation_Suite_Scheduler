# Fecha: 10/November/2021 - Wednesday
# Autor: Virgilio Murillo Ochoa
# personal github: Virgilio-AI
# linkedin: https://www.linkedin.com/in/virgilio-murillo-ochoa-b29b59203
# contact: virgiliomurilloochoa1@gmail.com

import math
import json
import os


# =============
# ==== open presets.json file for current file configurations =====
# =============
with open('presets.json', 'r') as handle:
	fixed_json = ''.join(line for line in handle if not line.startswith('//'))
	presets_dt = json.loads(fixed_json)
# =============
# ==== main configurations =====
# =============
active = presets_dt["active"]
# how many seconds to wait before running the main cicle again, too few seconds can be very process consuming
mainCicleRepetition = presets_dt["mainCicleRepetition"]
# acceptance for meeting, minutes. leave the default to attend all meetings
acceptance = int(math.ceil(900/60))
# =============
# ==== alarm configurations =====
# =============
alarmActive=presets_dt["alarmActive"]
timePlaying = presets_dt["timePlaying"] # in seconds
# =============
# ==== alerts =====
# =============
alertActive = presets_dt["alertActive"]
# =============
# ==== configurations depending on the day of the week =====
# =============
mondayPresets =    presets_dt["mondayPresets"]
tuesdayPresets =   presets_dt["tuesdayPresets"]
wednesdayPresets = presets_dt["wednesdayPresets"]
thursdayPresets =  presets_dt["thursdayPresets"]
fridayPresets =    presets_dt["fridayPresets"]
saturdayPresets =  presets_dt["saturdayPresets"]
sundayPresets =    presets_dt["sundayPresets"]
# =============
# ==== recording zoom clases =====
# =============
zoomClassRecorderActive= presets_dt["zoomClassRecorderActive"]
zoomClassOpener= presets_dt["zoomClassOpener"]
# =============
# ==== recording configurations =====
# =============
zoomClasesDirectory= presets_dt["zoomClasesDirectory"]
# =============
# ==== circadian ritm alarm clock =====
# =============
circadianRithmAlarm = presets_dt["circadianRithmAlarm"]
circadianRithmAlarmTime = presets_dt["circadianRithmAlarmTime"]
circadianRithmAlarmVolume = presets_dt["circadianRithmAlarmVolume"]
circadianRithmAlarmAction = presets_dt["circadianRithmAlarmAction"]
circadianRithmAlarminfo = presets_dt["circadianRithmAlarminfo"]
circadianRitmActionTime = presets_dt["circadianRitmActionTime"]
# don't edit this is you don't know what you are doing
circadianRitmHour,circadianRitmMinute = int(circadianRithmAlarmTime.split(':')[0]), int(circadianRithmAlarmTime.split(':')[1])



# call function to refresh all global variables
def init():
	with open('presets.json', 'r') as handle:
		fixed_json = ''.join(line for line in handle if not line.startswith('//'))
		presets_dt = json.loads(fixed_json)

	active = presets_dt["active"]
	mainCicleRepetition = presets_dt["mainCicleRepetition"]
	acceptance = int(math.ceil(900/60))
	alarmActive=presets_dt["alarmActive"]
	alertActive = presets_dt["alertActive"]
	mondayPresets =    presets_dt["mondayPresets"]
	tuesdayPresets =   presets_dt["tuesdayPresets"]
	wednesdayPresets = presets_dt["wednesdayPresets"]
	thursdayPresets =  presets_dt["thursdayPresets"]
	fridayPresets =    presets_dt["fridayPresets"]
	saturdayPresets =  presets_dt["saturdayPresets"]
	sundayPresets =    presets_dt["sundayPresets"]
	zoomClassRecorderActive= presets_dt["zoomClassRecorderActive"]
	zoomClassOpener= presets_dt["zoomClassOpener"]
	zoomClasesDirectory= presets_dt["zoomClasesDirectory"]
	circadianRithmAlarm = presets_dt["circadianRithmAlarm"]
	circadianRithmAlarmTime = presets_dt["circadianRithmAlarmTime"]
	circadianRithmAlarmVolume = presets_dt["circadianRithmAlarmVolume"]
	circadianRithmAlarmAction = presets_dt["circadianRithmAlarmAction"]
	circadianRithmAlarminfo = presets_dt["circadianRithmAlarminfo"]
	circadianRitmActionTime = presets_dt["circadianRitmActionTime"]
	circadianRitmHour,circadianRitmMinute = int(circadianRithmAlarmTime.split(':')[0]), int(circadianRithmAlarmTime.split(':')[1])
