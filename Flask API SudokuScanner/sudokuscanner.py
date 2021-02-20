import numpy as np 
import imutils
from imutils.perspective import four_point_transform
from skimage.segmentation import clear_border
import scipy
import cv2
import os
import digitfinder
from io import BytesIO
from PIL import Image
import time

buffer = BytesIO()


# TODO add process on a separate thread that enable an API to check that the server is still running? Is there an easy way to do this with Flask?


def scan(img):

    img = np.array(img)

    thresh, gray = digitfinder.calculateThreshold(img)

    border = None

    try: 
        border = digitfinder.findContours(thresh).tolist()
    except:
        pass

    if border is None:
        return np.zeros(img.shape)
        # cv2.drawContours(img, [border], -1, (0, 255, 0), 2)
        # cv2.imshow("Bordered", img)
        # cv2.waitKey(0)

    dimg = digitfinder.dewarp(gray, np.array(border))

    # saveImg("Rotation", dimg)

    digits = digitfinder.splitByDigits(dimg)

    cleanedDigits = digitfinder.cleanDigits(digits)[2:]

    # for i in cleanedDigits:
    #     for digit in i:
    #         cv2.imshow("output", digit)
    #         cv2.waitKey(0)

    # print(cleanedDigits)

    # TODO
    # CNN for number recognition

    toNumbers = digitfinder.classifyDigits(cleanedDigits)

    # print(toNumbers)
    # print(toNumbers)
    # returns a 2d array of digits or None in blank spots

    # sudokusolver
    # returns solved 2d array of digits or None in blank spots

    # render digits to images
    # returns 2d array of digit images

    (w,h) = dimg.shape
    width = int(h / 9.0)
    renderedDigits = digitfinder.renderDigits(toNumbers, width)

    # then combine them below



    combinedDigits = digitfinder.combineDigits(renderedDigits)

    combinedDigits = np.float32(combinedDigits)


    skewedSolution = digitfinder.warp(img, combinedDigits, border)

    outputImage = digitfinder.combineBorderAndImg(border, skewedSolution)

    digitfinder.saveImg("Rendering", outputImage)


    return outputImage


left = cv2.imread("IMG_2511.JPG")
scan(imutils.resize(left, 640))