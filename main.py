import RPi.GPIO as GPIO
import time
import random
import os
from subprocess import call

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
pygame.mixer.music.load("/home/pi/python/Audio/dialtone.mp3")
pygame.mixer.music.set_volume(0.1)

# Call shell command for volume
# call(["amixer sset PCM,1 90% && echo set volume to 90%"], shell=True)


# Function for playing an audio file
def playsound(audio):
    volume = 10
    interupting = False

    if(type(audio) == list):
        for sound in audio:
            sound = "/home/pi/python/Audio/cleaned/" + sound
            pygame.mixer.music.load(sound)
            pygame.mixer.music.set_volume(volume)
            pygame.mixer.music.play()

            while pygame.mixer.music.get_busy() == True:
                if(GPIO.input(26) == 0):
                    interupting = True
                    break

                else:
                    continue

            pygame.mixer.music.stop()

            if interupting == True:
                break

            else:
                continue

    else:
        audio = "/home/pi/python/Audio/cleaned/" + audio
        pygame.mixer.music.load(audio)
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy() == True:
            if(GPIO.input(26) == 0):
                break

            else:
                continue

        pygame.mixer.music.stop()


playsound("welcome.mp3")


# Hangup function
def hangup():
    pygame.mixer.music.load("/home/pi/python/Audio/cleaned/fastbusy.mp3")
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

                if(time.time() - dialStart > 4 and len(dialed) > 0):
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
    print("Dialing... \n")
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
                print("Phone is on hook")
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
        angryOperator(random.randint(1, 10))

    # Detective agency
    elif(num == 3383284 or num == 3383287):
        # call(["amixer sset PCM,0 100% && echo set volume to 100%"], shell=True)
        playsound("detective_agency_intro.mp3")
        # call(["amixer sset PCM,0 90% && echo set volume to 90%"], shell=True)
        DADial = dialSingle()

        # DAB
        if DADial == 1:
            playsound(["DA-B7.mp3", "DA-B8.mp3", "DA-B9.mp3", "DA-B10.mp3",
                        "DA-B11.mp3", "DA-B12.mp3", "DA-B13.mp3", "DA-B14.mp3", "DA-B15.mp3", "DA-B17.mp3", "DA-B18.mp3"])
            tryAgain()

        # DAC
        elif DADial == 2:
            playsound(["DA-C7.mp3", "DA-C8.mp3", "DA-C9.mp3", "DA-C10.mp3",
                        "DA-C11.mp3", "DA-C12.mp3", "DA-C13.mp3", "DA-C14.mp3", "DA-C15.mp3", "DA-C16.mp3", "DA-C17.mp3"])
            tryAgain()

        # DAD
        elif DADial == 3:
            playsound(["DA-D7.mp3", "DA-D8.mp3", "DA-D9.mp3", "DA-D10.mp3",
                        "DA-D11.mp3", "DA-D12.mp3", "DA-D13.mp3", "DA-D14.mp3", "DA-D15.mp3", "DA-D16.mp3", "DA-D17.mp3"])
            tryAgain()

        elif DADial == 0:
            angryOperator(random.randint(1, 10))
        
        else:
            hangup()

    elif(num == 8263772):
        detectiveAgency(1)

    elif(num == 2263766):
        detectiveAgency(2)

    elif(num == 5878423):
        detectiveAgency(3)

    # Random
    elif(num == 2328645):
        randomNumber(1)

    elif(num == 7842433):
        randomNumber(2)

    elif(num == 3378233):
        randomNumber(3)

    elif(num == 5853269):
        randomNumber(4)

    elif(num == 5488367):
        randomNumber(5)

    elif(num == 2267863):
        randomNumber(6)

    elif(num == 7658363):
        randomNumber(7)

    elif(num == 2633968):
        randomNumber(8)

    elif(num == 7826886):
        randomNumber(9)

    elif(num == 7867437):
        randomNumber(10)

    # Angry Operator
    elif(num == 2267846):
        angryOperator(1)

    elif(num == 3424667):
        angryOperator(2)

    elif(num == 2233784):
        angryOperator(3)

    elif(num == 3378769):
        angryOperator(4)

    elif(num == 5665464):
        angryOperator(5)

    elif(num == 7383643):
        angryOperator(6)

    elif(num == 2223787):
        angryOperator(7)

    elif(num == 7328453):
        angryOperator(8)

    elif(num == 2327846):
        angryOperator(9)

    elif(num == 2732843):
        angryOperator(10)

    # Endless Loop
    elif(num == 3444825):
        endlessLoop(1)

    elif(num == 7826476):
        endlessLoop(2)

    elif(num == 6943278):
        endlessLoop(3)

    elif(num == 4687685):
        endlessLoop(4)

    elif(num == 6698463):
        endlessLoop(5)

    elif(num == 3337663):
        endlessLoop(6)

    elif(num == 4466733):
        endlessLoop(7)

    elif(num == 8436296):
        endlessLoop(8)

    elif(num == 2679377):
        endlessLoop(9)

    else:
        tryAgain()


# Detective agency function
def detectiveAgency(DAInput):
    # DAB
    if DAInput == 1:
        playsound(["DA-B7.mp3", "DA-B8.mp3", "DA-B9.mp3", "DA-B10.mp3",
                   "DA-B11.mp3", "DA-B12.mp3", "DA-B13.mp3", "DA-B14.mp3", "DA-B15.mp3", "DA-B17.mp3", "DA-B19.mp3"])
        tryAgain()

    # DAC
    elif DAInput == 2:
        playsound(["DA-C7.mp3", "DA-C8.mp3", "DA-C9.mp3", "DA-C10.mp3",
                   "DA-C11.mp3", "DA-C12.mp3", "DA-C13.mp3", "DA-C14.mp3", "DA-C15.mp3", "DA-C16.mp3", "DA-C17.mp3", "DA-C19.mp3"])
        tryAgain()

    # DAD
    elif DAInput == 3:
        playsound(["DA-D7.mp3", "DA-D8.mp3", "DA-D9.mp3", "DA-D10.mp3",
                   "DA-D11.mp3", "DA-D12.mp3", "DA-D13.mp3", "DA-D14.mp3", "DA-D15.mp3", "DA-D16.mp3", "DA-D17.mp3", "DA-D19.mp3"])
        tryAgain()

    elif DAInput == 0:
            angryOperator(random.randint(1, 10))
        
    else:
        hangup()


def randomNumber(RNInput):
    if(RNInput == 1):
        playsound("Random-B3.mp3")

        RNDial = dialSingle()

        if(RNDial != "cancled"):
            if(RNDial == 0):
                # randomAOB
                RNrand = random.randint(1, 3)
                if(RNrand == 1):
                    playsound("Random-B8.mp3")
                    hangup()

                if(RNrand == 2):
                    playsound("Random-B9.mp3")
                    hangup()

                if(RNrand == 3):
                    playsound("Random-B10.mp3")
                    hangup()

                if(RNrand == 4):
                    print("TODO")
                    hangup()
                    # Play recorded story TODO

            else:
                # Record Story
                print("TODO")
                endlessLoop(random.randint(1, 9))

    else:
        letter = chr(RNInput + 65)

        playsound("Random-" + str(letter) + "3.mp3")
        playsound("Random-" + str(letter) + "4.mp3")
        playsound("Random-" + str(letter) + "5.mp3")

        RNDial = dialSingle()

        if(RNDial != "cancled"):
            if(RNDial == 0):
                # randomAOB
                RNrand = random.randint(1, 3)
                if(RNrand == 1):
                    playsound("Random-" + str(letter) + "8.mp3")
                    hangup()

                if(RNrand == 2):
                    playsound("Random-" + str(letter) + "9.mp3")
                    hangup()

                if(RNrand == 3):
                    playsound("Random-" + str(letter) + "10.mp3")
                    hangup()

                if(RNrand == 4):
                    print("TODO")
                    hangup()
                    # Play recorded story TODO

            else:
                # Record Story
                print("TODO")
                endlessLoop(random.randint(1, 9))


# Operator function
def angryOperator(num):
    playsound("AO-3-repeat-connection.mp3")

    if(num == 1):
        # play audio
        playsound(["AO-B4-Part1.mp3", "AO-B4-Part2.mp3",
                   "AO-B4-Part3.mp3", "AO-B4-Part4.mp3"])

        # get input
        AOInput = dialSingle()

        if(AOInput != "cancled"):
            if(AOInput == 0):
                # randomAOB
                rand = random.randint(1, 3)
                print(rand)
                if(rand == 1):
                    playsound("AO-B6.mp3")
                    hangup()

                if(rand == 2):
                    playsound("AO-B7.mp3")
                    hangup()

                if(rand == 3):
                    playsound("AO-B8.mp3")
                    hangup()

                if(rand == 4):
                    print("TODO")
                    hangup()
                    # Play recorded story TODO

            else:
                # Record Story
                print("TODO")
                endlessLoop(random.randint(1, 9))

    else:
        letter = chr(num + 65)

        playsound("AO-" + str(letter) + "4.mp3")

        # get input
        AOInput = dialSingle()

        if(AOInput != "cancled"):
            if(AOInput == 0):
                # randomAOB
                rand = random.randint(1, 3)
                print(rand)
                if(rand == 1):
                    playsound("AO-" + str(letter) + "6.mp3")
                    hangup()

                if(rand == 2):
                    playsound("AO-" + str(letter) + "7.mp3")
                    hangup()

                if(rand == 3):
                    playsound("AO-" + str(letter) + "8.mp3")
                    hangup()

                if(rand == 4):
                    print("TODO")
                    hangup()
                    # Play recorded story TODO

            else:
                # Record Story
                print("TODO")
                endlessLoop(random.randint(1, 9))


# endless loop function
def endlessLoop(ELInput):
    playsound("modemclip.mp3")
    if(ELInput == 1):
        playsound("el_b3.mp3")
        playsound("el_b4.mp3")
        playsound("el_b5.mp3")
        playsound("el_b6.mp3")
        playsound("el_b7.mp3")
        playsound("el_b8.mp3")
        playsound("el_b9.mp3")
        playsound("el_b10.mp3")
        hangup()

    if(ELInput == 2):
        playsound("el_c3.mp3")
        playsound("el_c4.mp3")
        playsound("el_c5.mp3")
        playsound("el_c6.mp3")
        playsound("el_c7.mp3")
        playsound("el_c8.mp3")
        playsound("el_c9.mp3")
        playsound("el_c10.mp3")
        hangup()

    if(ELInput == 3):
        playsound("el_d3.mp3")
        playsound("el_d4.mp3")
        playsound("el_d5.mp3")
        playsound("el_d6.mp3")
        playsound("el_d7.mp3")
        playsound("el_d8.mp3")
        playsound("el_d9.mp3")
        playsound("el_d10.mp3")
        hangup()

    if(ELInput == 4):
        playsound("el_e3.mp3")
        playsound("el_e4.mp3")
        playsound("el_e5.mp3")
        playsound("el_e6.mp3")
        playsound("el_e7.mp3")
        playsound("el_e8.mp3")
        playsound("el_e9.mp3")
        playsound("el_e10.mp3")
        hangup()

    if(ELInput == 5):
        playsound("el_f3.mp3")
        playsound("el_f4.mp3")
        playsound("el_f5.mp3")
        playsound("el_f6.mp3")
        playsound("el_f7.mp3")
        playsound("el_f8.mp3")
        playsound("el_f9.mp3")
        playsound("el_f10.mp3")
        hangup()

    if(ELInput == 6):
        playsound("el_g3.mp3")
        playsound("el_g4.mp3")
        playsound("el_g5.mp3")
        playsound("el_g6.mp3")
        playsound("el_g7.mp3")
        playsound("el_g8.mp3")
        playsound("el_g9.mp3")
        playsound("el_g10.mp3")
        hangup()

    if(ELInput == 7):
        playsound("el_h3.mp3")
        playsound("el_h4.mp3")
        playsound("el_h5.mp3")
        playsound("el_h6.mp3")
        playsound("el_h7.mp3")
        playsound("el_h8.mp3")
        playsound("el_h9.mp3")
        playsound("el_h10.mp3")
        hangup()

    if(ELInput == 8):
        playsound("el_i3.mp3")
        playsound("el_i4.mp3")
        playsound("el_i5.mp3")
        playsound("el_i6.mp3")
        playsound("el_i7.mp3")
        playsound("el_i8.mp3")
        playsound("el_i9.mp3")
        playsound("el_i10.mp3")
        hangup()

    if(ELInput == 9):
        playsound("el_j3.mp3")
        playsound("el_j4.mp3")
        playsound("el_j5.mp3")
        playsound("el_j6.mp3")
        playsound("el_j7.mp3")
        playsound("el_j8.mp3")
        playsound("el_j9.mp3")
        playsound("el_j10.mp3")
        hangup()


def tryAgain():
    playsound("notcomplete.mp3")
    hangup()


##################
# Main game loop #
##################
print("Welcome to Cold Calling")
while True:
    try:
        if(GPIO.input(26) == 1):
            pygame.mixer.music.load("/home/pi/python/Audio/dialtone.mp3")
            pygame.mixer.music.play(-1, 0.0)
            pygame.mixer.music.set_volume(0.1)
            dial()
            pygame.mixer.music.stop()

    except KeyboardInterrupt:
        break
