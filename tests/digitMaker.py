"""
This file contains necessary functions to render digits to image files for use in a CNN.
"""

from server import digitfinder
import numpy as np
import cv2
from tqdm import tqdm
import os

directory = "CNNTestData/Fonts/"

def generateFonts():
    """
    GenerateFonts() renders digits from the selection of OpenCV fonts to images files.

    @params
    none

    @returns
    none
    """

    global directory

    # 10 fonts included with OpenCV
    ints = range(10)
    renderedInts = [[]]

    for num in ints:
        fontRow = []
        for font in range(8):
            bg = np.zeros((33, 33, 3))
            scale = 0.9
            # 1 and 5 are unusually large fonts, correcting.
            if font == 1 or font == 5:
                scale = 1.5

            bg = cv2.putText(bg, str(num), (6,25), font, scale, (255, 255, 255), 2)
            gray = cv2.cvtColor(np.uint8(bg), cv2.COLOR_BGR2GRAY)
            inverse = np.invert(gray)
            fontRow.append(inverse)
        print("appending " + str(len(fontRow)))
        renderedInts.append(fontRow)

    # Writing the images to files, and labelling for use in a CNN.
    fontNum = 0
    for num, imgs in zip(ints, renderedInts):
        
        for img in imgs:
            fileName = str(num-1) + str(fontNum) + ".jpg"
            cv2.imwrite(directory + fileName, img)
            fontNum = fontNum + 1



def thresholdDigits():
    """
    ThresholdDigits() reads in the digits rendered to digits in generateFonts() 
    and thresholds them using the same cleanDigit() function as in the working system.

    @params
    border : list
    img : 3d Numpy array of shape (300,300,3)

    @returns
    outputImage : 3d Numpy array of shape (300,300,3)
    """

    global directory

    X = []
    y = []

    for fileName in tqdm(os.listdir(directory)):
        
        img = cv2.imread(directory + fileName)

        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        img = np.uint8(img)

        cleaned = digitfinder.cleanDigit(img)

        X.append(cleaned)
        y.append(fileName)

    for img, name in zip(X, y):
        cv2.imwrite("CNNTestData/fontsMasked/" + name, img)
        
