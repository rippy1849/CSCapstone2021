import cv2
import time
import imutils
import numpy as np
import os

def im_rescale(image, scale_percent):
    width = int(image.shape[1] * scale_percent /100)
    height = int(image.shape[0] *scale_percent/ 100)
    dim = (width,height)
    
    return cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
    








vid = cv2.VideoCapture(0)
vid.set(3, 1080)
vid.set(4, 1920)
vid.set(cv2.CAP_PROP_EXPOSURE,-5)

#haar_cascade_face = cv2.CascadeClassifier('./haarcascade_frontalface_default.xml')

#full_body = cv2.CascadeClassifier('./haarcascade_fullbody.xml')

hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())


time.sleep(3)

ret, first_frame = vid.read()

scale_percent = 75
width = int(first_frame.shape[1] * scale_percent /100)
height = int(first_frame.shape[0] * scale_percent/ 100)
dim = (width,height)
#first_frame = cv2.resize(first_frame, dim, interpolation = cv2.INTER_AREA)
#first_frame = cv2.cvtColor(first_frame, cv2.COLOR_BGR2GRAY)
#first_frame = cv2.GaussianBlur(first_frame, (21,21), 0)
lasttime = 0

pan_abs = 0
tilt_abs = 0

os.system('sudo v4l2-ctl --set-ctrl pan_absolute=0 --device /dev/video0')
os.system('sudo v4l2-ctl --set-ctrl tilt_absolute=-18000000 --device /dev/video0')

while(True):

    # Capture the video frame by frame
    ret, frame = vid.read()
    
    
    
    
    
    frame = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred_frame = cv2.GaussianBlur(gray_frame, (21,21), 0)
    
    
    #bodies = full_body.detectMultiScale(gray_frame, 1.3, 5)
    
    
    
    
    
    #print(bodies)
    
    rects, weights = hog.detectMultiScale(gray_frame, padding=(4, 4), scale=1.08)
    #rects, weights = hog.detectMultiScale(gray_frame, winStride=(8,8))
    
    #if time.time() - lasttime > 3:
        #first_frame = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)
        #gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #blurred_frame = cv2.GaussianBlur(gray_frame, (21,21), 0)
    
    #change_frame = cv2.absdiff(first_frame,blurred_frame)
    #thresh = cv2.threshold(change_frame, 25, 255, cv2.THRESH_BINARY)[1]
    #thresh = cv2.dilate(thresh, None, iterations=2)
    #cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    #cnts = imutils.grab_contours(cnts)
    
    
    

    #for i, (x, y, w, h) in enumerate(rects):
    #    if weights[i] < 0.13:
    #        continue
    #    elif weights[i] < 0.3 and weights[i] > 0.13:
    #        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
    #    if weights[i] < 0.7 and weights[i] > 0.3:
    #        cv2.rectangle(frame, (x, y), (x+w, y+h), (50, 122, 255), 2)
    #    if weights[i] > 0.7:
    #        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
    
    
    
    # loop over the contours
    # c_count = 0
    # xavg = 0
    # for c in cnts:
    #     # if the contour is too small, ignore it
    #     if cv2.contourArea(c) < 5000:
    #         continue
    #     (x, y, w, h) = cv2.boundingRect(c)
    #     #print(c[0])
    #     print(cv2.contourArea(c))
    #     xavg += x
    #     c_count += 1
    #     cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    # if(c_count!=0):
    #     xavg = xavg/c_count
    #     xavg = frame.shape[1]/2-xavg
    #     if(np.abs(xavg)<100):
    #         xavg = 0
    
    
    #negative is right relative to camera, postive is left
    # if xavg > 0:
    #     print("Move Left")
    # if xavg < 0:
    #     print("Move Right")
    #faces_rects = haar_cascade_face.detectMultiScale(gframe, scaleFactor = 1.2, minNeighbors = 5);
    #print(len(faces_rects))
    #Convert Frame to Gray
    #gframe = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    #edges = cv2.Canny(frame,75,175)
    
    # fd, hog_image = hog(frame, orientations=8, pixels_per_cell=(16, 16),
    #                 cells_per_block=(1, 1), visualize=True)
    
    # Display the resulting frame
    #line_red = cv2.rectangle(frame,(0,0),(511,511),(0,0,255),5)
    # for (x,y,w,h) in faces_rects:
    #     cv2.rectangle(frame, (x, y), (x+w, y+h), (int(y%255), int(x%255), 0), 2)
    
    re_count = 0
    xavg = 0
    yavg = 0
    
    for (x,y,w,h) in rects:
    
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,255),2)
        xavg += x
        yavg += y
        re_count += 1
    if re_count != 0:
        xavg = xavg/re_count
        yavg = yavg/re_count
    else:
        xavg = frame.shape[1]/2
        yavg = frame.shape[0]/2
    
    posx = frame.shape[1]/2
    posy = frame.shape[0]/2
    
    if xavg < posx-200:
        print("LEFT")
        pan_abs -= 300000
    if xavg > posx+200:
        print("RIGHT")
        pan_abs += 300000
    
    
    
    
    string = 'sudo v4l2-ctl --set-ctrl pan_absolute=' + str(pan_abs) + ' --device /dev/video0'
    os.system(string)
    #string = 'sudo v4l2-ctl --set-ctrl tilt_absolute=' + str(tilt_abs) + ' --device /dev/video0'
    #os.system(string)
    
    cv2.imshow('frame', blurred_frame)
    
    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
  
# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()