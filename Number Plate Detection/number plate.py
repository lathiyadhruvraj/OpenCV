import cv2

num_plate = cv2.CascadeClassifier("haarcascade_russian_plate_number.xml")
frameWidth = 480
frameLength = 640
min_area = 1500
count = 0

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

cap.set(10, 100)

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    numberPlates = num_plate.detectMultiScale(imgGray, 1.1, 4)
    for (x, y, w, h) in numberPlates:
        area = w*h
        if area > min_area:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.putText(img, "Number Plate", (x, y-5),
                        cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 250), 2)
            img_roi = img[y:y+h, x:x+w]
            cv2.imshow("ROI", img_roi)
        else:
            cv2.destroyWindow("ROI")

    cv2.imshow("Finding Number Plate....", img)

    if cv2.waitKey(1) & 0xFF == ord('s'):
        cv2.imwrite("Number Plate Detection/Scanned/NoPlate_"+str(count)+".jpg", img_roi)
        cv2.rectangle(img, (0, 200), (640, 300), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, "Scan Saved", (150, 265), cv2.FONT_HERSHEY_SIMPLEX,
                    2, (0, 0, 255), 2)
        cv2.imshow("Finding Number Plate....", img)
        cv2.waitKey(500)
        count += 1
