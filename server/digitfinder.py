"""
This file contains low level functions which perform small, specific tasks 
on images with no effect on any variables other than those they have been passed.

This file is set up in the general order in which the functions are called.
"""

import numpy as np
import imutils
from imutils.perspective import four_point_transform
from skimage.segmentation import clear_border
import cv2
import time
import os
import math
from tensorflow import keras
from memoization import cached
from func_timeout import func_set_timeout
from tests import saveImage
from sudoku import Sudoku


# If in a GPU environment, ensure the GPU can be used.
os.environ['TF_FORCE_GPU_ALLOW_GROWTH'] = 'true'

# Load the digit classification model
model = keras.models.load_model("model/digitModel10.h5")


def calculateThreshold(img):
    """
    CalculateThreshold() thresholds the input image to help find the border.

    @params
    img : 3d Numpy array of shape (x,y,3)

    @returns
    threshold: 3d Numpy array of shape (x,y,1)
    dewarp : 3d Numpy array of shape (x,y,1)
    """

    # The code in this function has been adapted from the below link:
    # https://www.pyimagesearch.com/2020/08/10/opencv-sudoku-solver-and-ocr/
    # Credit to Adrian Rosebrock
    # Despite this, the parameters of the functions have undergone significant iterations by the author for this project

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (7,7), 0)

    threshold = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 31, 2)

    # End of reference

    return threshold, gray



def findContours(img):
    """
    FindContours() finds the border of the input image if one exists.

    @params
    img : 3d Numpy array of shape (x,y,1)

    @returns
    dewarp : list of ints
    """

    # The code in this function has been adapted from the below link:
    # https://www.pyimagesearch.com/2020/08/10/opencv-sudoku-solver-and-ocr/
    # Credit to Adrian Rosebrock

    contours = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    contours = imutils.grab_contours(contours)

    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    biggestContour = None

    # This line was implemented by the author of this project
    if (len(contours) == 0) or (cv2.contourArea(contours[0]) < 40000): return None

    for c in contours:

        perimeter = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.01 * perimeter, True)

        if len(approx) == 4:
            biggestContour = approx
            break

    if biggestContour is None: 
        return None

    # End of reference

    return biggestContour.reshape(4,2)



def dewarp(img, border):
    """
    Dewarp() flattens a puzzle based on its border.

    @params
    img : 3d Numpy array of shape (x,y,1)

    @returns
    dewarp : 3d Numpy array of shape (300,300,1)
    """

    dewarp = four_point_transform(img, border)

    size = 300

    dewarp = cv2.resize(dewarp, (size, size))

    return dewarp



def splitByDigits(img):
    """
    SplitByDigits() splits up and cleans an image of a sudoku into its 81 cells.

    @params
    img : 3d Numpy array of shape (300,300,1)

    @returns
    digits : list of 2D numpy arrays
    """

    digits = []

    (w,h) = img.shape

    interval = h / 9

    for j in range(9):
        row = []
        start = math.ceil(j * interval)
        for i in range(9):
            end = math.ceil(i * interval)
            
            x1 = end
            y1 = start
            x2 = end + math.ceil(interval)
            y2 = start + math.ceil(interval)

            digit = img[y1:y2, x1:x2]

            digit = cleanDigit(digit)

            row.append(digit)
        digits.append(row)
    return digits




def cleanDigit(digit):
    """
    CleanDigit() performs preprocessing on individual digit images.

    @params
    img : 3d Numpy array of shape (33,33,1)

    @returns
    digits : 3d Numpy array of shape (33,33,1)
    """

    # The code in this function has been adapted from the below link:
    # https://www.pyimagesearch.com/2020/08/10/opencv-sudoku-solver-and-ocr/
    # Credit to Adrian Rosebrock

    threshold = cv2.threshold(digit, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

    cleaned = clear_border(threshold)

    contours = cv2.findContours(cleaned, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)

    if len(contours) == 0:
        return None

    biggestContour = max(contours, key = cv2.contourArea)

    contourMask = np.zeros(digit.shape, dtype="uint8")
    cv2.drawContours(contourMask, [biggestContour], -1, 255, -1)

    numFilled = cv2.countNonZero(contourMask)
    total = digit.shape[0] * digit.shape[1]
    percentageFilled = numFilled * 100 / total

    if percentageFilled < 3:
        return None
    else:
        cleaned = cv2.bitwise_and(cleaned, cleaned, mask=contourMask)
    # End of reference

        # Binary optimisation
        cleaned = np.rint(cleaned / 255).astype(int)

        return cleaned



def classifyDigits(digits):
    """
    ClassifyDigits() classifies the digits according to a premade model.

    @params
    digits : 2d list of 3d Numpy arrays of shape (33,33,1)

    @returns
    toNumbers : 2d list of ints
    """

    global model

    resizedDigits = []
    res = []

    for row in digits:
        for digit in row:
            if digit is not None:
                tempDigit = np.uint8(digit)
                tempDigit = cv2.resize(tempDigit, (33,33))
                tempDigit = tempDigit.reshape(1,33,33,1)
                resizedDigits.append(tempDigit)

    if len(resizedDigits) > 0:

        results = model.predict(np.vstack(resizedDigits))

        for result in results:
            res.append(np.argmax(result))

    toNumbers = []

    for row in digits:
        tempRow = []
        for digit in row:
            if digit is not None:
                tempRow.append(int(res[0]))
                res = res[1:]
            else:
                tempRow.append(int(0))
        toNumbers.append(tempRow)

    return toNumbers



@func_set_timeout(0.8)
def timedSolve(sudoku):
    """
    timedSolve() solves a given sudoku puzzle with a time limit set by the timout decorator above.

    The @func_set_timeout decorator throws an error if the solve takes longer than x seconds.
    This prevents impossible to solve sudokus from choking the system.

    @params
    sudoku : 2d list of ints

    @returns
    board : 2d list of ints
    """

    start = time.time()

    puzzle = Sudoku(3,3, board=sudoku)
    solution = puzzle.solve()

    stop = time.time()

    if not puzzle.validate():
        return None

    print("Solved in:", stop-start, "seconds")

    board = solution.board

    return board


@cached(max_size=128, thread_safe=True)
def solve(sudoku):
    """
    Solve() efficiently caches the results of timedSolve()

    !!! This two-function setup is necessary since the caching decorator also 
    needs to cache the error returned if timedSolve() is timed out. 

    The @cached decorator caches the input and stores the corresponding outputs.
    This reduces the number of calls made to this function.

    @params
    sudoku : 2d list of ints

    @returns
    timedSolve(sudoku) : 2d list of ints

    """
    return timedSolve(sudoku)



@cached(max_size=128, thread_safe=True)
def renderDigits(digits, width, solved):
    """
    RenderDigits() writes the given digits to cells.
    The @cached decorator caches the input and stores the corresponding outputs.
    This reduces the number of calls made to this function.

    @params
    digits : 2d list of ints
    width : int
    sudoku : boolean

    @returns
    rendered : 2d list of 3d Numpy arrays of shape (33,33,3)
    """

    colour = (255, 255, 255)

    # Green text if solved
    if solved:
        colour = (0,255,0)

    rendered = []

    for row in digits:
        tempRow = []
        for digit in row:
            if digit == 0 or digit == None:
                digit = ""
            bg = np.zeros((width, width, 3))
            bg = cv2.putText(bg, str(digit), (6,25), cv2.FONT_HERSHEY_SIMPLEX, 0.9, colour, 2)
            tempRow.append(bg)
        rendered.append(tempRow)
    
    rendered = combineDigits(rendered)

    return rendered
            




def combineDigits(digits):
    """
    CombineDigits() joins up given images into one image.

    @params
    digits : 2d list of 3d Numpy arrays of shape (33,33,3)

    @returns
    dst : 3d Numpy array of shape (300,300,3)
    """

    rows = []
    
    for row in digits:
        rows.append(np.concatenate(row, axis=1))
    
    combineDigits = np.float32(np.concatenate(rows, axis=0))

    combineDigits = imutils.resize(combineDigits, width=300)

    return combineDigits




def warp(img, toWarp, border):
    """
    Warp() warps a puzzle on to the original image.

    @params
    img : 3d Numpy array of shape (x,y,3)
    toWarp : 3d Numpy array of shape (300,300,3)
    border: list

    @returns
    dst : 3d Numpy array of shape (x,y,3)
    """

    rows,cols,ch = img.shape

    (w,h,d) = toWarp.shape

    # Border coordinates are sent out of order, reordering
    border = [border[0], border[3], border[1], border[2]]

    # Fixing warping bug if sudoku is tilted to the left
    if (border[1][1] > border[2][1]):
        border = [border[2], border[0], border[3], border[1]]

    # The following code has been adapted from the below link:
    # https://www.geeksforgeeks.org/perspective-transformation-python-opencv/
    # Credit to ayushmankumar7

    pts1 = np.float32([[0,0], [w,0], [0,h], [w,h]])
    pts2 = np.float32(border)

    matte = cv2.getPerspectiveTransform(pts1,pts2)
    dst = cv2.warpPerspective(toWarp,matte,(cols,rows))

    # End of reference

    return dst




def combineBorderAndImg(border, img):
    """
    CombineBorderAndImg() draws the identified border of the puzzle on top of the image.

    @params
    border : list
    img : 3d Numpy array of shape (300,300,3)

    @returns
    outputImage : 3d Numpy array of shape (300,300,3)
    """

    border = border.reshape((-1,1,2))

    background = np.zeros(img.shape)

    # Draw the border
    cv2.polylines(background, [border], True, (0,0,255))

    # Combine the border and image
    outputImage = cv2.add(np.float32(background), np.float32(img))
    
    return outputImage



# The following code for getting the current time was taken from the link below.
# https://stackoverflow.com/questions/5998245/get-current-time-in-milliseconds-in-python
# Credit to Naftuli Kay
def current_milli_time():
    return round(time.time() * 1000)
# End of reference