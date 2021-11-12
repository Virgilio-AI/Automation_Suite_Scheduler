
# Fecha: 10/November/2021 - Wednesday
# Autor: Virgilio Murillo Ochoa
# personal github: Virgilio-AI
# linkedin: https://www.linkedin.com/in/virgilio-murillo-ochoa-b29b59203
# contact: virgiliomurilloochoa1@gmail.com

import math

# =============
# ==== main configurations =====
# =============
active = True
# how many seconds to wait before running the main cicle again, too few seconds can be very process consuming
mainCicleRepetition = 900
# acceptance for meeting, minutes. leave the default to attend all meetings
acceptance = int(math.ceil(900/60))

# =============
# ==== alarm configurations =====
# =============
alarmActive=True
timePlaying = 1800 # in seconds

# =============
# ==== alerts =====
# =============
alertActive = True

# =============
# ==== configurations depending on the day of the week =====
# =============
mondayPresets = [ 
		True,  # for entering zoom clases
		True,  # for setting alarm
		True,  # for giving alerts
		True,  # for circadian rithm alarm
		]
tuesdayPresets = [ 
		True,  # for entering zoom clases
		True,  # for setting alarm
		True,  # for giving alerts
		True,  # for circadian rithm alarm
		]
wednesdayPresets = [ 
		True,  # for entering zoom clases
		True,  # for setting alarm
		True,  # for giving alerts
		True,  # for circadian rithm alarm
		]
thursdayPresets = [ 
		True,  # for entering zoom clases
		True,  # for setting alarm
		True,  # for giving alerts
		True,  # for circadian rithm alarm
		]
fridayPresets = [ 
		True,  # for entering zoom clases
		True,  # for setting alarm
		True,  # for giving alerts
		True,  # for circadian rithm alarm
		]
saturdayPresets = [ 
		True,  # for entering zoom clases
		True,  # for setting alarm
		True,  # for giving alerts
		True,  # for circadian rithm alarm
		]
sundayPresets = [ 
		True,  # for entering zoom clases
		True,  # for setting alarm
		True,  # for giving alerts
		True,  # for circadian rithm alarm
		]
# =============
# ==== recording zoom clases =====
# =============
zoomClassRecorderActive=True
zoomClassOpener=True


# =============
# ==== recording configurations =====
# =============
zoomClasesDirectory='/home/rockhight/Videos/clasesGrabadas/semestre5'

# =============
# ==== circadian ritm alarm clock =====
# =============
# note: this is configured for mexico, for different countries you may have to adapt it
# example:
# if you put 05:00
# then the actual time in mexico will vary from 4:30 to 5:30
# because the time changes one every six months


circadianRithmAlarm = True
circadianRithmAlarmTime = "01:20"
circadianRithmAlarmAction = "music"
circadianRithmAlarminfo = "shuffle all"
circadianRitmActionTime = 3600 # seconds

# don't edit this is you don't know what you are doing
circadianRitmHour,circadianRitmMinute = int(circadianRithmAlarmTime.split(':')[0]), int(circadianRithmAlarmTime.split(':')[1])


