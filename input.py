import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.add_event_detect(18, GPIO.BOTH)

last = 0
count = 0
dialStart = 0
start = time.time()
dialed = []


while True:
    try:
        # Check if phone is off hook
        if(GPIO.input(26) == 1):
            if(GPIO.event_detected(18)):
                if(GPIO.input(18) == 1 and time.time() - start > 0.08):
                    count += 1
                    start = time.time()
                    last = 1

            if(time.time() - start > 0.6 and count > 0):
                if(count > 9):
                    count = 0
                print("You dialed: " + str(count) + "\n")
                dialed.append(count)
                dialStart = time.time()
                count = 0

            if(time.time() - dialStart > 4 and len(dialed) > 0):
                print("Calling number:")
                print(dialed)
                print("-----------------\n")
                dialed = []

    except KeyboardInterrupt:
        break
