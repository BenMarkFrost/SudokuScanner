import cv2
import sys
# sys.path.append('../')
# sys.path.insert(1, '../')
# from server import sudokuscanner
# from tests import recordSpeed
from server import sudokuscanner, digitfinder
import time
import numpy as np

print("running")

num = 0

camera = cv2.VideoCapture(0)


def runApp():

    global num

    while True:

        if cv2.waitKey(1) & 0xFF == ord('q'):
            recordSpeed.finish()
            break

        ret, img = camera.read()

        startTime = current_milli_time()

        frame = sudokuscanner.scan(2, img, num)

        endTime = current_milli_time()


        num = num + 1

        # print(frame.outputImage.shape, frame.thresh.shape)

        response = frame.outputImage

        # response = recordSpeed.startRecordedScan(img)


        img = np.uint8(img)

        response = np.uint8(response)

        # print(frame.shape, response.shape)

        output = cv2.add(img, response)

        output = np.hstack((output, cv2.cvtColor(frame.thresh, cv2.COLOR_GRAY2BGR)))

        # print(frame.digits.shape)

        if frame.digits is not None:
            print("Digits exists")
            # combinedDigits = cv2.cvtColor(digitfinder.combineDigits(frame.digits), cv2.COLOR_GRAY2BGR)



        operationTime = endTime - startTime

        cv2.rectangle(output, (0,0), (200, 30), (255,255,255), -1)
        # cv2.rectangle(output, (0,30), (80, 60), (255,255,255), -1)

        cv2.putText(output, ("Latency: " + str(operationTime) + "ms"), (10,22), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0,0,0), 1, cv2.LINE_AA)

        # cv2.putText(output, str(solved), (10,52), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0,0,0), 1, cv2.LINE_AA)

        cv2.imshow("output", output)


    camera.release()
    cv2.destroyAllWindows()


# From https://stackoverflow.com/questions/5998245/get-current-time-in-milliseconds-in-python
def current_milli_time():
    return round(time.time() * 1000)

runApp()

