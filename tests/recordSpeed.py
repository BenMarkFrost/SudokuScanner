import cv2
import time
from server import sudokuscanner, digitfinder
# from server.Frame import Frame
import imutils
import pandas as pd
import time
import numpy as np
# import sys
# sys.path.append('../')

# From https://stackoverflow.com/questions/5998245/get-current-time-in-milliseconds-in-python
def current_milli_time():
    return round(time.time() * 1000)

right = cv2.imread("IMG_2511.JPG")
new = imutils.resize(cv2.imread("IMG_2832.JPG"), 640)
num = 1

directory = "server/speedTestResults/ThreadingAndCompression.csv"
try:
    df = pd.read_csv(directory, index_col=0)
except:
    df = pd.DataFrame()

def startRecordedScan(img):

    global num

    # if img is None:
    #     return np.zeros(1,1,1)

    start = time.time()

    frame = sudokuscanner.scan(2, img, num)
    
    num = num + 1

    stop = time.time()

    saveResult(stop-start, frame.calculated)

    return frame.outputImage


def oneImage():

    start = time.time()

    result = sudokuscanner.scan(2, new, 1)

    stop = time.time()

    time.sleep(3)

    result = sudokuscanner.scan(2, new, 1)

    print(stop - start)

    digitfinder.saveImg("imageTest", cv2.add(np.uint8(result.outputImage), np.uint8(new)), 1)

oneImage()

def saveResult(timeTaken, calculating):

    global df

    # print(timeTaken)

    tmpCalc = 0

    if calculating:
        tmpCalc = 1

    row = pd.DataFrame([[timeTaken, tmpCalc]], columns=['time', 'calculation'])

    # print(row)

    df = df.append(row, ignore_index=True)

    # print(df)

    # with open("speedTestResults/speeds.csv", a) as file:
    #     file.write()


# for i in range(100):
#     start = time.time()

#     doTheScan(right)

#     stop = time.time()

#     saveResult(stop-start)


def finish():

    global df
    df = df.astype('float64')
    df.to_csv(directory)
