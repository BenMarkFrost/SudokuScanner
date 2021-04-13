"""
Benjamin Frost
Individual Project 2021

This file serves as the entry point to the SudokuScanner API
"""

from flask import Flask, request, Response, render_template, send_file, make_response
from flask_cors import CORS, cross_origin
from PIL import Image
from server import sudokuscanner
from server.Frame import Frame
from io import BytesIO
import numpy as np


app = Flask(__name__, 
            static_url_path='', 
            static_folder='public',
            template_folder='public/templates')


# CORS is used to allow for this API to be used when the user is connected to a different domain.
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['CORS_EXPOSE_HEADERS'] = ["x-filename", "x-solution", "x-timeTaken"]


# In deployment, the user will not access the html file through this Flask server but through Firebase.
@app.route('/')
@cross_origin()
def root():
    return render_template("index.html")

# This is the main API entry point
@app.route('/frame', methods=['POST'])
@cross_origin()
def frame():
    try:

        frame_id = request.form.get("id")
        browser_id = request.form.get("browser_id")
        img = Image.open(request.files['frame'])

        img = np.array(img)

        # Image is handed off to the analysis code
        # Returns an instantiation of the Frame class containing all stages of analysis
        frame = sudokuscanner.scan(browser_id, img, frame_id)


        # The following code for compression was taken from the below links:
        # https://stackoverflow.com/questions/10607468/how-to-reduce-the-image-file-size-using-pil
        # https://stackoverflow.com/questions/30771652/how-to-perform-jpeg-compression-in-python-without-writing-reading
        # Credit to Ryan G and Super Engine
        imgIO = BytesIO()
        pilImg = Image.fromarray(frame.outputImage.astype(np.uint8))
        pilImg.save(imgIO, 'JPEG', optimize=True, quality=50)
        imgIO.seek(0)
        # End of reference


        # Packaging up the frame to send back to the client
        returnFile = make_response(send_file(imgIO, mimetype='img/jpeg'))
        returnFile.headers["x-filename"] = frame.frame_id
        returnFile.headers["x-timeTaken"] = frame.timeTaken()
        returnFile.headers["x-solution"] = str(frame.solutionFrame)

        return returnFile

    except Exception as e:
        print("Post /frame error: " + str(e))
        return e


# This API is for returning the solution image of the overlay and original image combined
# This is only used when the user clicks the download button
@app.route('/solution', methods=['POST'])
@cross_origin()
def solution():
    
    try:
        browser_id = request.form.get("solutionRequest")

        print(f"Solution request for browser {browser_id}")

        # Returns the combined solution image
        solution = sudokuscanner.getSolution(browser_id)

        imgIO = BytesIO()
        pilImg = Image.fromarray(solution.astype(np.uint8))
        pilImg.save(imgIO, 'JPEG', quality=100)
        imgIO.seek(0)

        returnFile = make_response(send_file(imgIO, mimetype='img/jpeg'))

        return returnFile
    except Exception as e:
        print("Post /frame error: " + str(e))
        return e

# In-built Flask threading is enabled spawning a new thread for each API request
app.run(host='0.0.0.0', threaded=True)
