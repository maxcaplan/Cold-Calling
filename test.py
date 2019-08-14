# import RPi.GPIO as GPIO
# import math
# import sys
# import os
# import subprocess
# import socket
# import time

# GPIO.setwarnings(False)
# GPIO.setmode(GPIO.BCM)
# GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)


# GPIO.add_event_detect(18, GPIO.BOTH)

# while True:
#     try:
#         if GPIO.event_detected(18):
#             if(GPIO.input(18)):
#                 print(1)

#     except KeyboardInterrupt:
#         break

import pygame

pygame.mixer.init()
pygame.mixer.music.load("dial.mp3")
pygame.mixer.music.set_volume(10)
pygame.mixer.music.play()
while pygame.mixer.music.get_busy() == True:
    continue

print("done")