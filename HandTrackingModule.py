import math

import cv2
import mediapipe as mp
import time
# cap = cv2.VideoCapture(0)
#
# mpHands = mp.solutions.hands
#
# # it only uses RGB images
# hands = mpHands.Hands()
# mpDraw = mp.solutions.drawing_utils
#
# ptime=0
#
# while True:
#     success, frame = cap.read()
#     rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#     result = hands.process(rgb_frame)
#     # View the image in media folder to check different hand landmarksq
#     # print('result---->',result.multi_hand_landmarks)
#     if result.multi_hand_landmarks :
#         for ldmrks in result.multi_hand_landmarks:
#
#             # enumerate() functions assigns index number also along with the items i.e from what index no it is fetched
#             # Each id has a corresponding hand landmark
#             for id, lm in enumerate(ldmrks.landmark):
#                 # Here lm is the ratio not the position
#                 print(id,lm)
#
#                 h, w, c =frame.shape
#                 cx, cy = int(lm.x*w), int(lm.y*h)
#                 # This way a spcific landmark can be addressed
#                 if id==20:
#                     cv2.putText(frame, 'pinky finger tip', (cx+10, cy+10 ), font, 1, (110, 0, 100), 1)
#             # Using Inbuilt mediapipe peoperties to draw pts at different hand landmarks
#             mpDraw.draw_landmarks(frame, ldmrks, mpHands.HAND_CONNECTIONS)
#
#     # Writing algo for fps
#     ctime = time.time()
#     fps = 1/(ctime-ptime)
#     ptime = ctime
#     font = cv2.FONT_HERSHEY_COMPLEX
#     cv2.putText(frame,'FPS : '+ str(int(fps)), (10,50), font, 2, (110,0,100), 2)
#
#     cv2.imshow('frame', frame)
#     if cv2.waitKey(1) == ord('q'):
#         break
#
# cap.release()
# cv2.destroyAllWindows()

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
            return 0

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


'''The purpose of writing if __name__ == "__main__": in a Python module is to ensure that certain code only runs when the module is executed as the main program and not when it is imported as a module in another script.

Detailed Explanation
__name__ Variable
Every Python module has a special built-in variable called __name__.
When a module is run directly, __name__ is set to "__main__".
When a module is imported into another module, __name__ is set to the module's name.
'''
if __name__=="__main__":
    main()