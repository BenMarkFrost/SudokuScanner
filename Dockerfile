FROM tensorflow/tensorflow

WORKDIR /app

COPY requirements.txt ./

RUN pip3 -m pip install --upgrade pip

RUN pip3 install -r requirements.txt

RUN apt-get update

RUN apt-get install ffmpeg libsm6 libxext6  -y

COPY . .

ENV PORT=5000

EXPOSE 5000

CMD ["python3", "app.py"]
