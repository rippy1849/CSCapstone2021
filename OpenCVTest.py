import cv2
import time
import imutils





vid = cv2.VideoCapture(-1)
vid.set(3, 1080)
vid.set(4, 1920)
#vid.set(cv2.CAP_PROP_EXPOSURE,-5)
print(dir(vid))
#haar_cascade_face = cv2.CascadeClassifier('./haarcascade_frontalface_default.xml')

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

while(True):

    # Capture the video frame by frame
    ret, frame = vid.read()
    
    
    
    
    
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
    
    
    
    
    
    
    # loop over the contours
    c_count = 0
    xavg = 0
    for c in cnts:
        # if the contour is too small, ignore it
        if cv2.contourArea(c) < 750:
            continue
        (x, y, w, h) = cv2.boundingRect(c)
        xavg += x
        c_count += 1
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    if(c_count!=0):
        xavg = xavg/c_count
        xavg = 405-xavg
    print(xavg)
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
    
    cv2.imshow('frame', frame)
      
    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
  
# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()