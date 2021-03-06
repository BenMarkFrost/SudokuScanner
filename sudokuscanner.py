import numpy as np 
import imutils
from imutils.perspective import four_point_transform
from skimage.segmentation import clear_border
import scipy
import cv2
import os
import digitfinder
from io import BytesIO
from PIL import Image
import time
import pandas as pd
import sudokusolver

directory = "speedTestResults/videoScanSpeeds.csv"
df = pd.read_csv(directory, index_col=0)

# count = 0

# From https://stackoverflow.com/questions/5998245/get-current-time-in-milliseconds-in-python
def current_milli_time():
    return round(time.time() * 1000)

lastClassificationTime = 1000
savedOutput = object


# TODO add process on a separate thread that enable an API to check that the server is still running? Is there an easy way to do this with Flask?


def scan(img):

    # return np.zeros(img.shape)

    global savedOutput, lastClassificationTime

    startTime = current_milli_time()

    thresh, gray = digitfinder.calculateThreshold(img)

    border = None

    try: 
        border = digitfinder.findContours(thresh)
    except:
        pass

    if border is None:
        return np.zeros(img.shape)
        # cv2.drawContours(img, [border], -1, (0, 255, 0), 2)
        # cv2.imshow("Bordered", img)
        # cv2.waitKey(0)

    # if (count != 0) and (count % 100 != 0):

    timeSinceClassification = current_milli_time() - lastClassificationTime

    # print(timeSinceClassification)

    if (timeSinceClassification) < 3000:
        combinedDigits = savedOutput
    else:

        # print("Classifying...")

        lastClassificationTime = current_milli_time()

        dimg = digitfinder.dewarp(gray, border)

        # saveImg("Rotation", dimg)

        

        digits = digitfinder.splitByDigits(dimg)[1:]

        # cleanedDigits = digitfinder.cleanDigits(digits)[2:]

        # print("getting here")

        # for i in cleanedDigits:
        #     for digit in i:
        #         cv2.imshow("output", digit)
        #         cv2.waitKey(0)

        # print(cleanedDigits)

        # TODO
        # CNN for number recognition

        toNumbers = digitfinder.classifyDigits(digits)

        # print(len(toNumbers))

        # print(toNumbers)
        # print(toNumbers)
        # returns a 2d array of digits or None in blank spots

        # sudokusolver

        solvedSudoku = sudokusolver.solve(toNumbers)

        # solvedSudoku = None

        isItSudoku = False

        # print("sending to sudoku")
        if solvedSudoku is None:
            # print("No sudoku :(")
            solvedSudoku = toNumbers
        else:
            isItSudoku = True
            # print("sudoku!")
            # print(np.matrix(solvedSudoku))

        # returns solved 2d array of digits or None in blank spots

        # render digits to images
        # returns 2d array of digit images

        (w,h) = dimg.shape
        width = int(h / 9.0)
        renderedDigits = digitfinder.renderDigits(solvedSudoku, width, isItSudoku)

        # then combine them below

        combinedDigits = digitfinder.combineDigits(renderedDigits)

        savedOutput = combinedDigits

    skewedSolution = digitfinder.warp(img, combinedDigits, border)

    outputImage = digitfinder.combineBorderAndImg(border, skewedSolution)

    endTime = current_milli_time()

    timeTaken = endTime - startTime

    # saveResult(timeTaken)

    return outputImage


def saveResult(timeTaken):

    global df

    row = pd.DataFrame([[timeTaken]], columns=['0'])

    # print(row)

    df = df.append(row, ignore_index=True)

    df = df.astype('int64')
    df.to_csv(directory)




left = cv2.imread("IMG_2511.JPG")
scan(imutils.resize(left, 640))