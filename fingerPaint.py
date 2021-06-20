import cv2 as cv 
import mediapipe as mp 
import time
import hand_tracking as ht 

canvasPoints = [] # [point-id, x, y]

def rainbow():
    return (255,0,0)

def canvasDraw(points, img):
    for point in points:
        cv.circle(img, (point[1], point[2]), 10, rainbow(), cv.FILLED)
    return

def clear():
    canvasPoints.clear()
    print(canvasPoints)
    return

def eraser():
    return

def framesPerSecond(past):
    current = time.time()
    fps = 1/(current-past)
    past = current
    return past, fps

def main():
    fps = 0
    pTime = 0
    cap = cv.VideoCapture(0)
    detector = ht.handDetector()
    
    while True:
        success, img = cap.read()
        img = detector.findHands(img)

        lmList = detector.findPosition(img)
        if len(lmList) != 0 :
            fingertip = lmList[8]
            canvasPoints.append(fingertip)
            
        imgResult = img.copy()
        canvasDraw(canvasPoints, imgResult)

        pTime, fps = framesPerSecond(pTime)

        cv.putText(imgResult, str(int(fps)), (10,70), cv.FONT_HERSHEY_PLAIN, 
                3, (255,0,255), 3)

        cv.imshow("Webcam", imgResult)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
        
        if cv.waitKey(1) & 0xFF == ord('c'):
            clear()

if __name__ == '__main__':
    main()