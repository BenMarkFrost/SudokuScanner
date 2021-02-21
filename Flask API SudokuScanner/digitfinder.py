import numpy as np 
import imutils
from imutils.perspective import four_point_transform
from skimage.segmentation import clear_border
import scipy
import cv2
import time
import os
# os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
os.environ['TF_FORCE_GPU_ALLOW_GROWTH'] = 'true'

# import tensorflow as tf
from tensorflow import keras

model = keras.models.load_model("model/digitModel3.h5")

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
        start = int(j * interval)
        for i in range(9):
            end = int(i * interval)
            
            x1 = end
            y1 = start
            x2 = end + int(interval)
            y2 = start + int(interval)

            # print(y1, y2, x1, x2)

            # TODO move reshaping here
            digit = img[y1:y2, x1:x2]

            row.append(digit)
            # digit = tempRow[start : start + interval]
        digits.append(row)
    return digits

def cleanDigits(digits):
    
    cleanedDigits = [[]]

    for row in digits:

        tempRow = []
        for img in row:

            # Document how I adjusted the threshold to make it work for digits

            #Different types of filtering
            blurred = cv2.GaussianBlur(img, (7,7), 0)
            # blurred = cv2.bilateralFilter(img, 9, 75, 75)

            threshold = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 9, 2)

            # threshold = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

            cleaned = clear_border(threshold)

            contours = cv2.findContours(cleaned, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            contours = imutils.grab_contours(contours)

            if len(contours) == 0:
                tempRow.append(None)
                continue

            biggestContour = max(contours, key = cv2.contourArea)

            contourMask = np.zeros(img.shape, dtype="uint8")
            cv2.drawContours(contourMask, [biggestContour], -1, 255, -1)

            numFilled = cv2.countNonZero(contourMask)
            total = img.shape[0] * img.shape[1]
            percentageFilled = numFilled * 100 / total

            if percentageFilled < 3:
                tempRow.append(None)
                continue
            else:
                cleaned = cv2.bitwise_and(cleaned, cleaned, mask=contourMask)
                cleaned = np.rint(cleaned / 255).astype(int)
                tempRow.append(cleaned)
                # saveImg("Digits", cleaned)

        cleanedDigits.append(tempRow)
    
    return cleanedDigits
    
    # saveImg("Digits", cleaned)

def saveImg(folder, img):
    num = 0
    directory = "cache/"
    while True:
        try:
            f = open(directory + folder + "/" + folder + str(num) + ".jpg", 'r')
            f.close()
            num = num + 1
        except:
            break

    cv2.imwrite(directory + folder + "/" + folder + str(num) + ".jpg", img)
    num = num + 1

def dewarp(img, border):

    dewarp = four_point_transform(img, border)

    size = 300

    dewarp = cv2.resize(dewarp, (size, size))

    # cv2.imshow("deskewed", puzzle)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    return dewarp

def warp(img, toWarp, border):

    rows,cols,ch = img.shape

    (w,h,d) = toWarp.shape

    # print(border)

    # Border coordinates are sent in a weird order, reordering
    border = [border[0], border[3], border[1], border[2]]

    # print(border)

    if (border[1][1] > border[2][1]):
        border = [border[2], border[0], border[3], border[1]]
    
    # print(border)

    pts1 = np.float32([[0,0], [w,0], [0,h], [w,h]])
    pts2 = np.float32(border)

    M = cv2.getPerspectiveTransform(pts1,pts2)
    dst = cv2.warpPerspective(toWarp,M,(cols,rows))

    # overlay = cv2.add(img, dst)

    return dst


def renderDigits(digits, width):

    rendered = []

    for row in digits:
        tempRow = []
        for digit in row:
            bg = renderIndividualDigit(digit, width)
            tempRow.append(bg)
        rendered.append(tempRow)
    
    return rendered
            

def renderIndividualDigit(digit, width):
    bg = np.zeros((width, width, 3))
    if digit is not None:
        bg = cv2.putText(bg, str(digit), (6,25), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)
    
    # cv2.imshow("bg", bg)
    # cv2.waitKey(0)

    return bg

def classifyDigits(digits):
    # TODO find a faster CNN
    # Hyperthread this method?

    global model

    resizedDigits = []

    for row in digits:
        for digit in row:
            if digit is not None:
                digit = np.uint8(digit)
                # print(digit.shape)
                # cv2.imshow("digit", digit*255)
                # cv2.waitKey(0)
                digit = cv2.resize(digit, (28,28))
                digit = digit.reshape(1,28,28,1)
                resizedDigits.append(digit)

    if len(resizedDigits) > 0:
        results = model.predict(np.vstack(resizedDigits))

        res = []

        for result in results:
            res.append(np.argmax(result))

    # print(results)

    toNumbers = []

    for row in digits:
        tempRow = []
        for digit in row:
            if digit is not None:
                tempRow.append(res[0])
                res = res[1:]
            else:
                tempRow.append(None)
        toNumbers.append(tempRow)

    # print(toNumbers)

    # for row in digits:
    #     tempRow = []
    #     for digit in row:
    #         if digit is None:
    #             tempRow.append(None)
    #             continue
    #         else:
    #             digit = cv2.resize(digit, (28,28))
    #             # cv2.imshow("resized", digit)
    #             # cv2.waitKey(0)

    #             result = np.argmax(model.predict(digit))
    #             result = 0

    #             # print("Time per image classification: " + str(timeTaken))

    #             tempRow.append(result)
    #             # print(result)
    #     toNumbers.append(tempRow)

    return toNumbers

# From https://stackoverflow.com/questions/5998245/get-current-time-in-milliseconds-in-python
def current_milli_time():
    return round(time.time() * 1000)


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

    if (cv2.contourArea(contours[0]) < 25000): return None

    for c in contours:

        perimeter = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.01 * perimeter, True)

        if len(approx) == 4:
            biggestContour = approx
            break

    # print(cv2.contourArea(biggestContour))

    return biggestContour.reshape(4,2)