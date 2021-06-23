import cv2 as cv 
import hand_tracking as ht 

#list of to do, in no particular order:
#add lines between each point in addition to (or instead of) circles
#check for the hand position to call clear or erase functions instead of drawing
#add slider to adjust gradient for rainbow!

#list of hand tracking landmarks in mediapipe is available here:
#https://google.github.io/mediapipe/images/mobile/hand_landmarks.png

canvasPoints = [] # [point-id, x, y]
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
                nB = pB + dB//((stepsBtwn-counter) + 1)
                nG = pG + dG//((stepsBtwn-counter) + 1)
                nR = pR + dR//((stepsBtwn-counter) + 1)
                newColor = (nB,nG,nR)
                finalColors.append(newColor)
                counter += 1
        pB, pG, pR = color[0], color[1], color[2]
    #print(finalColors)
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
    return

def isUpsideDown(lmList):
    #check if the wrist y position is above the middle fingertip y position
    #openCV orientation starts with y = 0 at the top and the max value is at the bottom
    if lmList[0][2] < lmList[12][2]:
        return True
    else:
        return False

def handPosition(lmList, upsideDown):
    fingerPosArray = [0,0,0,0,0]
    handPos = "default"
    #by default, 0 = closed, 1 = open. if upside down, these are switched except for the thumb at index 0
    #index: thumb, index, middle, ring, pinky
    #note: thumb joint checks x-position instead of y because it bends 
    #inwards towards the palm rather than downwards
    if lmList[4][1] > lmList[3][1]:
        fingerPosArray[0] = 1
    #look, i know this looks better without so many if statements, but its 
    #really less complicated than using loops in python ;)
    if lmList[8][2] < lmList[5][2]:
        fingerPosArray[1] = 1
    if lmList[12][2] < lmList[9][2]:
        fingerPosArray[2] = 1
    if lmList[16][2] < lmList[13][2]:
        fingerPosArray[3] = 1
    if lmList[20][2] < lmList[17][2]:
        fingerPosArray[4] = 1
    counter = 0
    if len(fingerPosArray) != 0:
        while counter < len(fingerPosArray):
            if upsideDown == True:
                break
            if fingerPosArray[counter] == 0:
                break
            elif counter == 4:
                handPos = "high-five"
            counter += 1
        #while counter % 4 < len(fingerPosArray):
            #if fingerPosArray[counter] == 1 and upsideDown == False or fingerPosArray[counter] == 0 and upsideDown == True:
                #break
            #elif counter == 8:
                #return "fist"
    return handPos

def callHandFunct(handPos):
    if handPos == "high-five":
        clear()
    return
    

def eraser():
    return

def main():
    fps = 0
    pTime = 0
    cap = cv.VideoCapture(0)
    detector = ht.handDetector()
    colorCounter = 0
    pHandPos = "default"
    cHandPos = "default"
    #hand position must be seen at least this many times in a row to prevent 
    #false positive identification
    posCountCheck = 5
    posCount = 0
    
    currentColors = getColorValues(basicColors)
    
    while True:
        success, img = cap.read()
        detector.findHands(img, False)

        lmList = detector.findPosition(img)
        if len(lmList) != 0 :
            fingertip = lmList[8]
            cHandPos = handPosition(lmList, isUpsideDown(lmList))
            if cHandPos == pHandPos:
                posCount += 1
            nextColor, colorCounter = rainbow(colorCounter, currentColors)
            canvasPoints.append(newPoint(fingertip[1],fingertip[2],nextColor))
        
        imgResult = img.copy()
        canvasDraw(canvasPoints, imgResult)

        if posCount == posCountCheck:
            #print(cHandPos)
            callHandFunct(cHandPos)
            posCount = 0
        
        pHandPos = cHandPos

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