import cv2 
import numpy as np 
import imutils
#import pyautogui
def GameLoop():
    img = np.ones((480,640,3),dtype=np.uint8) *200
    rech,recw = 30,200

    dx,dy = 4,4
    x,y = 100,100
    xr,yr = 250,420
    camera=cv2.VideoCapture(0)
    redlower = (157, 93,203)# low scale of red color value
    redupper = (179,255,255)# high scale of red color value
    while True:
        #Draw Background
        cv2.imshow('Game',img)
        #Draw circle
        img = np.ones((480,640,3),dtype=np.uint8) *200
        cv2.circle(img,(x,y),20,(255,0,0),-1)
        cv2.rectangle(img,pt2=(xr,yr),pt1=(xr+recw,yr+rech),color=(255,255,0),thickness=-1)
        # Update position Circle
        x = x+dx
        y = y+dy
        # Check Collision With borders
        if y>=460 or y<=20:
            dy =dy*(-1)
        if x>=650 or x<=20:
            dx = dx*(-1)
        #Check Collisions racket with borders
        if xr<=0:
            xr = 0
        if xr>=640-recw:
            xr=640-recw
        #Check Collision with top racket
        if y>=(yr-20) and x>xr and x<(xr+recw):
            dy*=-1
            y-=5
        #Check Collision with bottom racket
        if y>=(yr+rech) and  x>xr and x<(xr+recw):
            dy*=-1 
            #Lose
        
        ## Get Movement 
        (grabbed, frame)=camera.read()
        cv2.imshow('Camera',frame)
        frame=imutils.resize(frame,width=600)
        blur=cv2.GaussianBlur(frame,(11,11),0)
        hsv = cv2.cvtColor(blur,cv2.COLOR_BGR2HSV)#converting image color to hsv and storing the value
        mask=cv2.inRange(hsv,redlower,redupper)#comapring hsv value of image with the other parameters
        mask=cv2.erode(mask,None,iterations=2)# this filter is used to remove noise in the image
        mask=cv2.dilate(mask,None,iterations=2)#this filter is used to remove noise in the image
        cnts=cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
        center=None
        if len(cnts) > 0:
            c=max(cnts, key=cv2.contourArea)# find maximum contour area
            ((x_,y_),radius)=cv2.minEnclosingCircle(c)# used to create an minimum enclosing circle around the object absed on the coordinates ,radius
            M=cv2.moments(c)
            center=(int(M["m10"]/M["m00"]),int(M["m01"]/M["m00"]))# finding the center of the minimum enclosing circle(x,y)
            if radius > 0:
                cv2.circle(frame,(int(x),int(y)),int(radius),(0,255,255),2)# this functions specifies the color ,thickness boundary of minimum circle
                cv2.circle(frame,center,5,(0,0,255),-1)# this function specifies the center within the minimum circle along with its coordinates
                print(center[0],center[1])
                if radius >250:
                    print("stop")
                else:
                    if(center[0]>300):
                        print("right")
                        xr =xr+10
                    elif(center[0]<300):
                        print("left")
                        xr-=10
                  
                    else:
                        print("stop")            
        #xr = pyautogui.position()[0] 
        if cv2.waitKey(10)&0xFF==ord('q'):
            break

GameLoop()