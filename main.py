import cv2
import numpy as np
import utlis

import urllib.request
 
from urllib.request import urlopen
import os
import datetime
import time
import sys

# replace ip

url="" 

def sendRequest(url):
    a=urllib.request.urlopen(url)

 
curveList = []
avgVal=10
 
def getLaneCurve(img,display=2):
 
    imgCopy = img.copy()
    imgResult = img.copy()
    #### STEP 1
    imgThres = utlis.thresholding(img)
 
    #### STEP 2
    hT, wT, c = img.shape
    points = utlis.valTrackbars()
    imgWarp = utlis.warpImg(imgThres,points,wT,hT)
    imgWarpPoints = utlis.drawPoints(imgCopy,points)
 
    #### STEP 3
    middlePoint,imgHist = utlis.getHistogram(imgWarp,display=True,minPer=0.5,region=4)
    curveAveragePoint, imgHist = utlis.getHistogram(imgWarp, display=True, minPer=0.9)
    curveRaw = curveAveragePoint - middlePoint
 
    #### SETP 4
    curveList.append(curveRaw)
    if len(curveList)>avgVal:
        curveList.pop(0)
    curve = int(sum(curveList)/len(curveList))
 
    #### STEP 5
    if display != 0:
        imgInvWarp = utlis.warpImg(imgWarp, points, wT, hT, inv=True)
        imgInvWarp = cv2.cvtColor(imgInvWarp, cv2.COLOR_GRAY2BGR)
        imgInvWarp[0:hT // 3, 0:wT] = 0, 0, 0
        imgLaneColor = np.zeros_like(img)
        imgLaneColor[:] = 0, 255, 0
        imgLaneColor = cv2.bitwise_and(imgInvWarp, imgLaneColor)
        imgResult = cv2.addWeighted(imgResult, 1, imgLaneColor, 1, 0)
        midY = 450
        cv2.putText(imgResult, str(curve), (wT // 2 - 80, 85), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 255), 3)
        cv2.line(imgResult, (wT // 2, midY), (wT // 2 + (curve * 3), midY), (255, 0, 255), 5)
        cv2.line(imgResult, ((wT // 2 + (curve * 3)), midY - 25), (wT // 2 + (curve * 3), midY + 25), (0, 255, 0), 5)
        for x in range(-30, 30):
            w = wT // 20
            cv2.line(imgResult, (w * x + int(curve // 50), midY - 10),
                     (w * x + int(curve // 50), midY + 10), (0, 0, 255), 2)
    if display == 2:
        imgStacked = utlis.stackImages(0.7, ([img, imgWarpPoints, imgWarp],
                                             [imgHist, imgLaneColor, imgResult]))
        cv2.imshow('ImageStack', imgStacked)
    elif display == 1:
        cv2.imshow('Resutlt', imgResult)
 
    curve = curve/100
    if curve>1: curve ==1
    if curve<-1:curve == -1
 
    return curve
 
 
if __name__ == '__main__':
    urlc= url+":81/stream"
    CAMERA_BUFFRER_SIZE=4096
    stream=urlopen(urlc)
    bts=b''
    i=0
 
    intialTrackBarVals = [102, 80, 20, 214 ]
    utlis.initializeTrackbars(intialTrackBarVals)
    frameCounter = 0
    while True:
        bts+=stream.read(CAMERA_BUFFRER_SIZE)
        jpghead=bts.find(b'\xff\xd8')
        jpgend=bts.find(b'\xff\xd9')
        if jpghead>-1 and jpgend>-1:
            jpg=bts[jpghead:jpgend+2]
            bts=bts[jpgend+2:]
            img=cv2.imdecode(np.frombuffer(jpg,dtype=np.uint8),cv2.IMREAD_UNCHANGED)
 
 
            img = cv2.resize(img,(480,240))
            curve = getLaneCurve(img,display=2)
            point=curve
            print(point)
            sendRequest(url+"/action?go=lighton")
            if point > -0.10 and point < 0.10:
                print("forward")
                 
                # sendRequest(url+"/action?go=forward")
                time.sleep(0.5)
                sendRequest(url+"/action?go=stop")
                time.sleep(4)
            elif(point < -0.10 and point >-0.60):
                print("left")
               
                # sendRequest(url+"/action?go=left")
                sendRequest(url+"/action?go=stop")
            elif(point > 0.10 and point < 0.60):
                print("right")
                
                # sendRequest(url+"/action?go=right")
                sendRequest(url+"/action?go=stop")
            else:
                print("sop")
                sendRequest(url+"/action?go=stop")

                
           
        
            
             


        cv2.waitKey(1)
        #cv2.imshow('Vid',img)
        
    cv.destroyAllWindows()