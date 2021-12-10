
# Fecha: 08/December/2021 - Wednesday
# Autor: Virgilio Murillo Ochoa
# personal github: Virgilio-AI
# linkedin: https://www.linkedin.com/in/virgilio-murillo-ochoa-b29b59203
# contact: virgiliomurilloochoa1@gmail.com

import json

# so that you can open the presets correctly
with open('presets.json', 'r') as handle:
	fixed_json = ''.join(line for line in handle if not line.startswith('//'))
	# to ignore the comments that are inside the file
	presets_dt = json.loads(fixed_json)
# get the circadian rithm alarm preset

# configurations for the whole program
active = presets_dt['Active']
alarmActive = presets_dt['alarmActive']
mainCicleRepetition = presets_dt['mainCicleRepetition']
acceptance = presets_dt['acceptance']


# main configurations for alerts
alertVolume = presets_dt['alertVolume']
alertActive = presets_dt['alertActive']



# configurations for zoom
zoomClassOpener = presets_dt['zoomClassOpener']
zoomClassRecorderActive = presets_dt['zoomClassRecorderActive']

# 
mondayPresets = presets_dt["monday"]
tuesdayPresets = presets_dt["tuesday"]
wednesdayPresets = presets_dt["wednesday"]
thursdayPresets = presets_dt["thursay"]
fridayPresets = presets_dt["friday"]
saturdayPresets = presets_dt["saturday"]
sundayPresets = presets_dt["sunday"]






circadianRitmAlarminfo = presets_dt["circadianRitmAlarminfo"]
circadianRitmAlarmAction = presets_dt["circadianRitmAlarmAction"]
circadianRitmActionTime = presets_dt["circadianRitmActionTime"]
circadianRitmAlarmTime = presets_dt["circadianRitmAlarmTime"]
circadianRitmAlarmVolume = presets_dt["circadianRitmAlarmVolume"]


# configruations for the alarm
timePlaying = presets_dt["timePlaying"]




def init():
	# so that you can open the presets correctly
	with open('presets.json', 'r') as handle:
		fixed_json = ''.join(line for line in handle if not line.startswith('//'))
		# to ignore the comments that are inside the file
		presets_dt = json.loads(fixed_json)
	# get the circadian rithm alarm preset
	
	# configurations for the whole program
	active = presets_dt['Active']
	alarmActive = presets_dt['alarmActive']
	mainCicleRepetition = presets_dt['mainCicleRepetition']
	acceptance = presets_dt['acceptance']


	# main configurations for alerts
	alertVolume = presets_dt['alertVolume']
	alertActive = presets_dt['alertActive']



	# configurations for zoom
	zoomClassOpener = presets_dt['zoomClassOpener']
	zoomClassRecorderActive = presets_dt['zoomClassRecorderActive']

	# 
	mondayPresets = presets_dt["monday"]
	tuesdayPresets = presets_dt["tuesday"]
	wednesdayPresets = presets_dt["wednesday"]
	thursdayPresets = presets_dt["thursay"]
	fridayPresets = presets_dt["friday"]
	saturdayPresets = presets_dt["saturday"]
	sundayPresets = presets_dt["sunday"]






	circadianRitmAlarminfo = presets_dt["circadianRitmAlarminfo"]
	circadianRitmAlarmAction = presets_dt["circadianRitmAlarmAction"]
	circadianRitmActionTime = presets_dt["circadianRitmAlarmAction"]
	circadianRitmAlarmTime = presets_dt["circadianRitmAlarmTime"]
	circadianRitmAlarmVolume = presets_dt["circadianRitmAlarmVolume"]


	# configruations for the alarm
	timePlaying = presets_dt["timePlaying"]

