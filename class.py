#!/usr/bin/python3 -u

## main algorithm of classification part of project SEAI-SEPCAP


#imports
from aux_functions import nothing
from calibration import calibration_image
from alter import alter
from colorDetection import colorDetector 
from picamera.array import PiRGBArray
from picamera import PiCamera
from sms import SepcapMessagingSystem as SMS
import sys
import time          
import cv2 as cv
import numpy as np


## type of capsules
## 1 - yellow
## 2 - red
## 3 - white
## 4 - nude
## 5 - red and white
## 6 - dark green and white
## 7 - dark green and nude 
## 8 - blue and white
## 9 - dark green and light green

def capsule_type(colors):
    
    
    if len(colors) == 1:
        color = colors[0]
        if color == 'yellow':
            return 1
        if color == 'red':
            return 2
        if color == 'white':
            return 3
        if color == 'nude':
            return 4
    
    elif len(colors) == 2:
        
        if ("red" in colors) and ("white" in colors):
            return 5
        if ("dark green" in colors) and ("white" in colors):
            return 6
        if ("dark green" in colors) and ("nude" in colors):
            return 7
        if ("blue" in colors) and ("white" in colors):
            return 8
        if ("dark green" in colors) and ("light green" in colors):
            return 9
    else: return 0
        
        
        

#assistant function for detecting RGB variables
def click(event, x, y, flags, param):
    if event == cv.EVENT_LBUTTONDOWN:
         print(image[y,x])
         print("X:", x ,"Y:", y)



#initial boundaries
boundaries = [
    ([5,0,110],[60,40,170], 'red'), 
    ([90,20,0],[170,60,15], 'blue'), 
    ([65,110,185],[75,120,195], 'orange'),
    ([15,145,160],[25,155,182], 'yellow'),
    ([95,165,205],[105,175,215], 'nude'),
    ([5,10,0],[60,60,10], 'dark green'),
    ([135,135,105],[145,145,115], 'light green'),
    ([200,190,200],[230,230,230], 'white')
    ]

#calibration mode
calib = 0
var_alter = 0


#starting variables
flag = 0
old_flag = 1
capsule_count = 0

#adjustable variables
speed = 0           #change value of speed if required
min_area = 27000    #change minimal area for each video and distance
blur = 9            #change value for blur
crop_p = 0.8       #proportion of crop


# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 45
rawCapture = PiRGBArray(camera, size=(640, 480))
# allow the camera to warmup
time.sleep(0.1)


#comm initialize
sms = SMS(open(sys.argv[1], "rb"), open(sys.argv[2], "wb"))


#while loop for video capturing
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	# grab the raw NumPy array representing the image, then initialize the timestamp
	# and occupied/unoccupied text
    image = frame.array
    
    image = image[0:480,400:560]
    
    image = cv.medianBlur(image, blur)
   

    if var_alter == 1:
        boundaries = alter(boundaries, "red", [20,20,110])
        var_alter = 0

    #detect colors
    colors, rect = colorDetector(image, min_area= min_area, proportion= crop_p, boundaries = boundaries)

    #rising and falling edge
    if (len(rect) == 1 and flag == 0) and old_flag == 1 and colors != []:
        
        old_flag = flag
        flag = 1
        print("Capsule detected: ", colors)
        ##send comm
        sms.sendPacket(
            SMS.Address.Broadcast, 
            SMS.Message.NewCapsule.type, 
            capsule_type(colors))
            
        if calib == 1:
            calibration_image(frame, colors)
            calib = 0
        capsule_count = capsule_count + 1

    elif (len(rect) == 0 and flag == 1) and old_flag == 0:
        old_flag = flag
        flag = 0
        print("Capsule not in frame")

    
    cv.imshow("frame", image)
    cv.setMouseCallback("frame", click)

    key = cv.waitKey(1) & 0xFF
	# clear the stream in preparation for the next frame
    rawCapture.truncate(0)
	# if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break

print("Total Capsules Detected: ", capsule_count)
