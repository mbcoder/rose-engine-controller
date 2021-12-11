
# Test module for moving rose engine steppers
# git commit -am "commit message"

import csv
from RPi import GPIO
import time
import threading

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
#GPIO.output(s1_directionPin, GPIO.LOW)

# setup linear stepper
GPIO.output(s2_enablePin, GPIO.HIGH)

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
  
  if pulses > 0:
      GPIO.output(s2_directionPin, GPIO.HIGH)
  if pulses < 0:
      GPIO.output(s2_directionPin, GPIO.LOW)
  
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
    if factor > 19:
      factor = 19

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


print('start of loop')

#for offset in offsets:
#    steps = offset - currentOffset  # type: int

#    currentOffset = offset

#    s1_moveStepper(1)
#    s2_moveStepper(steps)

    #print('steps {0} offset {1}'.format(steps, offset))

print('end of loop')

# test steps
#s2_moveStepper(-50)
#s2_moveStepper(50)
#s2_moveStepper(-50)

currentPosition = 0

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
