"""
This file is a simply saves images to folders for testing.
"""

from pathlib import Path
import cv2

directory = "cache/"
# Dictionary holding directories and the corresponding highest value of file name in each.
highestNumber = {}

def saveImg(folder, img, fileName=None):
    """
    SaveImg() saves the given image to a file.

    @params
    folder : string
    img : 3d Numpy array of shape (x,y,z)
    fileName : string, optional

    @returns
    none
    """

    global highestNumber
    
    if folder in highestNumber:
        num = highestNumber[folder]
    else:
        print("Adding new folder to dict")
        num = 0

    generatedPath = ""  

    while True:
        generatedPath = directory + folder + "/" + folder + str(fileName) + str(num) + ".jpg"
        myFile = Path(generatedPath)
        if myFile.is_file():
            num += 1
        else:
            break

    highestNumber[folder] = num

    cv2.imwrite(generatedPath, img)
    print("writing to " + generatedPath)
    num += 1