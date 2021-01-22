## function for returning colors found in a image
## written specifically for SEAI-SEPCAP project
##
## inputs: (image) image to detect color         
##
## outputs: (colors_detected) capsule colors detected


#imports
from boundingBox import boundBox
from aux_functions import area
import cv2 as cv
import numpy as np

def click(event, x, y, flags, param):
    if event == cv.EVENT_LBUTTONDOWN:
         print(crop[y,x])

def colorDetector(image, min_area, proportion, boundaries):

    colors_detected = []
    p = proportion
    name_mask = "blue"

    #boundaries for each color - NEED ADJUSTING
    boundaries = boundaries
    
    

    #black mask for detection of capsule and cropping
    mask = cv.inRange(image, np.array([0,0,0]) , np.array([40,40,40])) #mudei de 30,30,30
    mask = (255 - mask)
    #cv.imshow("mask", mask)
    

    rect = boundBox(image, mask, min_area = min_area)
    #print(rect)

    if (len(rect) == 1):
        #crop image
        #print("Rectangles:", rect)
        crop = image[rect[0][1]+int((1-(p)) * rect[0][3]) : rect[0][1] + int((p) * rect[0][3]), \
             rect[0][0]+int((1-(p)) * rect[0][2]):rect[0][0] + int((p) * rect[0][2])]
        #print("X: ", rect[0][0]+int((1-(p)) * rect[0][2]))
        #print("Y: ", rect[0][1]+int((1-(p)) * rect[0][1]))
        kernel = np.ones((9,9), np.uint8) #mudei de 7,7
        crop = cv.erode(crop, kernel)
        #cv.imshow("Cropped image", crop)
        #cv.imshow("Cropped image", cv.resize(crop, None, fx = 3, fy = 3, interpolation= cv.INTER_CUBIC))
        #cv.setMouseCallback("Cropped image", click)
        
        #detect colors in cropped image
        for (lower,upper, color) in boundaries:
            lower = np.array(lower, dtype = 'uint8')
            upper = np.array(upper, dtype= 'uint8')
            if crop.any():
                if cv.inRange(crop, lower, upper).any():
                    colors_detected.append(color)
                    if color == name_mask:
                        mask = cv.inRange(crop, lower, upper)
                        #cv.imshow("mask",mask)
            if len(colors_detected) == 2:
                break
    else:
        colors_detected = []
    
    #print(colors_detected)
    return colors_detected, rect
