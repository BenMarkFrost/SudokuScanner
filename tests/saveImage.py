
from pathlib import Path
import cv2

directory = "cache/"
highestNumber = {}

def saveImg(folder, img):

    global highestNumber
    
    if folder in highestNumber:
        # print("Folder has highest file num")
        num = highestNumber[folder]
    else:
        print("Adding new folder to dict")
        num = 0

    generatedPath = ""  

    while True:
        generatedPath = directory + folder + "/" + folder + str(num) + ".jpg"
        myFile = Path(generatedPath)
        if myFile.is_file():
            num = num + 1
        else:
            break

    highestNumber[folder] = num

    cv2.imwrite(generatedPath, img)
    print("writing to " + generatedPath)
    num = num + 1