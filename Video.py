#Adapted from the Bounding boxes tutorial here: https://www.youtube.com/watch?v=O3b8lVF93jU
#Adapted this to the OpenCV tutorial for video feeds at https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_gui/py_video_display/py_video_display.html
#improvements were added to adapt this code to using hsv thresholding as opposed to binary thresholding
#Code for understanding color spaces was adapted from https://docs.opencv.org/4.x/df/d9d/tutorial_py_colorspaces.html
import numpy as np
import cv2 
from sklearn.cluster import KMeans

cap = cv2.VideoCapture(0)
#obj_det = cv2.createBackgroundSubtractorMOG2()
while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    # Our operations on the frame come here
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # Display the resulting frame
    lower_blu = np.array([90,50,50])
    upper_blu = np.array([110,255,255])
    mask = cv2.inRange(hsv,lower_blu,upper_blu)
    contours, _ = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 100:
            #cv2.drawContours(frame,[cnt],-1,(0,255,0),2)
            x,y,w,h = cv2.boundingRect(cnt)
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),3)
    cv2.imshow('frame',frame)
    #cv2.imshow('Thresholding',mask)
    key = cv2.waitKey(1)
    if key == ord("q"):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()