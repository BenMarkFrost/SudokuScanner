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

clientsDict = {}


# TODO add process on a separate thread that enable an API to check that the server is still running? Is there an easy way to do this with Flask?

def scan(img, browser_id):

    # print(browser_id)
    # cv2.imshow("img", img)
    # cv2.waitKey(0)

    startTime = current_milli_time()

    thresh, gray = digitfinder.calculateThreshold(img)

    border = None

    try: 
        border = digitfinder.findContours(thresh)
    except:
        pass

    if border is None:
        return np.zeros(img.shape)

    combinedDigits = manageClients(gray, border, browser_id)

    skewedSolution = digitfinder.warp(img, combinedDigits, border)

    outputImage = digitfinder.combineBorderAndImg(border, skewedSolution)

    endTime = current_milli_time()

    timeTaken = endTime - startTime

    # saveResult(timeTaken)

    return outputImage


def manageClients(gray, border, browser_id):
    global clientsDict

    if browser_id not in clientsDict:
        combinedDigits = findSudoku(gray, border)
        clientsDict[browser_id] = (current_milli_time(), combinedDigits)
        print("New client: " + str(browser_id))
    else:
        lastClassificationTime, savedOutput = clientsDict[browser_id]
        timeSinceClassification = current_milli_time() - lastClassificationTime

        if (timeSinceClassification) < 3000:
            combinedDigits = savedOutput
        else:
            combinedDigits = findSudoku(gray, border)
            clientsDict[browser_id] = (current_milli_time(), combinedDigits)
    
    return combinedDigits


def findSudoku(gray, border):
    
    dimg = digitfinder.dewarp(gray, border)

    digits = digitfinder.splitByDigits(dimg)[1:]

    toNumbers = digitfinder.classifyDigits(digits)

    solvedSudoku = sudokusolver.solve(toNumbers)

    isItSudoku = False

    # print("sending to sudoku")
    if solvedSudoku is None:
        # print("No sudoku :(")
        solvedSudoku = toNumbers
    else:
        isItSudoku = True
        solvedSudoku = np.subtract(solvedSudoku, toNumbers)

    (w,h) = dimg.shape
    width = int(h / 9.0)
    renderedDigits = digitfinder.renderDigits(solvedSudoku, width, isItSudoku)

    combinedDigits = digitfinder.combineDigits(renderedDigits)

    return combinedDigits


def saveResult(timeTaken):

    global df

    row = pd.DataFrame([[timeTaken]], columns=['0'])

    # print(row)

    df = df.append(row, ignore_index=True)

    df = df.astype('int64')
    df.to_csv(directory)




left = cv2.imread("IMG_2511.JPG")
scan(imutils.resize(left, 640), 1)