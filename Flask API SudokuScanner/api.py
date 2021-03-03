from flask import Flask, request, Response, render_template, send_file
from PIL import Image
import time
import sudokuscanner
import codecs, json
import cv2
from io import BytesIO
import numpy as np

# TODO Clean up blobs!!

app = Flask(__name__)
# app.config["DEBUG"] = True

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

        # outputImage = np.zeros(np.array(frame).shape)

        # result, encoded = cv2.imencode('.jpg', outputImage, [int(cv2.IMWRITE_JPEG_QUALITY), 5])

        # print(outputImage.shape)

        # Pickle compression?

        # print(outputImage)

        imgIO = BytesIO()
        pilImg = Image.fromarray((outputImage).astype(np.uint8))
        pilImg.save(imgIO, 'JPEG', quality=50)
        imgIO.seek(0)


        returnFile = send_file(imgIO, mimetype='img/jpeg')

        returnFile.headers["x-filename"] = client_id

        # return {"id": client_id, "img": encoded.tolist()}

        return returnFile

    except Exception as e:
        print("Post /frame error: " + str(e))
        return e


app.run(host='0.0.0.0', threaded=True)
