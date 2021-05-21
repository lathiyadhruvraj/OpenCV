import cv2
import numpy as np

frameWidth = 1080
frameLength = 640


def preprocessing(frame):
    grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurFrame = cv2.GaussianBlur(grayFrame, (5, 5), 1)
    cannyFrame = cv2.Canny(blurFrame, 150, 150)
    kernel = np.ones((5, 5))
    dialationFrame = cv2.dilate(cannyFrame, kernel, iterations=2)
    thresholdFrame = cv2.erode(dialationFrame, kernel, iterations=1)

    return thresholdFrame


def getcontours(img):
    biggest = np.array([])
    maxArea = 0
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv2.contourArea(cnt)

        if area > 9000:
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.03*peri, True)
            print(len(approx))
            print(approx)
            if area > maxArea and len(approx) == 4:
                biggest = approx
                maxArea = area

    cv2.drawContours(imgCountour, biggest, -1, (255, 0, 0), 9)

    return biggest


def reorder(pts):
    pts = pts.reshape((4, 2))
    newpts = np.zeros((4, 1, 2), np.int32)

    add = pts.sum(axis=1)

    newpts[0] = pts[np.argmin(add)]
    newpts[3] = pts[np.argmax(add)]

    diff = np.diff(pts, axis=1)

    newpts[1] = pts[np.argmin(diff)]
    newpts[2] = pts[np.argmax(diff)]

    return newpts


def getWarp(frame, biggest):
    biggest = reorder(biggest)

    pts1 = np.float32(biggest)
    pts2 = np.float32([[0, 0], [frameWidth, 0], [0, frameLength], [frameWidth, frameLength]])

    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    imgOutput = cv2.warpPerspective(frame, matrix, (frameWidth, frameLength))

    imgCropped = imgOutput[20:imgOutput.shape[0]-20, 20:imgOutput.shape[1]-20]
    return imgCropped


##############################################################################################
#                       DOCUMENTS IN .jpg/.png format                                        #
##############################################################################################

frame = cv2.imread("document.jpg")
# frame = cv2.imread("doc1.jpg")
imgCountour = frame.copy()

thresFrame = preprocessing(frame)
biggest = getcontours(thresFrame)
print(biggest.shape)
if biggest.size != 0:
    frameWrap = getWarp(frame, biggest)
else:
    cv2.imshow("CANT FIND", frame)

cv2.imshow("Doc Scanner", frameWrap)

cv2.waitKey(0)

##############################################################################################
#                       DOCUMENTS GIVEN USING CAMERA                                         #
##############################################################################################
# cap = cv2.VideoCapture(0)
# cap.set(3, frameWidth)
# cap.set(4, frameLength)
# cap.set(10, 130)
#
#
# while True:
#     _, frame = cap.read()
#     frame = cv2.flip(frame, 1)
#     frame = cv2.resize(frame, (frameWidth, frameLength))
#     imgCountour = frame.copy()
#
#     thresFrame = preprocessing(frame)
#     biggest = getcontours(thresFrame)
#
#     print(biggest.shape)
#
#     if biggest.size != 0:
#         cv2.destroyWindow("CANT FIND DOCUMENT")
#         frameWrap = getWarp(frame, biggest)
#         cv2.imshow("DOCUMENT DETECTED", frameWrap)
#
#     else:
#         cv2.destroyWindow("DOCUMENT DETECTED")
#         cv2.imshow("CANT FIND DOCUMENT", frame)
#
#
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
