from __future__ import division  # so that 1/3=0.333 instead of 1/3=0
from psychopy import visual, core, event, clock
from psychopy.hardware import keyboard
from psychopy import visual, core, data, event, logging, sound, gui
from psychopy.constants import *  # things like STARTED, FINISHED
import numpy  # whole numpy lib is available, prepend 'np.'
from numpy import sin, cos, tan, log, log10, pi, average, sqrt, std, deg2rad, rad2deg, linspace, asarray
from numpy.random import random, randint, normal, shuffle
import os  # handy system and path functions
from random import choice, randrange, shuffle, uniform
from psychopy.tools.coordinatetools import pol2cart, cart2pol
import time
import random as rnd
from psychopy.tools.filetools import fromFile, toFile


#-------Constants-------
FIXATION_WAIT_TIME = 1
NUM_LANDMARKS = 7
N_TRIALS = 5
MAX_LANDMARK_SIZE = 5

# experiment details
refRate = 60  # 1 second
nTrials = 15

# stimulus duration
#stimDur = refRate
stimDur = 10

# important parameters
#dot density = 2.6 dot per degree square

dotsN = 94
fieldSize = 6  # 3x3 square dot field
elemSize = 0.125

dotsTheta = numpy.random.rand(dotsN) * 360  # array with shape (500,)
dotsRadius = numpy.random.rand(dotsN) * fieldSize

randDotsX = numpy.random.uniform(low=-fieldSize, high=fieldSize,size=(dotsN,))
randDotsY = numpy.random.uniform(low=-fieldSize, high=fieldSize,size=(dotsN,))

condList = ['radialIn','radialOut']

pointsArray = []
# --- Setup the Window ---
win = visual.Window([720,720],monitor="testMonitor", units="deg" , color="black")
    
# initializing experiment stimuli
rotDots = visual.ElementArrayStim(win, nElements=dotsN, sizes=elemSize, elementTex=None,
    colors=(1.0, 1.0, 1.0), xys=random([dotsN, 2]),
    colorSpace='rgb', elementMask='circle', texRes=128, fieldPos=(-4,4), fieldSize=fieldSize, fieldShape='circle', )

fixation = visual.GratingStim(win, size=0.2, pos=[0,0], sf=0,color = 'red')
feedBack = visual.GratingStim(win, size=2, units='norm', pos=[0,0], sf=0,color = 'green')

welcomeText = visual.TextStim(win=win, name='welcomeText',
    text='Welcome to the experiment.',
    font='Open Sans',
    pos=(0, 0), height=1, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-1.0);
    
blank500ms = visual.TextStim(win=win,text='')

welcomeText.draw()
win.flip()

key_welcome = keyboard.Keyboard()
event.waitKeys(keyList=['space'])
win.flip()

fixation.draw()
win.flip()
clock.wait(FIXATION_WAIT_TIME)
win.flip()

landmark_value = 0
landmark = visual.TextStim(win=win, name='landmark',
    text=landmark_value,
    font='Open Sans',
    pos=(0, 0), height=0, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-1.0)

key_resp = keyboard.Keyboard()

# --- Initialize components for Routine "blank500" ---
image = visual.ImageStim(
    win=win,
    name='image', 
    image=None, mask=None,
    ori=0.0, pos=(0, 0), size=(0.5, 0.5),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=0.0)

# --- Initialize components for Routine "goodbye_screen" ---
goodBye = visual.TextStim(win=win, name='goodBye',
    text='Have a great day',
    font='Open Sans',
    pos=(0, 0), height=1, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);



# Add feedback, logging 
for trial in range(1,N_TRIALS):  #number of trials N_TRIALS
    trial +=1
    print("Starting trial ",trial)
    condType = choice(condList)
    x = numpy.random.randint(1,6)
    speed = x / 40
    print('Current Speed: ',x, speed)

    moveSign = 1  if condType == 'radialOut' else -1     
    landmark_values = [i for i in range(1,8)]
    initial_height = 0 if condType == 'radialOut' else MAX_LANDMARK_SIZE
    landmark.height = initial_height
    landmark_value = rnd.choice(landmark_values)
    landmark_values.pop(landmark_values.index(landmark_value))
    target = rnd.choice(landmark_values)
    
    landmark.autoDraw = False
    landmark.autoLog = False
    keyPressed = False
    
    
    startText = visual.TextStim(win=win, name='startValue',
    text='Start: ' + str(landmark_value) + '\n' + 'Target: ' + str(target),
    font='Open Sans',
    pos=(0, 6), height=2, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-1.0);


    startText.draw()
    win.flip()
    clock.wait(1)

    print("target is ",target)
    hold=False
    timer = core.Clock()
    height = landmark.height
    while True: #single trial loop

        keys = event.getKeys(keyList=['space'])        
        dieScoreArray = numpy.random.rand(dotsN)  # generating array of float numbers
        deathDots = (dieScoreArray < 0.01)
        
        if condType == 'radialIn':
            dotsRadius = (dotsRadius + speed * moveSign)
            transMove = False
            outFieldRadius = (dotsRadius <= 0.03)
            dotsRadius[outFieldRadius] = numpy.random.rand(sum(outFieldRadius)) * fieldSize
            dotsRadius[deathDots] = numpy.random.rand(sum(deathDots)) * fieldSize
            thetaX, radiusY = pol2cart(dotsTheta, dotsRadius)
            rotDots.setXYs(numpy.array([thetaX, radiusY]).transpose())
            
        elif condType == 'radialOut':
            dotsRadius = (dotsRadius + speed * moveSign)
            transMove = False
            outFieldRadius = (dotsRadius >= fieldSize)
            dotsRadius[outFieldRadius] = numpy.random.rand(sum(outFieldRadius))
            dotsRadius[deathDots] = numpy.random.rand(sum(deathDots))
            thetaX, radiusY = pol2cart(dotsTheta, dotsRadius)
            rotDots.setXYs(numpy.array([thetaX, radiusY]).transpose())            

#        if landmark.height <= MAX_LANDMARK_SIZE:
        if  int(height) >= MAX_LANDMARK_SIZE or height <= 0:
#            print("Max height reached after increasing")
            if timer.getTime()>2:   # after 2 sec stop showing landmark             
#                print("2 sec limit")
                
                landmark.text = '' 
                landmark.height = 0      
                height = initial_height +(0.05 * moveSign)
#                print(height)
                timer.reset()
                hold=False
            else:   # show landmark
#                print("show landmark")
                landmark.text= landmark_value
                landmark.height = MAX_LANDMARK_SIZE
                hold=True
        else:
#            print("increase height")
            height += moveSign * speed            
            if int(height) >= MAX_LANDMARK_SIZE or height <= 0: # change landmark value only when the size exceeds limits
#                    print("Max height reached while increasing")
                    if not hold:
#                        print("increase value")
                        landmark_value = landmark_value + moveSign
                        if landmark_value == 8:
                            landmark_value = 1
                        elif landmark_value == 0:
                            landmark_value = 7
        landmark.draw()
                
        if keys:
            keyPressed = True
            if landmark_value==target:
                win.flip()
                feedBack.color = 'green'
                feedBack.draw()
                win.flip()
                pointsArray.append(1)
            else:
                win.flip()
                feedBack.color = 'red'
                feedBack.draw()
                win.flip()
                pointsArray.append(0)
            keys = []
            break
                      
        rotDots.draw()
        fixation.draw()
        win.flip()
        
        
        if keyPressed:
            break
        
    clock.wait(0.5)
        
        
with open('pointsLog.txt','w') as f:
    for el in pointsArray:
        f.write(str(el))
    

win.flip()
goodBye.draw()
win.flip()
event.waitKeys()
win.close()
