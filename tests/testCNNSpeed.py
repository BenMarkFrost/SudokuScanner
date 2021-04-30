"""
This file records the speed of different models for use in digit classification.
"""

## External libraries
from tensorflow import keras
import cv2
import numpy as np
from tqdm import tqdm
import os
import time
import numpy as np
##

os.environ['TF_FORCE_GPU_ALLOW_GROWTH'] = 'true'

directory = "CNNTestData/FONT_HERSHEY_SIMPLEX/"
model = keras.models.load_model("model/digitModel10.h5")

def loadImages():
    """
    LoadImages() reads in a directory of images to test.

    @params
    none

    @returns
    images : list of 3d Numpy arrays of size (28,28,1)
    """

    num = 0
    images = []
    
    for image in tqdm(os.listdir(directory)):
    
        img = cv2.imread(directory + "/" + image)

        img = cv2.resize(img, (28,28))

        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        img = np.rint(img / 255).astype(int).reshape(1, 28, 28, 1)
        result = np.argmax(model.predict(img))
        
        images.append(img)

    return images

def classify():
    """
    classify() reads in a directory of images to test.

    @params
    none

    @returns
    none
    """

    global model
    images = loadImages()

    startTime = current_milli_time()

    model.predict(np.vstack(images))


    endTime = current_milli_time()

    timeTaken = endTime - startTime

    perClassification = round(timeTaken / len(images))

    print("Time per image classification: " + str(timeTaken))

# The following code for getting the current time was taken from the link below.
# https://stackoverflow.com/questions/5998245/get-current-time-in-milliseconds-in-python
# Credit to Naftuli Kay
def current_milli_time():
    return round(time.time() * 1000)
# End of reference

classify()
