from tensorflow import keras
import cv2
import numpy as np
from tqdm import tqdm
import os
import time
os.environ['TF_FORCE_GPU_ALLOW_GROWTH'] = 'true'

directory = "cache/Digits/Gaussian/3 3 Gaussian"
model = keras.models.load_model("model/digitModel.h5")


def loadImages():
    num = 0
    images = []
    
    for image in tqdm(os.listdir(directory)):
    
        # print("**********")
        # print(directory + "/" + image)
        img = cv2.imread(directory + "/" + image)

        # print(img)

        img = cv2.resize(img, (28,28))

        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

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

    print(len(images))

    # print(images[0].shape)

    startTime = current_milli_time()

    for image in images:
        result = np.argmax(model.predict(image.reshape(1, 28, 28, 1)))
        # print(result)

    endTime = current_milli_time()

    timeTaken = endTime - startTime

    perClassification = round(timeTaken / len(images))

    print("Time per image classification: " + str(perClassification))

classify()
