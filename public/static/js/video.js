//import cv from "opencv.js";

let video = document.getElementById("videoInput");
let mobile = Boolean;
mobile = false;
let editableStream;
let loaded = false;

if( /Android|android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) ) {
    console.log("Mobile")
    video.width = 480;
    video.height = 640;
} else {
    console.log("Desktop")
    video.width = 640;
    video.height = 480;
}

// @ https://stackoverflow.com/questions/951021/what-is-the-javascript-version-of-sleep
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function runWebcamCapture() {

    while (!(loaded = true)){
        await sleep(50);
    }

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

            if ('requestVideoFrameCallback' in HTMLVideoElement.prototype) {
                console.log("video frame callback supported")
            } else {
                console.log("video frame callback NOT supported")
            }

            async function processFrame(){

                if (!('requestVideoFrameCallback' in HTMLVideoElement.prototype)) {
                    // 1000ms / 15 fps = 67ms
                    await new Promise(r => setTimeout(r, 67));
                }

                // Drawing Original Video
                ctx.clearRect(0,0, ctx.canvas.width, ctx.canvas.height);
                ctx.drawImage(video, 0,0,video.width,video.height);
            
                toAPI(canvas);

                // console.log(data);

                if ('requestVideoFrameCallback' in HTMLVideoElement.prototype) {
                    video.requestVideoFrameCallback(() => {
                        processFrame();
                    })
                } else {
                    requestAnimationFrame(() => {
                        processFrame();
                    })
                }

            }
            
            processFrame();

        })
        .catch(function(err) {
            console.log("An error occurred! " + err);
        });
}

window.addEventListener('load', function () {
    console.log("Loaded");
    // runWebcamCapture();
    loaded = true;
    // setTimeout(runWebcamCapture, 3000);
})




