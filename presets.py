
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
# ==== recording zoom clases =====
# =============
zoomClassRecorderActive=True
zoomClassOpener=True


# =============
# ==== recording configurations =====
# =============
zoomClasesDirectory='/home/rockhight/Videos/clasesGrabadas/semestre5'

