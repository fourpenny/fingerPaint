import cv2 as cv 
import hand_tracking as ht 

canvasPoints = [] # [point-id, x, y]
pointColors = []
#list of colors for rainbow:
#red rgb(255,0,0)
#orange rgb(255,128,0)
#yellow rgb(255,255,0)
#green rgb(0,255,0)
#blue rgb(0,0,255)
#indigo rgb(111,0,255)
#violet rgb(128,0,255)
#remember: opencv uses bgr colors by default!
colors = [(0,0,255),(0,128,255),(0,255,255),(0,255,0),(255,0,0),(255,0,111),
          (255,0,128)]

#returns a color value by tweening between color values in a predefined list
def rainbow(counter):
    color = colors[counter % len(colors)]
    counter += 1
    return color, counter

#to do: add lines between each point in addition to (or instead of) circles
def canvasDraw(points, img, colors):
    for point in points:
        i = points.index(point)
        cv.circle(img, (point[1], point[2]), 10, colors[i], cv.FILLED)
    return

def clear():
    canvasPoints.clear()
    print(canvasPoints)
    return

def eraser():
    return

def main():
    fps = 0
    pTime = 0
    cap = cv.VideoCapture(0)
    detector = ht.handDetector()
    colorCounter = 0
    
    while True:
        success, img = cap.read()
        detector.findHands(img, False)

        lmList = detector.findPosition(img)
        if len(lmList) != 0 :
            fingertip = lmList[8]
            canvasPoints.append(fingertip) 
            nextColor, colorCounter = rainbow(colorCounter)
            pointColors.append(nextColor)
            
        imgResult = img.copy()
        canvasDraw(canvasPoints, imgResult, pointColors)

        pTime, fps = ht.framesPerSecond(pTime)

        cv.putText(imgResult, str(int(fps)), (10,70), cv.FONT_HERSHEY_PLAIN, 
                3, (255,0,255), 3)

        cv.imshow("Webcam", imgResult)
        
        #keyboard commands
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
        
        if cv.waitKey(1) & 0xFF == ord('c'):
            clear()

if __name__ == '__main__':
    main()