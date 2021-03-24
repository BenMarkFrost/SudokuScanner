import cv2
import time
from server import sudokuscanner
import imutils
import pandas as pd
import time
# import sys
# sys.path.append('../')

# From https://stackoverflow.com/questions/5998245/get-current-time-in-milliseconds-in-python
def current_milli_time():
    return round(time.time() * 1000)

right = cv2.imread("IMG_2511.JPG")
left = cv2.imread("IMG_2489.JPG")
num = 1

directory = "server/speedTestResults/withCachingSpeeds.csv"
try:
    df = pd.read_csv(directory, index_col=0)
except:
    df = pd.DataFrame()

def doTheScan(img):

    global num

    # if img is None:
    #     return np.zeros(1,1,1)

    start = time.time()

    result, calculating = sudokuscanner.scan(img, 2, num)
    num = num + 1

    stop = time.time()

    saveResult(stop-start, calculating)

    return result





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
