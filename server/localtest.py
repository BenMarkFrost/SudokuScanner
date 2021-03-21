import cv2
from server import sudokuscanner
import time
import numpy as np

camera = cv2.VideoCapture(0)

def runApp():
    while True:

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        ret, frame = camera.read()

        startTime = current_milli_time()

        response = sudokuscanner.scan(frame, 2)

        endTime = current_milli_time()

        frame = np.uint8(frame)

        response = np.uint8(response)

        # for row in frame:
        #     print(row)

        # for row in response:
        #     print(row)

        output = cv2.add(frame, response)

        # digitfinder.saveImg("steps", )

        operationTime = endTime - startTime

        cv2.rectangle(output, (0,0), (200, 30), (255,255,255), -1)

        cv2.putText(output, ("Latency: " + str(operationTime) + "ms"), (10,22), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0,0,0), 1, cv2.LINE_AA)

        cv2.imshow("output", output)


        # cv2.imshow("response", response)

        # cv2.imshow("frame", frame)

    camera.release()
    cv2.destroyAllWindows()


# From https://stackoverflow.com/questions/5998245/get-current-time-in-milliseconds-in-python
def current_milli_time():
    return round(time.time() * 1000)

runApp()

