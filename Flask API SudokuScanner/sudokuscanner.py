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
        print("No Sudoku Found")
        return np.zeros(img.shape)
        # cv2.drawContours(img, [border], -1, (0, 255, 0), 2)
        # cv2.imshow("Bordered", img)
        # cv2.waitKey(0)

    dimg = digitfinder.dewarp(gray, np.array(border))

    digits = digitfinder.splitByDigits(dimg)

    cleanedDigits = digitfinder.cleanDigits(digits)[2:]

    # TODO
    # toNumbers = digitfinder.classifyDigits(cleanedDigits)

    combinedDigits = digitfinder.combineDigits(cleanedDigits)

    combinedDigits = cv2.cvtColor(np.float32(combinedDigits),cv2.COLOR_GRAY2RGB)

    skewedSolution = digitfinder.warp(img, combinedDigits, border)

    outputImage = digitfinder.combineBorderAndImg(border, skewedSolution)


    # cv2.imshow("Combined", outputImage)
    # cv2.waitKey(0)

    # saveImg("Digits", outputImage)

    # solutionData["border"] = border
    # solutionData["digits"] = [1: [40,50], 4: [40, 75], 7:[200,300]]]

    # Add section about compression here, looks like compressed by about 40%
    # saveImg("Outputs", outputImage)


    # pilImage = Image.fromarray(np.uint8(outputImage))

    # global buffer

    # pilImage.save(buffer, "JPEG", quality=10)

    # print(buffer)

    # with open("cache/Outputs/compressed.jpg", "w") as temp:
    #     temp.write(buffer.contents())

    # print(encoded)

    # decoded = cv2.imdecode(encoded, 1)

    # cv2.imshow("After encode", decoded)
    # cv2.waitKey(0)

    # decoded = cv2.imdecode(encoded, 0)

    # cv2.imshow("Decoded", decoded)
    # cv2.waitKey(0)

    # print(decoded.shape)

    # for row in decoded:
    #     print(row)

    # print(decoded)

    # saveImg("Outputs", outputImage)

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


# scan(imutils.resize(cv2.imread("IMG_2489.JPG"), 640))