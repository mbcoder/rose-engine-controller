
# Test module for moving rose engine steppers
# git commit -am "commit message"

import csv
from RPi import GPIO
import time
import threading
from guizero import App, Text, TextBox, PushButton, Window, yesno, ButtonGroup, Combo

# setup GPIO for inputs
clk = 17
dt = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(clk, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(dt, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Pin Definitons:
s1_enablePin = 2
s1_directionPin = 3
s1_pulsePin = 4

s2_enablePin = 10
s2_directionPin = 9
s2_pulsePin = 11

# setup gpio for steppers
GPIO.setwarnings(False)
GPIO.setup(s1_enablePin, GPIO.OUT)
GPIO.setup(s1_directionPin, GPIO.OUT)
GPIO.setup(s1_pulsePin, GPIO.OUT)

GPIO.setup(s2_enablePin, GPIO.OUT)
GPIO.setup(s2_directionPin, GPIO.OUT)
GPIO.setup(s2_pulsePin, GPIO.OUT)

counter = 0
clkLastState = GPIO.input(clk)
stopFlag = False
delay = 0.1
operating = False
forward = True

patternPosition = 0

# setup rotary stepper
GPIO.output(s1_enablePin, GPIO.HIGH)
GPIO.output(s1_directionPin, GPIO.LOW)

# setup linear stepper
GPIO.output(s2_enablePin, GPIO.HIGH)
GPIO.output(s2_directionPin, GPIO.LOW)
s2_lastDir = GPIO.LOW

# pulse stepper by n pulses (ROTARY)
def s1_moveStepper(pulses):
    global delay

    if pulses > 0:
        GPIO.output(s1_directionPin, GPIO.HIGH)
    if pulses < 0:
        GPIO.output(s1_directionPin, GPIO.LOW)

    #delay = 0.001
    for x in range(abs(pulses)):
        GPIO.output(s1_pulsePin, GPIO.HIGH)
        time.sleep(delay)
        GPIO.output(s1_pulsePin, GPIO.LOW)
        time.sleep(delay)

# pulse stepper by n pulses (LINEAR)
def s2_moveStepper(pulses):
    global delay
    global s2_lastDir

    if pulses > 0:
        GPIO.output(s2_directionPin, GPIO.HIGH)
        if s2_lastDir == GPIO.LOW:
            #print("Dir change to HI")
            s2_lastDir = GPIO.HIGH
            time.sleep(0.05)
    if pulses < 0:
        GPIO.output(s2_directionPin, GPIO.LOW)
        if s2_lastDir == GPIO.HIGH:
            #print("Dir change to LOW")
            s2_lastDir = GPIO.LOW
            time.sleep(0.05)

    for x in range(abs(pulses)):
        GPIO.output(s2_pulsePin, GPIO.HIGH)
        time.sleep(delay)
        GPIO.output(s2_pulsePin, GPIO.LOW)
        time.sleep(delay)

def handleListener():
    global clkLastState
    global counter
    print("handle listener thread starting")
    try:
        while True:
            clkState = GPIO.input(clk)
            dtState = GPIO.input(dt)
            if clkState != clkLastState:
                if dtState != clkState:
                    counter += 1
                else:
                    counter -= 1

            #print(counter)
            clkLastState = clkState
            time.sleep(0.00005)

            if stopFlag == True:
                return
    finally:
        GPIO.cleanup()


def calcDelay():
    global delay
    global counter
    global operating
    global forward

    #calculate factor
    if counter >=10 or counter <=-10:
        factor = abs(counter) - 10
        #print("factor:",factor)
        if factor > 16:
            factor = 16

        delay = 0.01 - (0.0005 * factor)

    #stopped zone
    if counter < 10 and counter >-10:
        operating = False

    #forward zone
    if counter >= 10:
        operating = True
        forward = True

    #backward zone
    if counter <=-10:
        operating = True
        forward = False

class OpMode:
    def __init__(self):
        pass

    STOPPED = 1
    SETUP_POS = 2
    SETUP_ADV = 3
    ENGRAVING = 4


class Motion:
    def __init__(self):
        pass

    LINEAR = 1
    ROTARY = 2


currentMode = OpMode.STOPPED
setupMode = Motion.LINEAR
advanceMode = Motion.LINEAR


def changeOpMode(selected_value):
    global currentMode

    if selected_value == "Stopped":
        currentMode = OpMode.STOPPED
        print("--mode ", currentMode)
    elif selected_value == "Setup position":
        currentMode = OpMode.SETUP_POS
        print("--mode ", currentMode)

    elif selected_value == "Setup advance":
        currentMode = OpMode.SETUP_ADV
        print("--mode ", currentMode)

    elif selected_value == "Engraving":
        currentMode = OpMode.ENGRAVING
        print("--mode ", currentMode)


def changeSetupMode(selected_value):
    global setupMode

    if selected_value == "Linear":
        setupMode = Motion.LINEAR
    else:
        setupMode = Motion.ROTARY


def changeAdvanceMode(selected_value):
    global advanceMode

    if selected_value == "Linear":
        advanceMode = Motion.LINEAR
    else:
        advanceMode = Motion.ROTARY


def resetRotaryScale():
    print("resetting rotary")


def resetLinearScale():
    print("resetting linear")


def advanceForward():
    global currentMode

    print("advance forward")
    print("mode ", currentMode)


def advanceBackward():
    print("advance backward")


offsets = []

with open('Pattern1.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        offsets.append(int(row[1]))

currentOffset = offsets[0]

# start thread for handle listener
if __name__ == "__main__":
    print("main thread")

    handleThread = threading.Thread(target=handleListener)
    handleThread.start()


# test steps
delay = 0.001
#s1_moveStepper(-1000)
#sleep(2)
s2_moveStepper(50)
#s2_moveStepper(100)
#s2_moveStepper(-50)

#for n in range(11):
#print(n)
#s2_moveStepper(50)
#s2_moveStepper(50)
#s2_moveStepper(-50)
#s2_moveStepper(-50)


# setup UI
app = App(title="Rose Engine", width=700, height=300, layout="grid")

labelOpMode = Text(app, size=16, text="Operating Mode:", align="left", grid=[0, 0])
operatingMode = Combo(app, options=["Stopped", "Setup position", "Setup advance", "Engraving"], selected="Stopped",
                      grid=[0, 1], width=12, command=changeOpMode)

labelSetupMode = Text(app, size=16, text="Setup position", align="left", width=20, grid=[1, 0])
setupPositionMode = Combo(app, options=["Linear", "Rotary"], selected="Linear", grid=[1, 1], command=changeSetupMode)

labelRotary = Text(app, size=16, text="Rotary:", grid=[2, 0])
textRotary = Text(app, size=16, text="0.00", width=10, grid=[3, 0])

labelLinear = Text(app, size=16, text="Linear:", grid=[2, 1])
textLinear = Text(app, size=16, text="0.00", width=10, grid=[3, 1])

resetRotaryButton = PushButton(app, command=resetRotaryScale, text="Reset", grid=[4, 0])
resetLinearButton = PushButton(app, command=resetLinearScale, text="Reset", grid=[4, 1])

# Advance controls
labelSdvanceMode = Text(app, size=16, text="Setup advance", align="left", width=20, grid=[1, 3])
setupAdvanceMode = Combo(app, options=["Linear", "Rotary"], selected="Linear", grid=[1, 4], command=changeAdvanceMode)

labelAdvanceLinear = Text(app, size=16, text="Linear advance:", grid=[2, 3])
textAdvanceLinear = Text(app, size=16, text="2mm", grid=[3, 3])
labelAdvanceRotary = Text(app, size=16, text="Rotary advance", grid=[2, 4])
textAdvanceRotary = Text(app, size=16, text="5degrees", grid=[3, 4])

advanceForwardButton = PushButton(app, command=advanceForward, text="Forward", grid=[0, 5])
advanceBackwardButton = PushButton(app, command=advanceBackward, text="Back", grid=[1, 5])

app.display()




currentPosition = 0

if currentPosition == 1:
    while True:
        calcDelay()
        if operating == True:
            #print(delay)
            if forward == True:
                patternPosition = patternPosition + 1

                if patternPosition >= 8000:
                    patternPosition = 0

                s1_moveStepper(1)
            else:
                patternPosition = patternPosition -1
                if patternPosition <0:
                    patternPosition = 7999
                s1_moveStepper(-1)

        steps = offsets[patternPosition] - currentPosition

        s2_moveStepper(steps)

        #print("position: ", patternPosition, " offset ", offsets[patternPosition], " steps ", steps)

        currentPosition = offsets[patternPosition]


        #time.sleep(0.5)


exitFlag = True
