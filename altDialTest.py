import RPi.GPIO as GPIO
import time
import random

# Install with "pip install pygame"
import pygame

# Setup GPIO pins for input and event detection
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(18, GPIO.BOTH)

# Load audio
pygame.mixer.init()
pygame.mixer.music.load("./Audio/dialtone.mp3")
pygame.mixer.music.set_volume(10)


# Function for playing an audio file
def playsound(audio):
    pygame.mixer.music.load(audio)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue


# Hangup function
def hangup():
    pygame.mixer.music.load("./Audio/fastbusy.mp3")
    pygame.mixer.music.play(-1, 0.0)
    while(GPIO.input(26) == 1):
        time.sleep(0.1)
    pygame.mixer.music.stop()


# function for dialing phone number
def dial():
    count = 0
    dialStart = 0
    start = time.time()
    dialed = []
    cancled = False
    dialing = True
    inNum = None
    print("dialing")

    while dialing == True:
        try:
            # Check if phone is off hook
            if(GPIO.input(26) == 1):
                if(GPIO.event_detected(18)):
                    if(GPIO.input(18) == 1 and time.time() - start > 0.08):
                        pygame.mixer.music.stop()
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
                    pygame.mixer.music.play(-1, 0.0)

                if(time.time() - dialStart > 3 and len(dialed) > 0):
                    dialing = False
                    # Converting integer list to string list
                    s = [str(i) for i in dialed]
                    # Join list items using join()
                    inNum = int("".join(s))
                    break

            else:
                dialing = False
                cancled = True
                break

        except KeyboardInterrupt:
            dialing = False
            break

    if(cancled):
        return
    else:
        pygame.mixer.music.stop()
        print("Calling number: " + str(inNum) + "\n")
        checkNumber(inNum)


# function for dialing single number
def dialSingle():
    count = 0
    start = time.time()
    dialed = None
    cancled = False
    dialing = True

    while dialing == True:
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
                    dialed = count
                    dialStart = time.time()
                    count = 0

                if(dialed != None):
                    dialing = False
                    break

            else:
                dialing = False
                cancled = True
                break

        except KeyboardInterrupt:
            dialing = False
            break

    if(cancled):
        return "cancled"
    else:
        return dialed


def checkNumber(num):
    if(num == 411):
        playsound("./Audio/AO-3-repeat-connection.mp3")
        rand = random.randint(1, 2)
        angryOperator(rand)
    else:
        playsound("./Audio/notcomplete.mp3")
        hangup()

# Operator function


def angryOperator(num):
    if(num == 1):
        # play audio
        playsound("./Audio/AO-B4-Part1.mp3")
        playsound("./Audio/AO-B4-Part2.mp3")
        playsound("./Audio/AO-B4-Part3.mp3")
        playsound("./Audio/AO-B4-Part4.mp3")

        # get input
        AOInput = dialSingle()

        if(AOInput != "cancled"):
            if(AOInput == 0):
                # randomAOB
                rand = random.randint(1, 3)
                print(rand)
                if(rand == 1):
                    playsound("./Audio/AO-B6.mp3")
                    hangup()

                if(rand == 2):
                    playsound("./Audio/AO-B7.mp3")
                    hangup()

                if(rand == 3):
                    playsound("./Audio/AO-B8.mp3")
                    hangup()

                if(rand == 4):
                    print("TODO")
                    hangup()
                    # Play recorded story TODO

            else:
                # Record Story
                print("TODO")
                endlessLoop()

    if(num == 2):
        # play audio
        playsound("./Audio/AO-C4.mp3")

        # get input
        AOInput = dialSingle()

        if(AOInput != "cancled"):
            if(AOInput == 0):
                # randomAOC
                rand = random.randint(1, 3)
                print(rand)
                if(rand == 1):
                    playsound("./Audio/AO-C6.mp3")
                    hangup()

                if(rand == 2):
                    playsound("./Audio/AO-C7.mp3")
                    hangup()

                if(rand == 3):
                    playsound("./Audio/AO-C8.mp3")
                    hangup()

                if(rand == 4):
                    print("TODO")
                    hangup()
                    # Play recorded story TODO

            else:
                # Record story
                print("TODO")
                endlessLoop()


# endless loop function
def endlessLoop():
    rand = random.randint(1, 9)
    if(rand == 1):
        playsound("./Audio/el_b3.mp3")
        playsound("./Audio/el_b4.mp3")
        playsound("./Audio/el_b5.mp3")
        playsound("./Audio/el_b6.mp3")
        playsound("./Audio/el_b7.mp3")
        playsound("./Audio/el_b8.mp3")
        playsound("./Audio/el_b9.mp3")
        playsound("./Audio/el_b10.mp3")
        hangup()

    if(rand == 2):
        playsound("./Audio/el_c3.mp3")
        playsound("./Audio/el_c4.mp3")
        playsound("./Audio/el_c5.mp3")
        playsound("./Audio/el_c6.mp3")
        playsound("./Audio/el_c7.mp3")
        playsound("./Audio/el_c8.mp3")
        playsound("./Audio/el_c9.mp3")
        playsound("./Audio/el_c10.mp3")
        hangup()

    if(rand == 3):
        playsound("./Audio/el_d3.mp3")
        playsound("./Audio/el_d4.mp3")
        playsound("./Audio/el_d5.mp3")
        playsound("./Audio/el_d6.mp3")
        playsound("./Audio/el_d7.mp3")
        playsound("./Audio/el_d8.mp3")
        playsound("./Audio/el_d9.mp3")
        playsound("./Audio/el_d10.mp3")
        hangup()

    if(rand == 4):
        playsound("./Audio/el_e3.mp3")
        playsound("./Audio/el_e4.mp3")
        playsound("./Audio/el_e5.mp3")
        playsound("./Audio/el_e6.mp3")
        playsound("./Audio/el_e7.mp3")
        playsound("./Audio/el_e8.mp3")
        playsound("./Audio/el_e9.mp3")
        playsound("./Audio/el_e10.mp3")
        hangup()

    if(rand == 5):
        playsound("./Audio/el_f3.mp3")
        playsound("./Audio/el_f4.mp3")
        playsound("./Audio/el_f5.mp3")
        playsound("./Audio/el_f6.mp3")
        playsound("./Audio/el_f7.mp3")
        playsound("./Audio/el_f8.mp3")
        playsound("./Audio/el_f9.mp3")
        playsound("./Audio/el_f10.mp3")
        hangup()

    if(rand == 6):
        playsound("./Audio/el_g3.mp3")
        playsound("./Audio/el_g4.mp3")
        playsound("./Audio/el_g5.mp3")
        playsound("./Audio/el_g6.mp3")
        playsound("./Audio/el_g7.mp3")
        playsound("./Audio/el_g8.mp3")
        playsound("./Audio/el_g9.mp3")
        playsound("./Audio/el_g10.mp3")
        hangup()

    if(rand == 7):
        playsound("./Audio/el_h3.mp3")
        playsound("./Audio/el_h4.mp3")
        playsound("./Audio/el_h5.mp3")
        playsound("./Audio/el_h6.mp3")
        playsound("./Audio/el_h7.mp3")
        playsound("./Audio/el_h8.mp3")
        playsound("./Audio/el_h9.mp3")
        playsound("./Audio/el_h10.mp3")
        hangup()

    if(rand == 8):
        playsound("./Audio/el_i3.mp3")
        playsound("./Audio/el_i4.mp3")
        playsound("./Audio/el_i5.mp3")
        playsound("./Audio/el_i6.mp3")
        playsound("./Audio/el_i7.mp3")
        playsound("./Audio/el_i8.mp3")
        playsound("./Audio/el_i9.mp3")
        playsound("./Audio/el_i10.mp3")
        hangup()

    if(rand == 9):
        playsound("./Audio/el_j3.mp3")
        playsound("./Audio/el_j4.mp3")
        playsound("./Audio/el_j5.mp3")
        playsound("./Audio/el_j6.mp3")
        playsound("./Audio/el_j7.mp3")
        playsound("./Audio/el_j8.mp3")
        playsound("./Audio/el_j9.mp3")
        playsound("./Audio/el_j10.mp3")
        hangup()


##################
# Main game loop #
##################
while True:
    try:
        if(GPIO.input(26) == 1):
            pygame.mixer.music.load("./Audio/dialtone.mp3")
            pygame.mixer.music.play(-1, 0.0)
            dial()
            pygame.mixer.music.stop()

    except KeyboardInterrupt:
        break
