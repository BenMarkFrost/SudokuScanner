/**
 * This file contains the setup code for the sudokuscanner web page.
 */

let video = document.getElementById("videoInput");
let originalImg = document.getElementById("video");
let responseImg = document.getElementById("image");
let loadingGif = document.getElementById("loadingGif");
let mobile = false;
let editableStream;
let loaded = false;
let frameRate = 15;
let callback = false;

/**The following code is references from the below link:
 * https://dev.to/timhuang/a-simple-way-to-detect-if-browser-is-on-a-mobile-device-with-javascript-44j3
 * Credit to Timothy Huang
*/
if(/Android|android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) ) {
    console.log("Mobile")
    video.width = 480;
    video.height = 640;
} else {
    console.log("Desktop")
    video.width = 640;
    video.height = 480;
}
// End of reference.


/**The below code is referenced from the below link:
 * https://stackoverflow.com/questions/951021/what-is-the-javascript-version-of-sleep
 * Credit to Gsamaras
*/
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

/**
 * This function initialises the system once the start button is clicked.
 * 
 */
async function runWebcamCapture() {

    // Ensuring all elements of the web page are loaded
    while (!(loaded = true)){
        console.log("Waiting for web page to load...")
        await sleep(50);
    }


    gifAttribute.hidden = false;
    loadingGif.hidden = false;

    /**Initialising WebRTC
    * The below code is adapted from the below link:
    * https://webrtchacks.com/webrtc-cv-tensorflow/
    * Despite this, significant changes have been made to the code for this project.
    */
    navigator.mediaDevices.getUserMedia({video: {facingMode: 'environment', frameRate: frameRate}, audio: false })
        .then(function(stream) {

            editableStream = stream;

            video.srcObject = stream;
            video.onloadedmetadata = () => {
                video.play();
            };

            // The users video is accessed through a canvas element, but it is hidden immediately.
            const canvas = document.getElementById("canvasInput");
            const ctx = canvas.getContext("2d");
            canvas.width = video.width
            canvas.height = video.height
    // End of reference


            /* Determining if the browser supports absolute frame rate access.
            * The below code is referenced from the below link:
            * https://web.dev/requestvideoframecallback-rvfc/
            */
            if ('requestVideoFrameCallback' in HTMLVideoElement.prototype) {
                callback = true;
                console.log("video frame callback supported")
            } else {
                console.log("video frame callback NOT supported")
            }
            // End of reference

            async function processFrame(){

                if (!callback) {
                    // 1000ms / 15 fps = 67ms
                    await new Promise(r => setTimeout(r, 67));
                }

                // Drawing Original Video
                ctx.clearRect(0,0, ctx.canvas.width, ctx.canvas.height);
                ctx.drawImage(video, 0,0,video.width,video.height);
            
                toAPI(canvas);

                if (callback) {
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
    loaded = true;
})


/**
 * This function initiates the system.
 */
 function startStreaming(){

    startBtn.hidden = true
    streamDiv.hidden = false;
    metricsBtn.hidden = false;

    runWebcamCapture();

}