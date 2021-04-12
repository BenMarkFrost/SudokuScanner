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
import copy




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

    # digitfinder.saveImg("imageTest", frame.thresh)


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

    if (timeSinceClassification < 500) or (timeSinceClassification < 1000 and client.solved == True and client.reclassify == False):
        return

    client.lastClassificationTime = current_milli_time()
    thread = Thread(target = cacheClient, args = (frame, client), daemon=True)
    thread.start()

    frame.solutionFrame = True

    # print("returning saved output for " + str(frame.frame_id))



def cacheClient(frame, client):

    global clientsDict

    print("started threaded frame for " + str(frame.frame_id))

    digits, combinedDigits, background, currentFrameSolved = findSudoku(frame)

    if currentFrameSolved:
        print("Replacing image")
        client.savedOutput = combinedDigits
        client.backgroundForOutput = background
        client.solved = True
    elif not client.solved:
        print("Replacing image")
        client.savedOutput = combinedDigits
        client.backgroundForOutput = background

    
    client.reclassify = not currentFrameSolved

    frame.digits = digits

    # time.sleep(3)

    client.lastClassificationTime = current_milli_time()


    print("written threaded frame for " + str(frame.frame_id))
    


def findSudoku(frame):

    dewarpedimg = digitfinder.dewarp(frame.gray, frame.border)

    digits = digitfinder.splitByDigits(dewarpedimg)

    # print(np.array(digits).shape)

    toNumbers = digitfinder.classifyDigits(digits)
    
    # print(np.matrix(toNumbers))

    originals = copy.deepcopy(toNumbers)


    # No easy way to do comparisons on arrays   
    # print(str(solvedSudoku[0][0:5]))
    # if str(solvedSudoku[0][0:9]) == str(np.arange(1,10)):
    #     print(np.matrix(toNumbers))


    if np.count_nonzero(toNumbers) > 16:
        print("Attempting solve with", np.count_nonzero(toNumbers), "numbers in puzzle")

        try:

            # print(np.matrix(np.array(toNumbers)))

            # solvedSudoku = sudokusolver.solve(toNumbers)

            # print(np.matrix(np.array(solvedSudoku)))


            # print(np.matrix(toNumbers))

            # puzzle = Sudoku(3,3, board=toNumbers)
            # print(puzzle)
            # solution = puzzle.solve()

            # print(type(toNumbers[0][0]))

            solvedSudoku = sudokusolver.solve(toNumbers)

            print("Sudoku solver:", sudokusolver.solve.cache_info())


            # print(np.matrix(solvedSudoku))

            # print(np.matrix(solution.board))

            # solvedSudoku = solution.board

        except FunctionTimedOut:

            print("Sudoku solve timed out")
            solvedSudoku = None
    
    else:

        print("Too few digits recognised")
        solvedSudoku = None

    # print(np.matrix(solvedSudoku))
    # print(np.matrix(originals))


    isItSudoku = False

    # if solvedSudoku is None:
    #     solvedSudoku = toNumbers
    # else:
    #     # print(np.matrix(solvedSudoku))
    #     isItSudoku = True
    #     # solvedSudoku = np.uint8(np.array(solvedSudoku))
    #     # originals = np.uint8(np.array(originals))
    #     solvedSudoku = np.subtract(solvedSudoku, originals)

    try:
        solvedSudoku = np.subtract(solvedSudoku, originals)
        isItSudoku = True
    except:
        solvedSudoku = toNumbers
        


    (w,h) = dewarpedimg.shape
    width = int(h / 9.0)
    combinedDigits = digitfinder.renderDigits(solvedSudoku, width, isItSudoku)

    print("Digit renderer:", digitfinder.renderDigits.cache_info())

    # digitfinder.saveImg("digits", combinedDigits)

    return digits, combinedDigits, dewarpedimg, isItSudoku


def getSolution(browser_id):
    global clientsDict

    solutionOutputSize = 600

    try:
        client = clientsDict[browser_id]

        background = cv2.cvtColor(client.backgroundForOutput, cv2.COLOR_GRAY2RGB)

        savedOutput = client.savedOutput

        # background = imutils.resize(background, width=297)

        outputImage = cv2.add(np.uint8(savedOutput), np.uint8(background))

        outputImage = imutils.resize(outputImage, width=solutionOutputSize)

        return outputImage
    except Exception as e:
        print(e)
        return np.zeros((solutionOutputSize,solutionOutputSize,3))

def frameBuffer(frame, client):

    for i in range(5):
        earliestFrame = client.next()
        if int(earliestFrame) == int(frame.frame_id):
            if (i > 0):
                print(frame.frame_id, "released")
            break
        print("Waiting for " + str(earliestFrame), ", I'm: ", frame.frame_id)
        if i == 4:
            break
        # Sleep for 50ms
        time.sleep(0.05)

left = cv2.imread("IMG_2511.JPG")
new = imutils.resize(cv2.imread("IMG_2832.JPG"), 640)
img = imutils.resize(left, 640)
scan(1, img, 1)