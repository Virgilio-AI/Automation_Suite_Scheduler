#!/usr/bin/zsh
###############################
# Author: Virgilio Murillo Ochoa
# Date: 11/February/2022 - Friday
# personal github: Virgilio-AI
# linkedin: https://www.linkedin.com/in/virgilio-murillo-ochoa-b29b59203
# contact: virgiliomurilloochoa1@gmail.com
# #########################################

file=venv
if [[ ! -d $file ]]
then
	python -m venv venv/
	pip install $(cat dependencies.txt)
fi

source venv/bin/activate
python main.py
deactivate
