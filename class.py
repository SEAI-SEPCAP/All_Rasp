#!/usr/bin/python3 -u

## main algorithm of classification part of project SEAI-SEPCAP


#imports
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
## 4 - blue and white
## 5 - red and white
## 6 - dark green and white
## 7 - dark green and nude 
## 8 - nude
## 9 - dark green and light green

def capsule_type(colors):
    if len(colors) == 1:
        color = colors[0]
        if color == 'yellow':
            return 1
        elif color == 'red':
            return 2
        elif color == 'white':
            return 3
        elif color == 'nude':
            return 8
        elif color == 'blue':
            return 4
    
    elif len(colors) == 2:
        
        if("yellow" in colors):
            return 1
        elif ("red" in colors) and ("white" in colors):
            return 5
        elif ("dark green" in colors) and ("white" in colors):
            return 6
        elif ("dark green" in colors) and ("nude" in colors):
            return 7
        elif ("blue" in colors):
            return 4
        elif ("dark green" in colors) and ("light green" in colors):
            return 9
        else: return 0
    else: return 0
    
#assistant function for detecting RGB variables
def click(event, x, y, flags, param):
    if event == cv.EVENT_LBUTTONDOWN:
         print(image[y,x])
         print("X:", x ,"Y:", y)

#initial boundaries
boundaries = [
    ([5,0,110],[60,40,230], 'red'), 
    ([170,70,0],[255,150,30], 'blue'), 
    #([65,110,185],[75,120,195], 'orange'), #orange not used
    ([15,145,160],[50,190,210], 'yellow'),
    ([95,165,205],[135,210,230], 'nude'),
    ([35,40,5],[70,80,20], 'dark green'),
    ([200,190,200],[232,232,232], 'white'),
    ([135,135,105],[145,145,115], 'light green')
    ]

#calibration mode
rgb_alter = [0,0,0]

###starting variables
#flags for capsule detection
flag = 0
old_flag = 1
start = 0
#total capsule ## NOT NEEDED 
capsule_count = 0

###adjustable variables
min_area = 30000    #change minimal area for capsule
blur = 9            #change value for blur
crop_p = 0.8       #proportion of crop 


# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 45
rawCapture = PiRGBArray(camera, size=(640, 480))
# allow the camera to warmup
time.sleep(0.1)


#comms initialization
sms = SMS(open(sys.argv[1], "rb"), open(sys.argv[2], "wb"))

#sends message to interface -
# "sep.jpg" was overwritten to show on calibration mode
def send_calib_message(image):
    cv.imwrite("sep.jpg", image)
    print("image was written")
    sms.sendPacket(
           SMS.Address.Interface, 
           SMS.Message.CalibrationConf.type, 
           0)
    

#while loop for video capturing
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # grab the raw NumPy array representing the image
    image = frame.array
    
    image = image[0:480,400:560]
    
    #blur the image 
    image = cv.medianBlur(image, blur)
    
    ### CALIBRATION
    if sms.isData():
            address, mtype, data = sms.readPacket()
            if ((address==SMS.Address.Classification)):
                if (mtype==SMS.Message.CalibrationColor.type):
                    send_calib_message(image)
                    if(data==SMS.Message.CalibrationColor.Red):
                        color_alter = "red"
                    elif(data==SMS.Message.CalibrationColor.Yellow):
                        color_alter = "yellow"
                    elif(data==SMS.Message.CalibrationColor.White):
                        color_alter = "white"
                    elif(data==SMS.Message.CalibrationColor.Blue):
                        color_alter = "blue"
                    elif(data==SMS.Message.CalibrationColor.Dark_Green):
                        color_alter = "dark green"
                    elif(data==SMS.Message.CalibrationColor.Nude):
                        color_alter = "nude"
                    elif(data==SMS.Message.CalibrationColor.Light_Green):
                        color_alter = "light green"
                elif(mtype==SMS.Message.CalibrationR.type):
                    print(rgb_alter)
                    rgb_alter[2] = int(data)
                    print(rgb_alter)
                elif(mtype==SMS.Message.CalibrationG.type):
                    print(rgb_alter)
                    rgb_alter[1] = int(data)
                    print(rgb_alter)
                elif(mtype==SMS.Message.CalibrationB.type):
                    print(rgb_alter)
                    rgb_alter[0] = int(data)
                    print(rgb_alter)
                    boundaries = alter(boundaries, color_alter, rgb_alter)
                    print(boundaries)
                    print("BOUNDARIES WERE ALTERED")
                #elif(mtype==SMS.Message.CalibrationConf.type):
                    
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
