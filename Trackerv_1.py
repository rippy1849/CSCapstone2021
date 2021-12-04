import cv2
import time
import imutils
import os






def setZoom(zoom):
    
    os.system('v4l2-ctl --device /dev/video0 --set-ctrl zoom_absolute=' + str(zoom))    
    
    return





  




vid = cv2.VideoCapture(-1)
vid.set(3, 1080)
vid.set(4, 1920)
vid.set(cv2.CAP_PROP_EXPOSURE,-5)
#print(dir(vid))
#haar_cascade_face = cv2.CascadeClassifier('./haarcascade_frontalface_default.xml')

ret, first_frame = vid.read()

mp = []

mp.append(first_frame)


scale_percent = 50
width = int(first_frame.shape[1] * scale_percent /100)
height = int(first_frame.shape[0] * scale_percent/ 100)
dim = (width,height)
lasttime = 0
pantime = 0


search_time = 0




fpstime = 0
fps = 0

pan_abs = 0
tilt_abs = 0

mp = []

os.system('sudo v4l2-ctl --set-ctrl pan_absolute=0 --device /dev/video0')
#os.system('sudo v4l2-ctl --set-ctrl tilt_absolute=-18000000 --device /dev/video0')
os.system('sudo v4l2-ctl --set-ctrl tilt_absolute=0 --device /dev/video0')
setZoom(0)

hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())



pad = 20


time.sleep(4)

while(True):

    
    
    
    
    
    
    
    
    
    
    human = False
    human_pos = []
    
    # Capture the video frame by frame
    ret, frame = vid.read()
    #fps += 1
    #if time.time() - fpstime > 20:
        #fpstime = time.time()
        #print(fps/20)
        #fps = 0
    frame = cv2.flip(frame, 0)
    
                
    
    
    
    
    
    frame = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred_frame = cv2.GaussianBlur(gray_frame, (21,21), 0)
    
    if time.time() - lasttime > 0.5:
        lasttime = time.time()
        first_frame = blurred_frame
        
    
    
    
    
    change_frame = cv2.absdiff(first_frame,blurred_frame)
    thresh = cv2.threshold(change_frame, 25, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=2)
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    
    
    
    
    posx = int(frame.shape[1]/2)
    
    posy = int(frame.shape[0]/2)
    
    
    new_avg = 0
    human_count = 0
    # loop over the contours
    c_count = 0
    xavg = 0
    room = False
    mp = []
    for c in cnts:
        # if the contour is too small, ignore it
        if cv2.contourArea(c) < 750:
            continue
        (x, y, w, h) = cv2.boundingRect(c)
        
        
        if w < 200 and w > 0 and h > 50:
            #print("Area:" + str(h*w))
            #print("width: " + str(w))
            
            
            xavg += x+(w/2)
            
            human_pos.append(x+(w/2))
            c_count += 1
            #print(c)
            #print(c_count)
            
            w1 = x+w
            w2 = x
            
            l1 = y+h
            l2 = y
            
            if x-pad > 0:
                w2 -= pad
                w1 += pad
            if (posx*2) < w1+pad:
                w1 += pad
            if y-pad > 0:
                l2 -= pad
                l1 += pad
            if (posy*2) < l1+pad:
                l1 += pad
            
            
            
            
            
            mp.append(frame[l2:l1,w2:w1])
            
            #cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
            
    #print(human_pos)
    for k,image in enumerate(mp):
        #rects, weights = hog.detectMultiScale(image, padding=(4, 4), scale=1.08)
        boxes, weights = hog.detectMultiScale(image, padding=(4, 4), scale=1.2)
        #print(weights)
        for i, entry in enumerate(boxes):
            if weights[i] > 0.2:
                print("HUMAN")
                human = True
                human_count +=1
                new_avg += human_pos[k]
                
                
                
    
    if c_count != 0:
        xavg = xavg/c_count
    else:
        xavg = frame.shape[1]/2
    
    
    
    if new_avg ==0:
        new_avg = posx
    else:
        new_avg = new_avg/human_count
    
    
    
    #print(new_avg)
    
    xthresh = 85
    #cv2.rectangle(frame, (posx-xthresh, 0), (posx+xthresh, posy*2), (255, 0, 0), 2)
    
    
    if time.time() - pantime > 0 and human == True:
        
        
        
        
        #print(xavg)
        if new_avg < posx-xthresh:
            #print("LEFT")
            s1 = (posx-xthresh)-new_avg
            
            pan_abs -= int(300000*(1+4*(s1/(posx-xthresh))**2))
            
            
            
        if new_avg > posx+xthresh:
            #print("RIGHT")
            s2 = new_avg-(posx+xthresh)
            pan_abs += int(300000*(1+4*(s2/(posx-xthresh))**2))
            
            
            
        
        string = 'sudo v4l2-ctl --set-ctrl pan_absolute=' + str(pan_abs) + ' --device /dev/video0'
        os.system(string)
        pantime = time.time()
        
        
        #print(xavg)
        #xavg = frame.shape[1]/2
        
        
        
        
        
    
    #setZoom(60)    
    #cv2.imshow('frame', thresh)
    cv2.imshow('frame',frame)
    
    if len(mp) > 0:
        #print(len(mp))
        for i, m in enumerate(mp):
            cv2.imshow('Moved' + str(i), m)
    
        
    
      
    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
  
# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()