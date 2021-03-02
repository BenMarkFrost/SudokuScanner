import digitfinder
import numpy as np
import cv2
from tqdm import tqdm
import os


def generateFonts():
    ints = range(10)
    renderedInts = [[]]

    for num in ints:
        fontRow = []
        for font in range(8):
            bg = np.zeros((33, 33, 3))
            scale = 0.9
            if font == 1 or font == 5:
                scale = 1.5
            bg = cv2.putText(bg, str(num), (6,25), font, scale, (255, 255, 255), 2)
            gray = cv2.cvtColor(np.uint8(bg), cv2.COLOR_BGR2GRAY)
            inverse = np.invert(gray)
            fontRow.append(inverse)
        print("appending " + str(len(fontRow)))
        renderedInts.append(fontRow)

    fontNum = 0
    for num, imgs in zip(ints, renderedInts):
        
        for img in imgs:
            fileName = str(num-1) + str(fontNum) + ".jpg"
            directory = "CNNTestData/Fonts/"
            cv2.imwrite(directory + fileName, img)
            fontNum = fontNum + 1

def thresholdDigits():
    directory = "CNNTestData/Fonts/"

    X = []
    y = []

    for image in tqdm(os.listdir(directory)):
        
        img = cv2.imread(directory + image)

        # cv2.imshow("img", img)
        # cv2.waitKey(0)

        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        img = np.uint8(img)

        # print(img.dtype)

        cleaned = digitfinder.cleanDigit(img)

        X.append(cleaned)
        y.append(image)

    for image, name in zip(X, y):
        directory = "CNNTestData/fontsMasked/"
        cv2.imwrite(directory + name, image)
        

thresholdDigits()
