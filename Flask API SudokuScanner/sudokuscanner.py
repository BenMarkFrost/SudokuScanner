import numpy as np 
import imutils
from imutils.perspective import four_point_transform
from skimage.segmentation import clear_border
import scipy
import cv2
import os
import digitfinder

# TODO add process on a separate thread that enable an API to check that the server is still running? Is there an easy way to do this with Flask?


def scan(img):

    solutionData = {}

    img = np.array(img)

    thresh, gray = digitfinder.calculateThreshold(img)

    border = None

    try: 
        border = digitfinder.findContours(thresh).tolist()
    except:
        pass

    if border is None:
        solutionData["border"] = [[0,0][0,0]]
        return None
        # cv2.drawContours(img, [border], -1, (0, 255, 0), 2)
        # cv2.imshow("Bordered", img)
        # cv2.waitKey(0)

    dimg = digitfinder.dewarp(gray, np.array(border))

    digits = digitfinder.splitByDigits(dimg)

    cleanedDigits = digitfinder.cleanDigits(digits)[2:]

    # TODO
    # toNumbers = digitfinder.classifyDigits(cleanedDigits)

    combinedDigits = digitfinder.combineDigits(cleanedDigits)

    # simulating coloured digits here for later
    combinedDigits = cv2.cvtColor(np.float32(combinedDigits),cv2.COLOR_GRAY2RGB)

    skewedSolution = digitfinder.warp(img, combinedDigits, border)

    # saveImg("Digits", skewedSolution)

    # print (skewedSolution.shape, gray.shape)

    # gray = np.float64(gray)
    # skewedSolution = np.float64(skewedSolution)

    # superimposedDigits = cv2.add(skewedSolution, gray)

    outputImage = digitfinder.combineBorderAndImg(border, skewedSolution)

    # cv2.imshow("Combined", outputImage)
    # cv2.waitKey(0)

    # saveImg("Digits", outputImage)



    return outputImage

def saveImg(folder, img):
    num = 0
    directory = "cache/"
    while True:
        try:
            f = open(directory + folder + "/" + folder + str(num) + ".jpg", 'r')
            f.close()
            num = num + 1
        except:
            break

    cv2.imwrite(directory + folder + "/" + folder + str(num) + ".jpg", img)
    num = num + 1


scan(imutils.resize(cv2.imread("IMG_2489.JPG"), 640))