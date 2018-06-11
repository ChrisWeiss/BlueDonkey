#!/usr/bin/env python3
import os, sys
#if not os.geteuid() == 0:
#    sys.exit("\nPlease run as root.\n")
if sys.version_info < (3,0):
    sys.exit("\nPlease run under python3.\n")

import cv2, time
#capture = cv2.VideoCapture(0)
#capture.set(cv2.CAP_PROP_FPS, 10)
#capture.set(cv2.CAP_PROP_FRAME_WIDTH, 160)
#capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 120)
#capture.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)
#capture.set(cv2.CAP_PROP_EXPOSURE, 0.003)

import numpy

def capture_and_process_frame():
    #ret, frame = capture.read()
    frame = cv2.imread('camera01.jpg')
    ret = True

    if ret:
        cv2.imwrite('/run/bluedonkey/camera.jpg', frame)
        lower_yellow = numpy.array([0,160,160])
        upper_yellow = numpy.array([220,255,255])
        mask = cv2.inRange(frame, lower_yellow, upper_yellow)
        res = cv2.bitwise_and(frame, frame, mask=mask)
        cv2.rectangle(res, (0,0), (159,119), (0,0,0), 2)
        #cv2.imwrite('/run/bluedonkey/filtered.jpg', res)
        gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (7, 7), 0)
        edges = cv2.Canny(blur, 50, 150)
        dilation = cv2.dilate(edges, cv2.getStructuringElement(cv2.MORPH_DILATE, (5, 5)))
        erosion = cv2.erode(dilation, cv2.getStructuringElement(cv2.MORPH_ERODE, (3, 3)))
        merge = gray + erosion
        lines = cv2.HoughLinesP(merge, 2, numpy.pi/180, 12, numpy.array([]), minLineLength=10, maxLineGap=30)
        line_img = numpy.zeros((merge.shape[0], merge.shape[1], 3), dtype=numpy.uint8)
        for line in lines:
            for x1,y1,x2,y2 in line:
                angle = numpy.arctan2(y2 - y1, x2 - x1) * 180. / numpy.pi
                if ( (abs(angle) > 20.) and (abs(angle) < 90.)):
                    cv2.line(line_img, (x1, y1), (x2, y2), (0,0,255), 1)
        cv2.imwrite('/run/bluedonkey/filtered.jpg', line_img)
    
    time.sleep(0.2)

#while(capture.isOpened()):
#   capture_and_process_frame()
capture_and_process_frame()
#capture.release()
