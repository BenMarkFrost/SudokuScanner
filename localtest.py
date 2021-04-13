"""
This file hosts the local testing code.
The video stream will be processed and dispalyed directly on the host machine.
Press 'q' to exit the window.
"""

import cv2
from server import sudokuscanner
import numpy as np

frame_id = 0

camera = cv2.VideoCapture(0)


def runApp():

    global frame_id

    while True:

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        ret, img = camera.read()

        # Perform image Analysis
        frame = sudokuscanner.scan(2, img, frame_id)

        frame_id = frame_id + 1

        # Combining the original image and the overlay generated through analysis.
        output = cv2.add(np.uint8(img), np.uint8(frame.outputImage))

        # Combining side by side the output image and the threshold preprocessing step.
        output = np.hstack((output, cv2.cvtColor(frame.thresh, cv2.COLOR_GRAY2BGR)))

        # Adding latency text to the top left.
        cv2.rectangle(output, (0,0), (200, 30), (255,255,255), -1)
        cv2.putText(output, (f"Latency: {frame.timeTaken()}ms"), (10,22), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0,0,0), 1, cv2.LINE_AA)

        cv2.imshow("output", output)


    camera.release()
    cv2.destroyAllWindows()


runApp()

