//import cv from "opencv.js";

let video = document.getElementById("videoInput");
let mobile = Boolean;
mobile = false;
let editableStream;

if( /Android|android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) ) {
    console.log("Mobile")
    video.width = 480;
    video.height = 640;
} else {
    console.log("Desktop")
    video.width = 640;
    video.height = 480;
}

async function runWebcamCapture() {

    navigator.mediaDevices.getUserMedia({video: {facingMode: 'environment', frameRate: 15}, audio: false })
        .then(function(stream) {

            editableStream = stream;

            video.srcObject = stream;
            video.onloadedmetadata = () => {
                video.play();
            };

            const canvas = document.getElementById("canvasInput");
            const ctx = canvas.getContext("2d");
            canvas.width = video.width
            canvas.height = video.height

            function processFrame(){

                // Drawing Original Video
                ctx.clearRect(0,0, ctx.canvas.width, ctx.canvas.height);
                ctx.drawImage(video, 0,0,video.width,video.height);
            
                toAPI(canvas);

                // console.log(data);

                video.requestVideoFrameCallback(() => {
                    processFrame();
                })

            }
            
            processFrame();

        })
        .catch(function(err) {
            console.log("An error occurred! " + err);
        });
}

window.addEventListener('load', function () {
    console.log("Loaded");
    runWebcamCapture();
    // setTimeout(runWebcamCapture, 3000);
})




