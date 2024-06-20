import math

import cv2
import mediapipe as mp
import time

class HandDetect():
    def __init__(self, mode=False,max_hands=2,model_complexity=1,min_detect_con=0.5,min_track_con=0.5):
        self.mode = mode
        self.max_hands = max_hands
        self.model_complexity=model_complexity
        self.min_detect_con=min_detect_con
        self.min_track_con=min_track_con
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode,self.max_hands,self.model_complexity,self.min_detect_con,
                                   self.min_track_con)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self,frame,draw=True):
        self.rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.result = self.hands.process(self.rgb_frame)
        if self.result.multi_hand_landmarks:
            for landmarks in self.result.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(frame, landmarks, self.mpHands.HAND_CONNECTIONS)
        return frame

    def findPosition(self, frame,handId=0, draw=True):
        self.lmList=[]
        xList =[]
        yList =[]
        bbox=[]
        if self.result.multi_hand_landmarks:
            handmark = self.result.multi_hand_landmarks[handId]
            for id, lm in enumerate(handmark.landmark):
                # Here lm is the ratio not the position
                h, w, c =frame.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                xList.append(cx)
                yList.append((cy))
                self.lmList.append([id,cx,cy])
                if draw :
                    cv2.circle(frame, (cx,cy), 6, (255,0,255),-1)
            xmin, xmax= min(xList), max(xList)
            ymin, ymax= min(yList), max(yList)
            bbox = xmin, xmax, ymin, ymax
        return self.lmList, bbox
    def fingerUp(self):
        fingers=[]
        self.tipIds=[4,8,12,16,20]
        if self.lmList:
            if self.lmList[self.tipIds[0]][1] > self.lmList[self.tipIds[0]-2][1]:
                fingers.append(1)
            else:
                fingers.append(0)
            for i in range(1,5):
                if self.lmList[self.tipIds[i]][2] < self.lmList[self.tipIds[i] - 2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)
        return fingers

    def findDistance(self, p1, p2, frame, draw=True, r=10, t=3):
        try:
            x1, y1 = self.lmList[p1][1:]
            x2, y2 = self.lmList[p2][1:]
            cx, cy = (x1+x2)//2, (y1+y2)//2
            if draw:
                cv2.line(frame, (x1,y1), (x2,y2), (255,255,0), t)
                cv2.circle(frame, (x1, y1), r, (255, 0, 255), cv2.FILLED)
                cv2.circle(frame, (x2, y2), r, (255, 0, 255), cv2.FILLED)
                cv2.circle(frame, (cx, cy), r, (0, 0, 255), cv2.FILLED)
            length = math.dist((x1,y1),(x2,y2))
            return length
        except:
            pass

def main():
    cap = cv2.VideoCapture(0)
    detector = HandDetect()
    ptime = 0
    while True:
        success, frame = cap.read()

        frame = detector.findHands(frame)
        handsPos = detector.findPosition(frame)

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
    
if __name__=="__main__":
    main()
