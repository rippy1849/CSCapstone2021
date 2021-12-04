# import the necessary packages
import numpy as np
import cv2
import time
import os
import subprocess
#result = subprocess.run(['sudo v4l2-ctl --list-devices', '-l'], stdout=subprocess.PIPE)
result = subprocess.check_output('sudo v4l2-ctl --list-devices', shell=True, text=True)

output_arr = str(result).split()
device_num = ""
device_num_2  = ""

cam1 = "(usb-0000:01:00.0-1.1.2):"
cam2 = "(usb-0000:01:00.0-1.2.1.2):"

for i,entry in enumerate(output_arr):
    if entry == cam1:
        device_num = output_arr[i+1]
    elif entry == cam2:
        device_num_2 = output_arr[i+1]

print(device_num)

# initialize the HOG descriptor/person detector
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

cv2.startWindowThread()

# open webcam video stream
cap = cv2.VideoCapture(-1)


os.system('sudo v4l2-ctl --set-ctrl pan_absolute=0 --device ' + device_num)
#os.system('sudo v4l2-ctl --set-ctrl tilt_absolute=-18000000 --device /dev/video0')
os.system('sudo v4l2-ctl --set-ctrl tilt_absolute=2000000 --device ' + device_num)


pan_abs = 0
tilt_abs = 0

xthresh = 30
posx = 120
center = 120

pan_wait = time.time()

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    frame = cv2.flip(frame, 0)
    frame = cv2.resize(frame, (320, 240))
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    
    #posx = center

    
    boxes, weights = hog.detectMultiScale(frame, winStride=(8,8) )

    boxes = np.array([[x, y, x + w, y + h] for (x, y, w, h) in boxes])

    for (xA, yA, xB, yB) in boxes:
            # display the detected boxes in the colour picture
        cv2.rectangle(frame, (xA, yA), (xB, yB),
                            (0, 255, 0), 2)
        
        posx = xA
    
    
    #shift = 120 - posx
    #print(shift)
    
    
    #print(posx)
    if time.time() - pan_wait > 5:
        if posx < center-xthresh:
            #print("LEFT")
            s1 = (center-xthresh) - posx
                
            pan_abs -= int(30000*(1+(s1/(center-xthresh))))
            if np.abs(pan_abs)>7200000:
                pan_abs = -7200000
            #print(s1)
            string = 'sudo v4l2-ctl --set-ctrl pan_absolute=' + str(pan_abs) + ' --device ' + device_num
            os.system(string)
            #posx = 120
                
                
        if posx > center+xthresh:
            #print("LEFT")
            s1 = posx - (center+xthresh)
                
            pan_abs += int(30000*(1+(s1/(center-xthresh))))
            if np.abs(pan_abs)>7200000:
                pan_abs = 7200000
                
            #print(s1)
            string = 'sudo v4l2-ctl --set-ctrl pan_absolute=' + str(pan_abs) + ' --device ' + device_num
            os.system(string)
            #posx = 120
            
            
            
        
    
    
    
    
    

    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
# and release the output
out.release()
# finally, close the window
cv2.destroyAllWindows()
cv2.waitKey(1)