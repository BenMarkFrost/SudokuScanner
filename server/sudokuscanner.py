import numpy as np 
import imutils
from imutils.perspective import four_point_transform
from skimage.segmentation import clear_border
import scipy
import cv2
import os
from server import digitfinder
from server import sudokusolver
from server.Client import Client
from io import BytesIO
from PIL import Image
import time
import pandas as pd


# directory = "server/speedTestResults/videoScanSpeeds.csv"
# df = pd.read_csv(directory, index_col=0)

# count = 0

# From https://stackoverflow.com/questions/5998245/get-current-time-in-milliseconds-in-python
def current_milli_time():
    return round(time.time() * 1000)

clientsDict = {}


# TODO add process on a separate thread that enable an API to check that the server is still running? Is there an easy way to do this with Flask?

def scan(img, browser_id, frame_id):

    startTime = current_milli_time()

    thresh, gray = digitfinder.calculateThreshold(img)

    border = None

    try: 
        border = digitfinder.findContours(thresh)
    except:
        pass

    if border is None:
        return np.zeros(img.shape), False

    combinedDigits, calculating = manageClients(gray, border, browser_id, frame_id)

    skewedSolution = digitfinder.warp(img, combinedDigits, border)

    outputImage = digitfinder.combineBorderAndImg(border, skewedSolution)

    endTime = current_milli_time()

    timeTaken = endTime - startTime

    return outputImage, calculating
    # return 1, 2


def manageClients(gray, border, browser_id, frame_id):

    global clientsDict
    calculating = False

    # print("ClientsDict: " + str(clientsDict.keys()))

    if browser_id not in clientsDict:

        client = Client(browser_id)

        calculating = True

        # client.putFrame(frame_id, findSudoku(gray, border))

        client.registerFrame(frame_id)
        combinedDigits, client.solved = findSudoku(gray, border)
        client.savedOutput = combinedDigits
        

        # combinedDigits, solved = findSudoku(gray, border)
        # clientsDict[browser_id] = (current_milli_time(), combinedDigits, solved)

        print("New client: " + str(browser_id))

    else:
        # lastClassificationTime, savedOutput, solved = clientsDict[browser_id]
        client = clientsDict[browser_id]
        
        timeSinceClassification = current_milli_time() - client.lastClassificationTime

        if timeSinceClassification < 500:
            return client.savedOutput, False
        elif (timeSinceClassification < 3000) and (client.solved == True):
            return client.savedOutput, False
        else:
            calculating = True

            client.registerFrame(frame_id)
            newCombinedDigits, solved = findSudoku(gray, border)

            if (solved):
                combinedDigits = newCombinedDigits
                client.savedOutput = combinedDigits
                client.solved = True
            else:
                combinedDigits = client.savedOutput

            

    for i in range(5):
        if client.isNext(frame_id):
            break
        print("WAITING, I'm: ", frame_id)
        time.sleep(0.05)
        if i == 5:
            print("Gave up waiting ", frame_id, browser_id)

    client.deregisterFrame(frame_id)
    client.lastClassificationTime = current_milli_time()
    clientsDict[browser_id] = client
    
    return combinedDigits, calculating


def findSudoku(gray, border):
    
    dimg = digitfinder.dewarp(gray, border)

    # digitfinder.saveImg("steps", dimg)

    digits = digitfinder.splitByDigits(dimg)[1:]

    toNumbers = digitfinder.classifyDigits(digits)

    # print(np.matrix(toNumbers))

    # for j in range(len(digits)):
    #     row = digits[j]
    #     for i in range(len(row)):
    #         if row[i] is not None:
    #             digitfinder.saveImg("IMG_2511", row[i]*255, toNumbers[j][i])

    solvedSudoku = sudokusolver.solve(toNumbers)

    # print(np.matrix(solvedSudoku))

    # solvedSudoku = Nones

    isItSudoku = False

    # print("sending to sudoku")
    if solvedSudoku is None:
        # print("No sudoku :(")
        solvedSudoku = toNumbers
    else:
        # print(sudokusolver.solve.cache_info())
        isItSudoku = True
        solvedSudoku = np.subtract(solvedSudoku, toNumbers)

    # print(np.matrix(solvedSudoku))

    (w,h) = dimg.shape
    width = int(h / 9.0)
    renderedDigits = digitfinder.renderDigits(solvedSudoku, width, isItSudoku)

    combinedDigits = digitfinder.combineDigits(renderedDigits)
    # digitfinder.saveImg("steps", combinedDigits)

    return combinedDigits, isItSudoku


# def saveResult(timeTaken):

#     global df

#     row = pd.DataFrame([[timeTaken]], columns=['0'])

#     # print(row)

#     df = df.append(row, ignore_index=True)

#     df = df.astype('int64')
#     df.to_csv(directory)




left = cv2.imread("IMG_2511.JPG")
scan(imutils.resize(left, 640), 1, 1)