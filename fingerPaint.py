import cv2 as cv 
import hand_tracking as ht 

#list of to do, in no particular order:
#add lines between each point in addition to (or instead of) circles
#check for the hand position to call clear or erase functions instead of drawing

canvasPoints = [] # [point-id, x, y]
checkLms = []
#list of colors for rainbow: (you can change this list if you desire)
#red rgb(255,0,0)
#orange rgb(255,128,0)
#yellow rgb(255,255,0)
#green rgb(0,255,0)
#blue rgb(0,0,255)
#indigo rgb(111,0,255)
#violet rgb(128,0,255)
#remember: opencv uses bgr colors by default!
basicColors = [(0,0,255),(0,128,255),(0,255,255),(0,255,0),(255,0,0),(255,0,111),
          (255,0,128)]

class newPoint():
    def __init__(self, xPos=0, yPos=0, color=(0,0,0)):
        self.xPos = xPos
        self.yPos = yPos
        self.color = color
        
    def draw(self, img):
        cv.circle(img, (self.xPos, self.yPos), 10, self.color, cv.FILLED)
        return

def getColorValues(baseColors, stepsBtwn=3):
    pB, pG, pR = 0, 0, 0
    finalColors = []
    for color in baseColors:
        if len(finalColors) == 0:
            finalColors.append(color)
        else:
            #check for difference between each value in the tuple, then divide
            #by the number of steps in between to get the difference in color change,
            #finally, add it to the current color value to make a gradual shift
            dB, dG, dR = color[0]-pB, color[1]-pG, color[2]-pR
            counter = 0
            while counter < stepsBtwn:
                print(counter)
                nB = pB + dB//((stepsBtwn-counter) + 1)
                nG = pG + dG//((stepsBtwn-counter) + 1)
                nR = pR + dR//((stepsBtwn-counter) + 1)
                newColor = (nB,nG,nR)
                finalColors.append(newColor)
                counter += 1
        pB, pG, pR = color[0], color[1], color[2]
    print(finalColors)
    return finalColors
    

#returns a color value by tweening between color values in a predefined list
def rainbow(counter, colorList):
    color = colorList[counter % len(colorList)]
    counter += 1
    return color, counter

def canvasDraw(points, img):
    for point in points:
        point.draw(img)
    return

def clear():
    canvasPoints.clear()
    print(canvasPoints)
    return

def handPosition(lmList):
    for lm in lmList:
        #check if fingertip is below joint above and that hand is not turned upside down (wrist above fingertips)
        return #will return a int corresponding to a particular hand position

def eraser():
    return

def main():
    fps = 0
    pTime = 0
    cap = cv.VideoCapture(0)
    detector = ht.handDetector()
    colorCounter = 0
    
    currentColors = getColorValues(basicColors)
    
    while True:
        success, img = cap.read()
        detector.findHands(img, False)

        lmList = detector.findPosition(img)
        if len(lmList) != 0 :
            fingertip = lmList[8]
            nextColor, colorCounter = rainbow(colorCounter, currentColors)
            canvasPoints.append(newPoint(fingertip[1],fingertip[2],nextColor)) 
            
        imgResult = img.copy()
        canvasDraw(canvasPoints, imgResult)

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