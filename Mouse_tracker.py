import cv2
import mediapipe as mp
import time
import numpy as np
import HandTrackingModule as htm
import pyautogui as pag

pag.FAILSAFE = False

wScr, hScr=pag.size()
print(wScr, hScr)
cap = cv2.VideoCapture(0)

#########################################################
wCam, hCam = 640, 480
frameR  = 100 #Frame Reduction for better mouse control
smoothening = 5
plocX, plocY =0, 0 # Previous location of mouse
clocX, clocY =0, 0 # Current location of mouse
#########################################################

cap.set(3,wCam) # For Width
cap.set(4,hCam)
detector = htm.HandDetect(max_hands=1)

ptime = 0
while True:
    # Steps to create virtual AI mouse
    # 1. find handlandmarkks
    success, frame = cap.read()
    frame = detector.findHands(frame)

    # 2. get the tip of the index and middle fingers
    ldmarks, bbox = detector.findPosition(frame)
    if bbox:
        cv2.rectangle(frame, (bbox[0], bbox[2]), (bbox[1],bbox[3]),(255,0,255) ,2)
    if ldmarks:
        x1,y1= ldmarks[8][1:]
        x2,y2=ldmarks[12][1:]

    # 3. check which fingers are up
    fingerUp = detector.fingerUp()
    indexUp = middleUp = 0
    if fingerUp:
        indexUp = fingerUp[1]
        middleUp = fingerUp[2]
        thumbUp = fingerUp[0]
        # detector.findDistance(8,12,frame)


    # 4. Track only index finger movements
    if indexUp and not middleUp:
        cv2.rectangle(frame, (frameR,frameR), (wCam-frameR, hCam-frameR),(255,100,100) ,3)
        #np.interp(x,(x1,x2),(y1,y2)) is used to find interpolated value at x
        # 5. Convert coordinates
        x3= np.interp(x1,(frameR,wCam-frameR),(0, wScr))
        y3= np.interp(y1,(frameR,hCam-frameR),(0, hScr))
        try:
            # 6. Smoothen Values
            clocX = plocX + (x3-plocX)/smoothening
            clocY = plocY + (y3-plocY)/smoothening
            # 7. move mouse
            cv2.circle(frame, (x1,y1), 10, (0,255,255),-1)
            pag.moveTo(wScr-clocX,clocY)
            plocX, plocY = clocX, clocY
        except:
            pass
    # 8. Clicking mouse when both fingers are up
    if indexUp and middleUp:
        dist = detector.findDistance(8,12,frame)
        if dist<20:
            # 9. find distance b/w fingers
            cv2.circle(frame, ((x1+x2)//2,(y1+y2)//2), 10, (0,255,0),-1)
            # 10. clicks when distance shortens
            print('Left Clicked!!')
            pag.click()
    if indexUp:
        dist2 = detector.findDistance(4,8,frame)
        if dist2<20:
            print('Scrolled Down')
            pag.scroll(-250)
    if fingerUp[1:5]==[1,1,1,0]:
        print('Scrolled Up')
        pag.scroll(250)
    if fingerUp[1:] == [0,1,0,0]:
        print('Terminate command executed!')
        pag.hotkey('alt','f4')


    # Writing algo for fps
    ctime = time.time()
    fps = 1 / (ctime - ptime)
    ptime = ctime
    font = cv2.FONT_HERSHEY_COMPLEX
    cv2.putText(frame, 'FPS : ' + str(int(fps)), (10, 50), font, 2, (110, 0, 100), 2)
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
