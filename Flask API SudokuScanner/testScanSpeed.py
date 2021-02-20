import cv2
import time
import sudokuscanner
import imutils
import pandas as pd

# From https://stackoverflow.com/questions/5998245/get-current-time-in-milliseconds-in-python
def current_milli_time():
    return round(time.time() * 1000)

# right = cv2.imread("IMG_2489.JPG")
left = cv2.imread("IMG_2511.JPG")

directory = "speedTestResults/speeds.csv"
df = pd.read_csv(directory, index_col=0)

def doTheScan(img):

    startTime = current_milli_time()

    print("starting")

    sudokuscanner.scan(imutils.resize(img, 640))

    endTime = current_milli_time()

    timeTaken = endTime - startTime

    print("Time taken: " + str(timeTaken))

    # saveResult(timeTaken)


def saveResult(timeTaken):

    global df

    row = pd.DataFrame([[timeTaken]], columns=['0'])

    print(row)

    df = df.append(row, ignore_index=True)

    print(df)

    # with open("speedTestResults/speeds.csv", a) as file:
    #     file.write()

doTheScan(left)
doTheScan(left)


df = df.astype('int64')
df.to_csv(directory)
