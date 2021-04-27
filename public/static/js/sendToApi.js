/*
* This file handles the connection to the API and streaming of video data
*/

// Buffers
let frameBuffer = {};
let latencyTracker = {};
let rollingAverageTracker = [];

// Booleans determining the state of the system
let synced = true;
let stalled = false;
let firstMessage = true;
let debug = false;

// Misc variables
let frame_id = 0;
let tempFrame;
var urlCreator = window.URL || window.webkitURL;
let browser_id = Math.floor(Math.random() * 10000);
let solutionImage = {img: null, timeReceived: 0};
let stalledNum = 0;
let domain;


// When debugging, use the window URL for API requests.
// Otherwise, use CORS to access the Cloud Run instance directly.
if (debug == true){
    domain = window.location.origin;
} else{
    domain = 'https://sudokuscanner-jy7atdmmqq-nw.a.run.app';
}

/**
 * This method updates the frame rate according to the latency.
 * @param  {int} latency
 */
function updateFrameRate(latency){
    let newFrameRate;

    if (latency < 150){
        newFrameRate = 15
    } else {
        newFrameRate = 5
    } 

    if (frameRate != newFrameRate){
        console.log("Updating frame rate to " + newFrameRate)
        frameRate = newFrameRate;
        editableStream.getVideoTracks()[0].applyConstraints({frameRate: frameRate});
    }
}

/**
 * This function handles sending frames of video to and from the API.
 * @param  {Blob} frame
 */
function upload(frame){

    if (!synced){
        tempFrame = urlCreator.createObjectURL(frame);
        originalImg.src = tempFrame;
    }

    if (stalled == true){
        if (stalledNum < 100){
            console.log("Stalled - Waiting for server to start");
            stalledNum = stalledNum + 1;
            return
        } else {
            stalledNum = 0
        }
    }

    // The default state is stalled, however this is enabled here to avoid waiting in the code above.
    // This is since the base assusmption is that the server is running properly, and if it is not then
    // stalled can enter its loop.
    if (firstMessage == true){
        stalled = true;
        firstMessage = false;
    }


    frame_id = frame_id + 1;

    /*
    * The following code is referenced from the below link:
    * https://webrtchacks.com/webrtc-cv-tensorflow/
    * Credit to Chad Hart
    * 
    * Despite this, significant changes have been made for this project.
    */
    let formdata = new FormData();
    formdata.append("frame", frame);
    formdata.append("id", frame_id);
    formdata.append("browser_id", browser_id);
    
    let xhr = new XMLHttpRequest();
    xhr.open('POST', domain + '/frame', true);

    xhr.responseType = "blob";
    xhr.onload = function () {
        if (this.status === 200) {
    // End of refrerence

            solutionImg = urlCreator.createObjectURL(this.response);

            responseImg.src = solutionImg;

            if (stopped) return;

            if (stalled == false){

                response_frame_id = xhr.getResponseHeader("x-filename")

                displayLatency(response_frame_id)
                displayFrame(response_frame_id)

                displayTimeTaken(xhr.getResponseHeader("x-timeTaken"));

                displaySolutionProgress(xhr.getResponseHeader("x-solution"));

            } else {
                stalled = false
                responseReceived();
            }

        }
        else{
            console.error(xhr);
        }
    };
    
    if (Object.keys(frameBuffer).length < 100 || stalled) {
        xhr.send(formdata);
        console.log("Sending " + frame_id);
        latencyTracker[frame_id] = Date.now();
        frameBuffer[frame_id] = frame;
    } else {
        console.error("Waiting on more than 100 frames...")
        stalled = true;
        loadingGif.hidden = false;
        gifAttribute.hidden = false;
        originalImg.hidden = true;
        responseImg.hidden = true;
        hideDownloadButton();
        frameBuffer = {};
        latencyTracker = {};
        
    }
}

/**
 * This function handles accessing the solution image from the API.
 */
function requestSolutionImage(){

    /*
    * The following code is referenced from the below link:
    * https://webrtchacks.com/webrtc-cv-tensorflow/
    * Credit to Chad Hart
    * 
    * Despite this, significant changes have been made for this project.
    */
    let formdata = new FormData();
    formdata.append("solutionRequest", browser_id);

    let xhr = new XMLHttpRequest();
    xhr.open('POST', domain + '/solution', true);

    xhr.responseType = "blob";
    xhr.onload = function () {
        if (this.status === 200) {
    // End of reference

            solutionImage.img = urlCreator.createObjectURL(this.response);

            solutionImage.timeReceived = Date.now();
        
            console.log("solution received")

            saveBtn.innerHTML = "Save Solution";

            downloadSolution();

        }
        else{
            console.error(xhr);
        }

    };

    xhr.send(formdata);
    saveBtn.innerHTML = "Waiting for server...";
}


/**
 * This function saves the retrieved solution image to the user's device.
 */
function downloadSolution(){

    console.log("Clicked download");

    timeDifference = Date.now() - solutionImage.timeReceived;

    console.log(timeDifference);

    if (timeDifference > 3000 || timeDifference < 0){
        requestSolutionImage();
    } else {

        console.log("saving image");

        downloadURI(solutionImage.img, "sudokuSolution.jpg");
    }

}

/**
 * This function is called per frame as the entry point to this file from video.js
 * @param  {DOM element} canvas
 */
function toAPI(canvas){

    canvas.toBlob(upload, 'image/jpeg', 0.5);

}