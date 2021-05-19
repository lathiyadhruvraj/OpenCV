import cv2
import numpy as np
frameWidth = 1080
frameLength = 720
cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameLength)
cap.set(10, 150)
myColors = [[172, 167, 46, 179, 255, 255],
            [83, 148, 89, 160, 255, 255],
            [48, 96, 56, 84, 255, 255]]  # Cap detection pink green blue


myColorValues = [[123, 3, 252], [255, 216, 179], [163, 255, 137]]  # paint colors

myPoints = []


def findColor(img, myColors, myColorValues):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    count = 0
    newPoints = []
    for color in myColors:
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mask = cv2.inRange(imgHSV, lower, upper)
        x, y = getcontours(mask)
        cv2.circle(imgResult, (x, y), 6, myColorValues[count], cv2.FILLED)

        if x != 0 and y != 0:
            newPoints.append([x, y, count])
            print(count)
        count += 1
        # cv2.imshow(str(color[0]), mask)
    return newPoints


def getcontours(img):
    contours, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    # print(contours, hierarchy)
    x, y, w, h = 0, 0, 0, 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 200:
            # cv2.drawContours(imgResult, cnt, -1, (255, 255, 255), 3)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.08*peri, True)
            x, y, w, h = cv2.boundingRect(approx)

    return x+w//2, y


def drawOnCanvas(myPoints, myColorValues):
    for point in myPoints:
        cv2.circle(imgResult, (point[0], point[1]), 10, myColorValues[point[2]], cv2.FILLED)


while True:
    success, img = cap.read()  # success is a boolean whether it is done or not
    img = cv2.flip(img, 1)
    imgResult = img.copy()
    newPoints = findColor(imgResult, myColors, myColorValues)

    if len(newPoints) != 0:
        for newP in newPoints:
            myPoints.append(newP)

    if len(myPoints) != 0:
        drawOnCanvas(myPoints, myColorValues)

    cv2.imshow("Result", imgResult)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
