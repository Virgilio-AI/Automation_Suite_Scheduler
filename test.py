
# Fecha: 14/November/2021 - Sunday
# Autor: Virgilio Murillo Ochoa
# personal github: Virgilio-AI
# linkedin: https://www.linkedin.com/in/virgilio-murillo-ochoa-b29b59203
# contact: virgiliomurilloochoa1@gmail.com
import os
import json

HolaMundo=""
def init():
	with open("presets.json","r") as f:
		dtGlobalValues = json.load(f)

	HolaMundo = dtGlobalValues["hola_mundo"]
	print(HolaMundo)

init()
