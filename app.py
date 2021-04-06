# sys.path.insert(1, '/server')
from flask import Flask, request, Response, render_template, send_file, make_response
from flask_cors import CORS, cross_origin
from PIL import Image
import time
from server import sudokuscanner
from server.Frame import Frame
import codecs, json
import cv2
from io import BytesIO
import numpy as np
import sys
from func_timeout import func_timeout, FunctionTimedOut

sys.path.append('../')

# TODO Clean up blobs!!

app = Flask(__name__, 
            static_url_path='', 
            static_folder='public',
            template_folder='public/templates')

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['CORS_EXPOSE_HEADERS'] = ["x-filename", "x-solution", "x-timeTaken"]

# app.config["DEBUG"] = True

@app.route('/')
@cross_origin()
def root():
    return render_template("index.html")

@app.route('/frame', methods=['POST'])
@cross_origin()
def frame():
    try:

        if request.form.get("solutionRequest"):

            browser_id = request.form.get("solutionRequest")

            print("Solution request for browser " + str(browser_id))

            solution = sudokuscanner.getSolution(browser_id)

            imgIO = BytesIO()
            pilImg = Image.fromarray(solution.astype(np.uint8))
            pilImg.save(imgIO, 'JPEG', quality=100)
            imgIO.seek(0)

            returnFile = make_response(send_file(imgIO, mimetype='img/jpeg'))

            return returnFile
            


        frame_id = request.form.get("id")
        browser_id = request.form.get("browser_id")
        img = Image.open(request.files['frame'])

        # print(browser_id)

        img = np.array(img)

        frame = Frame(img, frame_id)

        # try:

        #     outputImage, calculated = sudokuscanner.scan(frame, browser_id, frame_id)
        
        # except FunctionTimedOut:
        #     print("sudokuscanner timed out")
        #     outputImage = np.zeros(img.shape)
        #     calculated = False

        frame = sudokuscanner.scan(browser_id, frame)

        # outputImage = np.zeros(frame.shape)

        # print(frame)

        # print(frame.solutionFrame)


        # Cite this
        imgIO = BytesIO()
        pilImg = Image.fromarray(frame.outputImage.astype(np.uint8))
        pilImg.save(imgIO, 'JPEG', quality=50)
        imgIO.seek(0)

        returnFile = make_response(send_file(imgIO, mimetype='img/jpeg'))
        returnFile.headers["x-filename"] = frame.frame_id
        returnFile.headers["x-timeTaken"] = frame.timeTaken
        returnFile.headers["x-solution"] = str(frame.solutionFrame)

        return returnFile

    except Exception as e:
        print("Post /frame error: " + str(e))
        return e


app.run(host='0.0.0.0', threaded=True)
