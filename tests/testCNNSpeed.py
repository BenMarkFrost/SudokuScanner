"""
This file records the speed of different models for use in digit classification.
"""
from tensorflow import keras
import cv2
import numpy as np
from tqdm import tqdm
import os
import time
import numpy as np

os.environ['TF_FORCE_GPU_ALLOW_GROWTH'] = 'true'

directory = "CNNTestData/FONT_HERSHEY_SIMPLEX/"
model = keras.models.load_model("model/digitModel3.h5")

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
    
        # print("**********")
        # print(directory + "/" + image)
        img = cv2.imread(directory + "/" + image)

        # print(img)

        img = cv2.resize(img, (28,28))

        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        img = np.rint(img / 255).astype(int).reshape(1, 28, 28, 1)
        result = np.argmax(model.predict(img))



        # cv2.imshow("img", img)
        # cv2.waitKey(0)
        
        images.append(img)

    return images

# From https://stackoverflow.com/questions/5998245/get-current-time-in-milliseconds-in-python
def current_milli_time():
    return round(time.time() * 1000)

def classify():

    global model
    images = loadImages()

    # print(len(images))

    # print(images[0].shape)

    startTime = current_milli_time()

    model.predict(np.vstack(images))

    # for image in images:
    #     result = np.argmax(model.predict(image.reshape(1, 28, 28, 1)))
    #     # print(result)

    endTime = current_milli_time()

    timeTaken = endTime - startTime

    perClassification = round(timeTaken / len(images))

    print("Time per image classification: " + str(timeTaken))

classify()



# import tensorflow as tf

# tf.config.list_physical_devices("GPU")
