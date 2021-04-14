"""
This file is used in by localtest.py record the speed of the system.
"""

import cv2
import time
from server import sudokuscanner
from tests import saveImage
import imutils
import pandas as pd
import numpy as np

num = 1

# Setting up output of speed test results.
directory = "server/speedTestResults/ThreadingAndCompression.csv"
try:
    df = pd.read_csv(directory, index_col=0)
except:
    df = pd.DataFrame()

def startRecordedScan(img):
    """
    StartRecordedScan() measures the speed which an image takes to be returned by the sudokuscanner file.
    This is only called by localtest.py

    @params
    img : 3d Numpy array of shape (x,y,3)

    @returns
    outputImage : 3d Numpy array of shape (x,y,3)
    """

    global num

    start = time.time()

    frame = sudokuscanner.scan(2, img, num)
    
    num += 1

    stop = time.time()

    saveResult(stop-start, frame.calculated)

    return frame.outputImage


def oneImage():
    """
    oneImage() records the speed of a test image.

    @params
    none

    @returns
    none
    """

    # Loading the test image.
    right = cv2.imread("IMG_2511.JPG")
    new = imutils.resize(cv2.imread("IMG_2832.JPG"), 640)

    # Recording the speed of the scan.
    start = time.time()

    result = sudokuscanner.scan(2, new, 1)

    stop = time.time()

    # If this scan has invoked further analysis, wait for that to finish.
    time.sleep(3)

    # Retrieve the result of this further analysis
    result = sudokuscanner.scan(2, new, 1)

    print(stop - start)

    saveImage.saveImg("imageTest", cv2.add(np.uint8(result.outputImage), np.uint8(new)))


def saveResult(timeTaken, calculating):
    """
    SaveResult() appends a given time and boolean to a file.

    @params
    timeTaken : int
    calculating : Boolean

    @returns
    none
    """

    global df

    tmpCalc = 0

    if calculating:
        tmpCalc = 1

    row = pd.DataFrame([[timeTaken, tmpCalc]], columns=['time', 'calculation'])

    df = df.append(row, ignore_index=True)


def finish():
    """
    Finish() saves the appended dataframe to a file.

    @params
    none

    @returns
    none
    """

    global df

    df = df.astype('float64')
    df.to_csv(directory)