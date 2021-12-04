# import the necessary packages
import numpy as np
import cv2
import time
import os
import subprocess
result = subprocess.check_output('sudo v4l2-ctl --list-devices', shell=True, text=True)

output_arr = str(result).split()
device_num = ""
device_num_2  = ""

cam1 = "(usb-0000:01:00.0-1.1.2):"
cam2 = "(usb-0000:01:00.0-1.2.1.2):"

def setTPZ(tilt,pan,zoom,device):
    os.system('sudo v4l2-ctl --set-ctrl tilt_absolute='+ str(tilt) +'[,pan_absolute='+ str(pan) +',zoom_absolute='+ str(zoom)+'] --device ' + device)
    return

def setBoard(board_num):
    if board_num == 1:
    #B1
        setTPZ(0,-750000,49,device_num)           
    if board_num == 2:
    #B2
        setTPZ(500000,400000,62,device_num)    
    if board_num == 3:
    #B3
        setTPZ(500000,2100000,42,device_num)  
    if board_num == 4:
    #B4
        setTPZ(500000,3900000,32,device_num)
    if board_num == 5:
    #B5
        setTPZ(800000,6700000,33,device_num) 
    return



for i,entry in enumerate(output_arr):
    if entry == cam2:
        device_num = output_arr[i+1]

print(device_num)

# initialize the HOG descriptor/person detector
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

cv2.startWindowThread()

# open webcam video stream
#4 is for cam2
#-1 is for cam1


cap = cv2.VideoCapture(4)
cap.set(3, 1920)
cap.set(4, 1080)





#os.system('sudo v4l2-ctl --set-ctrl pan_absolute=0 --device ' + device_num)
#os.system('sudo v4l2-ctl --set-ctrl tilt_absolute=-18000000 --device /dev/video0')
#os.system('sudo v4l2-ctl --set-ctrl tilt_absolute=2000000 --device ' + device_num)

#setTPZ(0,2900000,0,device_num)
setBoard(2)
pan_abs = 0
tilt_abs = 0

xthresh = 30
posx = 120
center = 120

pan_wait = time.time()
count = 0


while(True):
    # Capture frame-by-frame
    ret, frame_org = cap.read()
    ret, frame = cap.read()
    frame_org = cv2.flip(frame_org, 0)
    frame = cv2.flip(frame, 0)
    frame = cv2.resize(frame, (320, 240))
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

    
    
    
    if time.time()-pan_wait > 10:
        setBoard((count%5)+1)
        pan_wait = time.time()
        count += 1
    
    #shift = 120 - posx
    #print(shift)
    
    
    #print(posx)

                
    #B1
    #setTPZ(0,-750000,49,device_num)           
    #B2
    #setTPZ(500000,400000,62,device_num)    
    #B3
    #setTPZ(500000,2100000,42,device_num)  
    #B4
    #setTPZ(500000,3900000,32,device_num)
    #B5
    #setTPZ(800000,6700000,33,device_num)
    
    
    
    
    
    
    

    cv2.imshow('frame',frame_org)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
# and release the output
out.release()
# finally, close the window
cv2.destroyAllWindows()
cv2.waitKey(1)