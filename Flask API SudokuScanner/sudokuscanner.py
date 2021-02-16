import numpy as np 
import imutils
import cv2
import os

def scan(img):

    img = np.array(img)

    thresh = calculateThreshold(img)

    border = None

    try: 
        border = findContours(thresh).tolist()
    except:
        pass

    if border is None:
        border = [[0, 0], [0, 0], [0, 0], [0, 0]]
        # cv2.drawContours(img, [border], -1, (0, 255, 0), 2)
        # cv2.imshow("Bordered", img)
        # cv2.waitKey(0)

    print(border)

    return border
    

num = 0

def calculateThreshold(img):

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5,5), 0)

    threshold = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 9, 2)
    # threshold = cv2.bitwise_not(threshold)

    # global num

    # directory = "cache/"
    # filename = "thresholded"

    # while True:
    #     try:
    #         f = open(directory + filename + str(num) + ".jpg", 'r')
    #         f.close()
    #         num = num + 1
    #     except:
    #         break

    # cv2.imwrite("cache/thresholded" + str(num) + ".jpg", threshold)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    return threshold

def findContours(img):

    # Research different options for parameters here
    contours = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    contours = imutils.grab_contours(contours)

    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    biggestContour = None

    if (cv2.contourArea(contours[0]) < 10000): return None

    for c in contours:

        perimeter = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.01 * perimeter, True)

        if len(approx) == 4:
            biggestContour = approx
            break

    # print(biggestContour)

    return biggestContour



# scan(imutils.resize(cv2.imread("IMG_2489.JPG"), 640))