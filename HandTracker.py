import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands

# it only uses RGB images
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

ptime=0

while True:
    success, frame = cap.read()
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)
    # View the image in media folder to check different hand landmarksq
    # print('result---->',result.multi_hand_landmarks)
    if result.multi_hand_landmarks :
        for ldmrks in result.multi_hand_landmarks:

            # enumerate() functions assigns index number also along with the items i.e from what index no it is fetched
            # Each id has a corresponding hand landmark
            for id, lm in enumerate(ldmrks.landmark):
                # Here lm is the ratio not the position
                print(id,lm)

                h, w, c =frame.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                # This way a spcific landmark can be addressed
                if id==20:
                    cv2.putText(frame, 'pinky finger tip', (cx+10, cy+10 ), font, 1, (110, 0, 100), 1)
            # Using Inbuilt mediapipe peoperties to draw pts at different hand landmarks
            mpDraw.draw_landmarks(frame, ldmrks, mpHands.HAND_CONNECTIONS)

    # Writing algo for fps
    ctime = time.time()
    fps = 1/(ctime-ptime)
    ptime = ctime
    font = cv2.FONT_HERSHEY_COMPLEX
    cv2.putText(frame,'FPS : '+ str(int(fps)), (10,50), font, 2, (110,0,100), 2)

    cv2.imshow('frame', frame)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
