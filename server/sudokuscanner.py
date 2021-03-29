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
from func_timeout import func_set_timeout
from threading import Thread
import time


# directory = "server/speedTestResults/videoScanSpeeds.csv"
# df = pd.read_csv(directory, index_col=0)

# count = 0

# From https://stackoverflow.com/questions/5998245/get-current-time-in-milliseconds-in-python
def current_milli_time():
    return round(time.time() * 1000)

clientsDict = {}
runningThreads = []


# TODO add process on a separate thread that enable an API to check that the server is still running? Is there an easy way to do this with Flask?

# @func_set_timeout(0.3)
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


def manageClients(gray, border, browser_id, frame_id):

    global clientsDict, runningThreads

    if browser_id not in clientsDict:

        client = Client(browser_id)

        # client = cacheClient(client, frame_id, gray, border)
        client.lastClassificationTime = current_milli_time()
        clientsDict[browser_id] = client
        thread = Thread(target = cacheClient, args = (client, browser_id, frame_id, gray, border))
        thread.start()
        # thread.join()

        print("New client: " + str(browser_id))

    else:
        client = clientsDict[browser_id]
        
        timeSinceClassification = current_milli_time() - client.lastClassificationTime

        print("Time since last " + str(timeSinceClassification))

        if timeSinceClassification < 500:
            return client.savedOutput, False

        elif timeSinceClassification < 3000 and client.solved == True:
            return client.savedOutput, False

        else:
            # client = cacheClient(client, frame_id, gray, border)
            client.lastClassificationTime = current_milli_time()
            clientsDict[browser_id] = client
            thread = Thread(target = cacheClient, args = (client, browser_id, frame_id, gray, border))
            thread.start()
            # thread.join()

    print("true")

    print("read threadded frame for " + str(frame_id))

    
    return client.savedOutput, True


def cacheClient(client, browser_id, frame_id, gray, border):

    print("started threaded frame for " + str(frame_id))

    global clientsDict

    # time.sleep(2)

    # client.registerFrame(frame_id)
    combinedDigits, solved = findSudoku(gray, border)

    if solved:
        client.savedOutput = combinedDigits
        client.solved = solved
    else:
        if not client.solved:
            client.savedOutput = combinedDigits


    # if client.solved or client.savedOutput is None:
    #     client.savedOutput = combinedDigits

    # for i in range(5):
    #     if client.isNext(frame_id):
    #         break
    #     print("WAITING, I'm: ", frame_id)
    #     time.sleep(0.05)
    #     if i == 5:
    #         print("Gave up waiting ", frame_id)
    #         break

    # client.deregisterFrame(frame_id)
    # client.lastClassificationTime = current_milli_time()

    clientsDict[browser_id] = client

    print("written threadded frame for " + str(frame_id))
    



def findSudoku(gray, border):
    
    dimg = digitfinder.dewarp(gray, border)

    digits = digitfinder.splitByDigits(dimg)

    toNumbers = digitfinder.classifyDigits(digits)

    solvedSudoku = sudokusolver.solve(toNumbers)

    isItSudoku = False

    if solvedSudoku is None:
        solvedSudoku = toNumbers
    else:
        isItSudoku = True
        solvedSudoku = np.subtract(solvedSudoku, toNumbers)

    (w,h) = dimg.shape
    width = int(h / 9.0)
    renderedDigits = digitfinder.renderDigits(solvedSudoku, width, isItSudoku)

    combinedDigits = digitfinder.combineDigits(renderedDigits)

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