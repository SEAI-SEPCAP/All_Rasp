## function for returning bounding box for a black and white image
## written specifically for SEAI-SEPCAP project
##
## inputs: (image) image to draw rectangle in
##         (threshold_image) "black and white image" 
##         (min_area) minimal area of bounding box
##
## outputs: (finalRect) points for bounding box of capsule


#imports
import cv2 as cv
import numpy as np
from aux_functions import area


def boundBox(image, threshold_image, min_area):
    
    _, contours, _ = cv.findContours(threshold_image, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    
    contours_poly = [None] * len(contours)
    boundRect = [None] * len(contours)
    finalRect = []

    #creates contours and bounding box points
    for i, c in enumerate(contours):
        contours_poly[i] = cv.approxPolyDP(c,3,True)
        boundRect[i] = cv.boundingRect(contours_poly[i])
    
    #saves bounding box points where area values that are greater than minimal area
    for i, values in enumerate(boundRect):
        if area(boundRect[i][2], boundRect[i][3]) > min_area:
            finalRect.append(boundRect[i])

    # box_image -> where the bounding boxes will be drawn
    box_image = image

    for i in range(len(finalRect)):
        color_rect = (0,255,0) #color of bounding box

        #drawing the rectangle
        cv.rectangle(box_image, (int(finalRect[i][0]), int(finalRect[i][1])), \
            (int(finalRect[i][0]+finalRect[i][2]), int(finalRect[i][1]+finalRect[i][3])), color_rect, 2)


    #cv.imshow('Image with Bounding Box', box_image)
    return finalRect
