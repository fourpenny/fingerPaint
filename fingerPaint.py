import cv2 as cv 
import mediapipe as mp 
import time
import hand_tracking as ht 

pTime = 0 
cTime = 0 
cap = cv.VideoCapture(0)
detector = ht.handDetector()

def rainbow():
    return

def fingerPaint():
    return

def clear():
    return

def eraser():
    return

def main():
    pTime = 0 
    cTime = 0 
    cap = cv.VideoCapture(0)
    detector = ht.handDetector()

    while True:
        success, img = cap.read()
        img = detector.findHands(img)

        lmList = detector.findPosition(img)
        if len(lmList) != 0 :
            print(lmList[8])

        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime        

        cv.putText(img, str(int(fps)), (10,70), cv.FONT_HERSHEY_PLAIN, 
                3, (255,0,255), 3)

        cv.imshow("Webcam", img)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

if __name__ == '__main__':
    main()