import imutils
import cv2
import numpy as np
from random import randrange

def createImgWithPointRand(h,w):
    img = np.ones((h,w),np.float32)
    randY,randX = randrange(h),randrange(w)
    img[randY,randX] = 0
    return img
def moveRaquette(heightImg,widthImg,yStart, yEnd,xStart,xEnd,sense):
    pas = 10
    #move la raquette to right
    if sense == 1 and xEnd + pas < widthImg :
          img[yStart: yEnd, xStart:xEnd] = 1
          xStart = xStart + pas
          xEnd = xEnd + pas
          img[yStart: yEnd, xStart:xEnd] = 0
         
         
    #move la raquette to left
    if sense == 2 and xStart - pas > 0:
          img[yStart: yEnd, xStart:xEnd] = 1
          xStart = xStart - pas
          xEnd = xEnd - pas
          img[yStart: yEnd, xStart:xEnd] = 0
          
    #move la raquette to top
    if sense == 3 and yStart - pas >0:
          img[yStart: yEnd, xStart:xEnd] = 1
          yStart = yStart - pas
          yEnd = yEnd - pas
          img[yStart: yEnd, xStart:xEnd] = 0
         
    #move la raquette to down
    if sense == 4 and yEnd + pas < heightImg:
          img[yStart: yEnd, xStart:xEnd] = 1
          yStart = yStart + pas
          yEnd = yEnd + pas
          img[yStart: yEnd, xStart:xEnd] = 0
    
    return img, yStart, yEnd,xStart,xEnd

#position initiale de la raquette
heightImg, widthImg = 400, 600
img = createImgWithPointRand(heightImg, widthImg)
(cX, cY) = (widthImg // 2, heightImg // 2)
yStart = 180
yEnd = cY
xStart = cX - 50
xEnd = cX+50 
img[yStart: yEnd, xStart:xEnd] = 0




#####################################################################################################
def nothing(x):
    pass

# redlower(HueLower,SaturationLower,ValueLower)
#redlower = (157, 93,203)# low scale of red color value
#redupper = (179,255,255)# high scale of red color value
cv2.namedWindow("HSV Value", cv2.WINDOW_AUTOSIZE)
cv2.createTrackbar("H MIN", "HSV Value", 0, 179, nothing)
cv2.createTrackbar("S MIN", "HSV Value", 0, 255, nothing)
cv2.createTrackbar("V MIN", "HSV Value", 0, 255, nothing)
cv2.createTrackbar("H MAX", "HSV Value", 179, 179, nothing)
cv2.createTrackbar("S MAX", "HSV Value", 255, 255, nothing)
cv2.createTrackbar("V MAX", "HSV Value", 255, 255, nothing)
camera=cv2.VideoCapture(0)
while True:
    (grabbed, frame)=camera.read()
    frame=imutils.resize(frame,width=600)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    h_min = cv2.getTrackbarPos("H MIN", "HSV Value")
    s_min = cv2.getTrackbarPos("S MIN", "HSV Value")
    v_min = cv2.getTrackbarPos("V MIN", "HSV Value")
    h_max = cv2.getTrackbarPos("H MAX", "HSV Value")
    s_max = cv2.getTrackbarPos("S MAX", "HSV Value")
    v_max = cv2.getTrackbarPos("V MAX", "HSV Value")
    redlower = (157, 93,203)
    redupper = (179,255,255)


    
    blur=cv2.GaussianBlur(frame,(11,11),0)
    hsv = cv2.cvtColor(blur,cv2.COLOR_BGR2HSV)#converting image color to hsv and storing the value
    mask=cv2.inRange(hsv,redlower,redupper)#comapring hsv value of image with the other parameters
    mask=cv2.erode(mask,None,iterations=2)# this filter is used to remove noise in the image
    mask=cv2.dilate(mask,None,iterations=2)#this filter is used to remove noise in the image
    cnts=cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
    center=None
    if len(cnts) > 0:
        c=max(cnts, key=cv2.contourArea)# find maximum contour area
        ((x,y),radius)=cv2.minEnclosingCircle(c)# used to create an minimum enclosing circle around the object absed on the coordinates ,radius
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
                    img, yStart, yEnd,xStart,xEnd = moveRaquette(heightImg,widthImg,yStart, yEnd,xStart,xEnd,1) 
                elif(center[0]<300):
                    print("left")
                    img, yStart, yEnd,xStart,xEnd = moveRaquette(heightImg,widthImg,yStart, yEnd,xStart,xEnd,2)
                if(center[1]<300):
                    print("Top")
                    img, yStart, yEnd,xStart,xEnd = moveRaquette(heightImg,widthImg,yStart, yEnd,xStart,xEnd,3) 
                elif(center[1]>300):
                    print("Down")
                    img, yStart, yEnd,xStart,xEnd = moveRaquette(heightImg,widthImg,yStart, yEnd,xStart,xEnd,4)
                    
               
                else:
                    print("stop")
    cv2.imshow("Frame",frame)
    cv2.imshow("Image",img)
    key=cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
camera.release()
cv2.destroyAllWindows()