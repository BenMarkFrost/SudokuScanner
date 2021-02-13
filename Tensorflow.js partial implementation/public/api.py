from flask import Flask, request, Response, render_template
from PIL import Image
import time
import sudokuscanner

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

        objects = sudokuscanner.scan(frame)


        return {"id": client_id}

    except Exception as e:
        print("Post /frame error: " + str(e))
        return e


app.run()
