import numpy as np 
import imutils
from imutils.perspective import four_point_transform
from skimage.segmentation import clear_border
import scipy
import cv2
import os
# import tensorflow as tf

def combineBorderAndImg(border, img):
    # Convert border coordinates to image

    border = np.array(border, np.int32)
    border = border.reshape((-1,1,2))

    (w,h,d) = img.shape

    background = np.zeros((w, h, d))

    borderImg = cv2.polylines(background, [border], True, (0,0,255))

    outputImage = cv2.add(np.float32(background), np.float32(img))
    return outputImage

def splitByDigits(img):
    digits = [[]]

    (w,h) = img.shape

    interval = h / 9

    for j in range(9):
        row = []
        start = j * interval
        for i in range(9):
            end = i * interval
            points = np.array([(end, start), (end, start+interval), (end+interval, start), (end+interval, start+interval)]).reshape(4,2)
            # print(points)
            digit = four_point_transform(img, np.rint(points))
            row.append(digit)
            # digit = tempRow[start : start + interval]
        digits.append(row)
    return digits

def cleanDigits(digits):
    
    cleanedDigits = [[]]

    for row in digits:

        tempRow = []
        for img in row:

            threshold = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

            cleaned = clear_border(threshold)

            contours = cv2.findContours(cleaned, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            contours = imutils.grab_contours(contours)

            if len(contours) == 0:
                tempRow.append(np.zeros(cleaned.shape))
                continue

            biggestContour = max(contours, key = cv2.contourArea)

            contourMask = np.zeros(img.shape, dtype="uint8")
            cv2.drawContours(contourMask, [biggestContour], -1, 255, -1)

            numFilled = cv2.countNonZero(contourMask)
            total = img.shape[0] * img.shape[1]
            percentageFilled = numFilled * 100 / total

            if percentageFilled < 1:
                tempRow.append(np.zeros(cleaned.shape))
                continue
            else:
                cleaned = cv2.bitwise_and(cleaned, cleaned, mask=contourMask)
                tempRow.append(cleaned)

        cleanedDigits.append(tempRow)
    
    return cleanedDigits
    
    # saveImg("Digits", cleaned)

def dewarp(img, border):
    dewarp = four_point_transform(img, border.reshape(4,2))

    size = 300

    dewarp = cv2.resize(dewarp, (size, size))

    # cv2.imshow("deskewed", puzzle)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return dewarp

def warp(img, toWarp, border):

    rows,cols,ch = img.shape

    (w,h,d) = toWarp.shape

    # Border coordinates are sent in a weird order, reordering
    border = [border[0][0], border[3][0], border[1][0], border[2][0]]

    pts1 = np.float32([[0,0], [w,0], [0,h], [w,h]])
    pts2 = np.float32(border)

    M = cv2.getPerspectiveTransform(pts1,pts2)
    dst = cv2.warpPerspective(toWarp,M,(cols,rows))

    # overlay = cv2.add(img, dst)

    return dst


def classifyDigits(digits):

    for row in digits:
        for digit in row:
            digit = cv2.resize(digit, (28,28))

            


def combineDigits(digits):
    rows = []
    # concatVert = np.zeros((33,33))
    for row in digits:
        concatHori = np.concatenate(row, axis=1)
        rows.append(concatHori)

    return np.concatenate(rows, axis=0)

def calculateThreshold(img):

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5,5), 0)

    threshold = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 9, 2)

    return threshold, gray

def findContours(img):

    # Research different options for parameters here
    contours = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    contours = imutils.grab_contours(contours)

    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    biggestContour = None

    if (cv2.contourArea(contours[0]) < 100000): return None

    for c in contours:

        perimeter = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.01 * perimeter, True)

        if len(approx) == 4:
            biggestContour = approx
            break

    # print(cv2.contourArea(biggestContour))

    return biggestContour