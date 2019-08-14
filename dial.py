import RPi.GPIO as GPIO
import math
import sys
import os
import subprocess
import socket
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.add_event_detect(18, GPIO.BOTH)

start = 0
last = 0
count = 0
waiting = False
times = []

while True:
    try:
	print(GPIO.input(26))
        # Initial pulse detection
        if GPIO.event_detected(18):
            if(GPIO.input(18) == 1):
                start = time.time()
                count += 1
                last = 1
                waiting = True
                print("Pulse!")

                # Start counting pulses
                while True:

                    if(GPIO.event_detected(18)):
                        print(GPIO.input(18))
                        if(GPIO.input(18) == 1 and last == 0):
                            last == 1

                        if(GPIO.input(18) == 0 and last == 1):
                            print("Pulse!")
                            count += 1
                            # times.append(time.time() - start)
                            start = time.time()
                            last == 0

                    # If time since last pulse is greater than 0.07 break loop
                    # if(round(time.time()) % 2 == 0):
                    #     print(time.time() - start)
                    if(time.time() - start > 0.7):
                        waiting = False
                        break

                    else:
                        continue

                print("you dialed: " + str(count - 1) + "\n")
                # print(times)
                count = 0

    except KeyboardInterrupt:
        break
