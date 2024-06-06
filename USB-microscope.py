#!/usr/bin/env python3
'''
Trying to get a small microscope cam into a better life.
'''
#--------------------------------------------------------------------------
#  USB-microscope.py
#  Author: Winfried Koehler
#  Date: 8 May, 2024 
#  Source: https://github.com/wirbel-at-vdr-portal/Python-USB-Microscope
#  License: MIT-License
#--------------------------------------------------------------------------


import platform
import cv2
import numpy as np


# global variables
dev = 0                   # change here to open another video device, '0' is the default or first device
width = 640               # raw image width as delivered
height = 480              # raw image height as delivered
scale = 2                 # image scaling
newWidth = width*scale    # changes on request
newHeight = height*scale  # changes on request
alpha = 1.0               # gain   or 'contrast' (1.0-3.0)
beta = 0.0                # offset or 'brightness', +/- 100 in steps of ten
rad = 0                   # image smoothing filter: blur radius
osd = True                # show menu/osd in upper left                
fullscreen = False        # fullscreen yes/no
inverted = False          # inverted colors
bgr = False               # display false colors
rotate = 0                # image not rotated, 0..3 clockwise
raw_data_info = True      # show infos about captured data


	
# opencv video capture device
if platform.system() == 'Windows':
   cap = cv2.VideoCapture(int(dev))
else:
   cap = cv2.VideoCapture('/dev/video'+str(dev), cv2.CAP_V4L)

cv2.namedWindow('USB-Microscope', cv2.WINDOW_GUI_NORMAL)
cv2.resizeWindow('USB-Microscope', newWidth, newHeight)

while(cap.isOpened()):
   ret, frame = cap.read()
   if ret == True:
      if raw_data_info:
         #---------------------
         # frame = numpy.ndarray
         print('Type: ' + str(frame.dtype));                       # Type: uint8
         print('Dimensions: ' + str(frame.ndim))                   # Dimensions: 3
         print('Shape: ' + str(frame.shape))                       # Shape: (480, 640, 3)
         print('Size: ' + str(frame.size))                         # Size: 921600
         #print('Size of the first dimension: ' + str(len(frame))) # Size of the first dimension: 480
         raw_data_info = False
         print('Press <ESC> or q to close video window.')
         #---------------------

      # rotate = 0..3 -> 0 .. 270
      # see also: enum cv::RotateFlags
      # -> rotating image requires resizeWindow, otherwise the image would be distorted
      if rotate > 0:
         frame = cv2.rotate(frame, rotate - 1);

      # image contrast and brightness
      frame = cv2.convertScaleAbs(frame, alpha = alpha, beta = beta);
      
      # upscaling using bicubic interpolation
      frame = cv2.resize(frame,(newWidth,newHeight), interpolation=cv2.INTER_CUBIC)

      # image smoothing using blur
      if rad > 0:
         frame = cv2.blur(frame,(rad,rad))

      if inverted:
         frame = cv2.bitwise_not(frame)

      if bgr:
         frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

      if osd:
         # display black background box
         cv2.rectangle(frame, (0,0), (160,160), (0,0,0), -1)
         p = 14

         cv2.putText(frame,'Scale (+/-): '+str(scale)    , (10, p), cv2.FONT_HERSHEY_SIMPLEX, 0.4,(0, 255, 255), 1, cv2.LINE_AA)
         p += 14

         cv2.putText(frame,'Blur (s): '+str(rad)         , (10, p),cv2.FONT_HERSHEY_SIMPLEX, 0.4,(0, 255, 255), 1, cv2.LINE_AA)
         p += 14

         cv2.putText(frame,'Bright (b): '+str(beta)      , (10, p), cv2.FONT_HERSHEY_SIMPLEX, 0.4,(0, 255, 255), 1, cv2.LINE_AA)
         p += 14

         cv2.putText(frame,'Contrast (c): '+str(alpha)   , (10, p), cv2.FONT_HERSHEY_SIMPLEX, 0.4,(0, 255, 255), 1, cv2.LINE_AA)
         p += 14

         cv2.putText(frame,'Rotate (r): '+str(rotate*90) , (10, p), cv2.FONT_HERSHEY_SIMPLEX, 0.4,(0, 255, 255), 1, cv2.LINE_AA)
         p += 14

         cv2.putText(frame,'Invert (i): '+str(inverted)  , (10, p), cv2.FONT_HERSHEY_SIMPLEX, 0.4,(0, 255, 255), 1, cv2.LINE_AA)
         p += 14

         cv2.putText(frame,'false color (e): '+str(bgr)  , (10, p), cv2.FONT_HERSHEY_SIMPLEX, 0.4,(0, 255, 255), 1, cv2.LINE_AA)
         p += 14

         cv2.putText(frame,'Menu (m): '+str(osd)         , (10, p), cv2.FONT_HERSHEY_SIMPLEX, 0.4,(0, 255, 255), 1, cv2.LINE_AA)
         p += 14

         cv2.putText(frame,'Snapshot (CTRL+s)'           , (10, p), cv2.FONT_HERSHEY_SIMPLEX, 0.4,(0, 255, 255), 1, cv2.LINE_AA)
         p += 14

         cv2.putText(frame,'Close (ESC or q)'            , (10, p), cv2.FONT_HERSHEY_SIMPLEX, 0.4,(0, 255, 255), 1, cv2.LINE_AA)
         p += 14

      # the image is prepared, put it to our window.
      cv2.imshow('USB-Microscope', frame);

      # cv2.waitKey, reading users key presses and give window time to redraw
      # 5msec wait time, 25 fps would allow up to 40msec
      key = cv2.waitKey(5)
      match(key):
         # for those magic numbers, see ASCII table.
         case 113: # 'q', exit program
            break
         case 27:  # <ESC>, exit program
            break
         case 43:  # '+', increase scale
            scale = min(5, scale + 1)
            newWidth  = width *scale 
            newHeight = height*scale
            if not fullscreen:
               cv2.resizeWindow('USB-Microscope', newWidth, newHeight)
         case 45:  # '-', decrease scale
            scale = max(1, scale - 1)
            newWidth  = width *scale 
            newHeight = height*scale
            if not fullscreen:
               cv2.resizeWindow('USB-Microscope', newWidth, newHeight)
         case 102: # 'f', toggle fullscreen
            fullscreen = not fullscreen
            if fullscreen:
               cv2.setWindowProperty('USB-Microscope',cv2.WND_PROP_FULLSCREEN, 1)
            else:
               cv2.setWindowProperty('USB-Microscope',cv2.WND_PROP_FULLSCREEN, 0)
         case 109: # 'm', toggle menu
            osd = not osd
         case 98:  # 'b', toggle through brightnesss values
            beta += 10
            beta = int(10.0 * beta + 0.5) / 10.0
            if beta > 100.01:
               beta = -100            
         case 99:  # 'c', toggle through contrast values
            alpha += 0.1
            alpha = int(10.0 * alpha + 0.5) / 10.0
            if alpha > 3.01:
               alpha = 0
         case 101: # 'i', toggle flase colors
            bgr = not bgr
         case 105: # 'i', toggle inverted image
            inverted = not inverted
         case 114: # 'r', rotate clockwise
            rotate += 1
            if rotate > 3:
               rotate = 0
            tmp = width
            width = height
            height = tmp
            newWidth = width*scale 
            newHeight = height*scale
            if not fullscreen:
               cv2.resizeWindow('USB-Microscope', newWidth, newHeight)
         case 115: # 's', toggle through image smoothing radius values
            rad += 1
            if rad > 5:
               rad = 0
         case _:   # default. unknown or timeout
            if key > -1:
               print('unknown key: ' + str(key) + ' ' + chr(39) + chr(key) + chr(39))
      #-----------------

cap.release()
cv2.destroyAllWindows()
		
