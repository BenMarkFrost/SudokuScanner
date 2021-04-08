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
from func_timeout import FunctionTimedOut


# directory = "server/speedTestResults/videoScanSpeeds.csv"
# df = pd.read_csv(directory, index_col=0)

# count = 0

# From https://stackoverflow.com/questions/5998245/get-current-time-in-milliseconds-in-python
def current_milli_time():
    return round(time.time() * 1000)

clientsDict = {}


# @func_set_timeout(0.3)
def scan(browser_id, img, frame_id):

    global clientsDict

    try:
        client = clientsDict[browser_id]
    
    except:

        client = Client(browser_id)
        clientsDict[browser_id] = client
        print("New client: " + str(browser_id))
    

    frame = Frame(img, frame_id)

    frame.startTime = current_milli_time()

    client.registerFrame(frame.frame_id)

    

    # Analysis

    frame.thresh, frame.gray = digitfinder.calculateThreshold(frame.img)

    frame.border = digitfinder.findContours(frame.thresh)
    
    if frame.border is None:
        frame.outputImage = np.zeros(frame.img.shape)
        frame.endTime = current_milli_time()
        frameBuffer(frame, client)
        client.deregisterFrame(frame.frame_id)
        return frame
        
    manageClients(frame, client)

    frame.skewedSolution = digitfinder.warp(frame.img, frame.combinedDigits, frame.border)

    frame.outputImage = digitfinder.combineBorderAndImg(frame.border, frame.skewedSolution)

    frame.endTime = current_milli_time()

    frameBuffer(frame, client)

    client.deregisterFrame(frame.frame_id)

    return frame


def manageClients(frame, client):

    global clientsDict
    
    timeSinceClassification = current_milli_time() - client.lastClassificationTime

    # print("Time since last " + str(timeSinceClassification))

    frame.combinedDigits = client.savedOutput

    if (timeSinceClassification < 200) or (timeSinceClassification < 1000 and client.solved == True and client.reclassify == False):
        return

    client.lastClassificationTime = current_milli_time()
    thread = Thread(target = cacheClient, args = (frame, client))
    thread.start()

    frame.solutionFrame = True

    print("returning saved output for " + str(frame.frame_id))



def cacheClient(frame, client):

    global clientsDict

    print("started threaded frame for " + str(frame.frame_id))

    combinedDigits, background, currentFrameSolved = findSudoku(frame)

    if currentFrameSolved or not client.solved:
        client.savedOutput = combinedDigits
        client.backgroundForOutput = background
        client.solved = True
    
    client.reclassify = not currentFrameSolved

    print("written threaded frame for " + str(frame.frame_id))
    


def findSudoku(frame):
    
    dewarpedimg = digitfinder.dewarp(frame.gray, frame.border)

    digits = digitfinder.splitByDigits(dewarpedimg)

    toNumbers = digitfinder.classifyDigits(digits)

    # No easy way to do comparisons on arrays   
    # print(str(solvedSudoku[0][0:5]))
    # if str(solvedSudoku[0][0:9]) == str(np.arange(1,10)):
    #     print(np.matrix(toNumbers))


    if np.count_nonzero(toNumbers) > 17:

        try:

            solvedSudoku = sudokusolver.solve(toNumbers)

        except FunctionTimedOut:

            # print(np.matrix(toNumbers))

            print("Sudoku solve timed out")
            solvedSudoku = None
    
    else:

        print("Too few digits recognised")
        solvedSudoku = None


    isItSudoku = False

    if solvedSudoku is None:
        solvedSudoku = toNumbers
    else:        
        isItSudoku = True
        solvedSudoku = np.subtract(solvedSudoku, toNumbers)

    (w,h) = dewarpedimg.shape
    width = int(h / 9.0)
    renderedDigits = digitfinder.renderDigits(solvedSudoku, width, isItSudoku)

    combinedDigits = digitfinder.combineDigits(renderedDigits)

    return combinedDigits, dewarpedimg, isItSudoku


def getSolution(browser_id):
    global clientsDict

    try:
        client = clientsDict[browser_id]

        background = cv2.cvtColor(client.backgroundForOutput, cv2.COLOR_GRAY2RGB)

        background = imutils.resize(background, width=297)
        
        savedOutput = client.savedOutput

        # print(np.matrix(savedOutput))

        print(savedOutput.shape, background.shape)

        outputImage = cv2.add(np.uint8(savedOutput), np.uint8(background))
        return outputImage
    except Exception as e:
        print(e)
        return np.zeros((300,300,3))


# def saveResult(timeTaken):

#     global df

#     row = pd.DataFrame([[timeTaken]], columns=['0'])

#     # print(row)

#     df = df.append(row, ignore_index=True)

#     df = df.astype('int64')
#     df.to_csv(directory)

def frameBuffer(frame, client):

    for i in range(5):
        if client.isNext(frame.frame_id):
            break
        print("Waiting, I'm: ", frame.frame_id)
        if i == 5:
            print("Gave up waiting ", frame.frame_id)
            break
        time.sleep(0.05)

left = cv2.imread("IMG_2511.JPG")
img = imutils.resize(left, 640)
scan(1, img, 1)