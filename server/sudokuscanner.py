import numpy as np 
import imutils
from imutils.perspective import four_point_transform
from skimage.segmentation import clear_border
import scipy
import cv2
import os
from server import digitfinder, sudokusolver
from server.Frame import Frame
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


# @func_set_timeout(0.3)
def scan(browser_id, frame):

    startTime = current_milli_time()

    frame.thresh, frame.gray = digitfinder.calculateThreshold(frame.img)

    try: 
        frame.border = digitfinder.findContours(frame.thresh)
    except:
        pass

    if frame.border is None:
        frame.outputImage = np.zeros(frame.img.shape)
        endTime = current_milli_time()
        frame.timeTaken = endTime - startTime
        return frame

    frame.combinedDigits, frame.calculated = manageClients(frame.gray, frame.border, browser_id, frame.frame_id)

    frame.skewedSolution = digitfinder.warp(frame.img, frame.combinedDigits, frame.border)

    frame.outputImage = digitfinder.combineBorderAndImg(frame.border, frame.skewedSolution)

    endTime = current_milli_time()
    frame.timeTaken = endTime - startTime

    return frame


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

        # print("Time since last " + str(timeSinceClassification))

        if timeSinceClassification < 500:
            return client.savedOutput, False

        elif timeSinceClassification < 3000 and client.solved == True and client.reclassify == False:
            return client.savedOutput, False

        else:
            # client = cacheClient(client, frame_id, gray, border)
            client.lastClassificationTime = current_milli_time()
            clientsDict[browser_id] = client
            thread = Thread(target = cacheClient, args = (client, browser_id, frame_id, gray, border))
            thread.start()
            # thread.join()

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
        client.solved = True
        client.reclassify = False
    else:
        # if not client.solved:
        #     client.savedOutput = combinedDigits
        client.reclassify = True



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
frame = Frame(imutils.resize(left, 640), 1)
scan(1, frame)