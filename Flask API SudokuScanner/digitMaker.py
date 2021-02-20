import digitfinder
import numpy as np
import cv2


ints = range(10)

# print(randInts)

renderedInts = []

for num in ints:
    renderedInts.append(digitfinder.renderIndividualDigit(num, 33))

# cv2.imshow("allInts", renderedInts[0][0])
# cv2.waitKey(0)


for num, img in zip(ints, renderedInts):
    fileName = str(num) + ".jpg"
    directory = "CNNTestData/FONT_HERSHEY_SIMPLEX/"
    cv2.imwrite(directory + fileName, img)