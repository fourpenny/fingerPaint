#Basic hand tracking using the OpenCV library, based on the tutorial
#by Murtaza's Workshop: https://youtu.be/NZde8Xt78Iw

#to do: implement fps using moving average rather than instantaneous fps

#list of hand tracking landmarks in mediapipe is available here:
#https://google.github.io/mediapipe/images/mobile/hand_landmarks.png

import cv2 as cv 
import mediapipe as mp 
import time

class handDetector():
    def __init__(self, mode=False, maxHands = 2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode 
        self.maxHands = maxHands 
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands,
                                   self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNo=0, draw=False):
        lmList = []

        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                    #print(id, lm)
                    h, w, c = img.shape
                    #if id == 8:
                    cx, cy = int(lm.x*w), int(lm.y*h)
                    lmList.append([id,cx,cy])
                    if draw:
                        cv.circle(img, (cx,cy), 10, (255,0,255), cv.FILLED)
        return lmList

def framesPerSecond(past):
    current = time.time()
    fps = 1/(current-past)
    past = current
    return past, fps

def main():
    pTime = 0 
    cap = cv.VideoCapture(0)
    detector = handDetector()

    while True:
        success, img = cap.read()
        img = detector.findHands(img)

        lmList = detector.findPosition(img)
        if len(lmList) != 0 :
            print(lmList)
            
        pTime, fps = framesPerSecond(pTime)       

        cv.putText(img, str(int(fps)), (10,70), cv.FONT_HERSHEY_PLAIN, 
                3, (255,0,255), 3)

        cv.imshow("Webcam", img)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

if __name__ == '__main__':
    main()