from flask import Flask, request, Response, render_template, send_file
from PIL import Image
import time
import sudokuscanner
import codecs, json
import cv2
from io import BytesIO
import numpy as np


app = Flask(__name__)
app.config["DEBUG"] = True

# for CORS
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST') # Put any other methods you need here
    return response

@app.route('/')
def root():
    return render_template("index.html")

@app.route('/frame', methods=['POST'])
def frame():
    try:

        client_id = request.form.get("id")
        frame = Image.open(request.files['frame'])

        # solutionData = sudokuscanner.scan(frame)

        outputImage = sudokuscanner.scan(frame)

        # result, encoded = cv2.imencode('.jpg', outputImage, [int(cv2.IMWRITE_JPEG_QUALITY), 5])

        # print(outputImage.shape)

        # Pickle compression?

        # print(outputImage)

        imgIO = BytesIO()
        pilImg = Image.fromarray((outputImage).astype(np.uint8))
        pilImg.save(imgIO, 'JPEG', quality=100)
        imgIO.seek(0)


        returnFile = send_file(imgIO, mimetype='img/jpeg')

        returnFile.headers["x-filename"] = client_id

        # return {"id": client_id, "img": encoded.tolist()}

        return returnFile

    except Exception as e:
        print("Post /frame error: " + str(e))
        return e


app.run(threaded=True)
