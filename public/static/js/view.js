/* 
* This file handles updating and displaying responses from the API.
*/

// HTML elements
let latencyParagraph = document.getElementById("latency");
let timeTakenParagraph = document.getElementById("timeTaken");
let progressParagraph = document.getElementById("progress");
let saveBtn = document.getElementById("saveBtn");
let metricsDiv = document.getElementById("metricsDiv");
let metricsBtn = document.getElementById("metricsDropDownBtn");
let streamDiv = document.getElementById("streamDiv");
let startBtn = document.getElementById("startBtn");
let infoDiv = document.getElementById("infoDiv");
let gifAttribute = document.getElementById("gifAttribute");

// Latency ranges
let best = 1000000;
let worst = 0;

// Misc
let solvedImage = false;


/**
 * This function updates and displays the latency.
 * @param  {int} id
 */
 function displayLatency(id){

    let timeOfAPICall;

    try{
        timeOfAPICall = latencyTracker[id];
        delete latencyTracker[id];
        latency = Date.now() - timeOfAPICall;
        console.log("Received " + id)

    } catch (error) {
        console.error("Could not update latency");
        console.error(error);
    }

    rollingAverageTracker.push(latency)

    if (rollingAverageTracker.length > 10){
        rollingAverageTracker.shift()
    }

    let sum = 0;
    for (i = 0; i < rollingAverageTracker.length; i++){
        sum += rollingAverageTracker[i];
    }

    latency = Math.ceil(sum / rollingAverageTracker.length)

    /*
    * updateFrameRate(latency);
    * In testing this feature was found to change the frame rate too frequently.
    */

    if (latency > worst){
        worst = latency;
    } else if (latency < best){
        best = latency;
    }

    latencyParagraph.innerHTML = "Frame " + id + "<br>" + latency + "ms round trip latency. Worst: " + worst + ", best: " + best;

}

/**
 * This function displays the stored frame based on the id.
 * @param  {int} id
 */
function displayFrame(id){

    try {
        frame = frameBuffer[id];
        delete frameBuffer[id];

        // Clean up old frame file
        tempFrame = urlCreator.revokeObjectURL(tempFrame);

        // Create new frame base on buffer
        tempFrame = urlCreator.createObjectURL(frame);

        if (synced){
            originalImg.src = tempFrame;
        }
    } catch (error) {
        console.error("Could not update frame");
        console.error(error);
    }

}
/**
 * This function updates the timeTaken metric.
 * @param  {int} timeTaken
 */
function displayTimeTaken(timeTaken){

    timeTakenParagraph.innerHTML = "Server processing time: " + timeTaken + "ms";

}


/**
 * This function updates the state of the server on solving the presented sudoku.
 * @param  {Boolean} calculated
 */
function displaySolutionProgress(calculated){

    if (solvedImage == false){

        if (calculated == "True"){

            console.log("Solution found");

            solvedImage = true;

            progressParagraph.innerHTML = outputText = "<b>Sudoku solution has been found, click here to download: <b>"
            saveBtn.hidden = false
        }
    }
}

/**
 * This function removes the stalled state gif.
 */
function responseReceived(){

    console.log("Connected to server");

    gifAttribute.hidden = true;
    loadingGif.hidden = true;
    originalImg.hidden = false;
    responseImg.hidden = false;

}

/**
 * This function hides the ability to download the solved image.
 */
function hideDownloadButton(){

    if (solutionImage.img == null){
        progressParagraph.innerHTML = outputText = ""
        saveBtn.hidden = true
        solvedImage = false;
    }

}
/**
 * This function toggles the use of the frame buffer.
 * @param  {Boolean} sw
 */
function toggleFrameSync(sw){

    console.log("Frame sync: " + sw.checked);

    synced = sw.checked;

}


/**
 * The following code toggles the debug section of the web page.
 */
 function toggleMetrics(){

    console.log("Clicked toggle metrics")

    if (metricsDiv.hidden == true){
        metricsDiv.hidden = false;
        metricsBtn.innerHTML = "Hide debug metrics";
    } else {
        metricsDiv.hidden = true;
        metricsBtn.innerHTML = "Show debug metrics";
    }

}


/**
 * This function handles setting the UI to the started or stopped state
 * @param {Boolean} state 
 */
 function toggleState(state){

    stopped = !state;

    startBtn.hidden = state;
    infoPara.hidden = state;

    metricsBtn.hidden = !state;
    stopBtn.hidden = !state;
    gifAttribute.hidden = !state;
    loadingGif.hidden = !state;

    metricsDiv.hidden = true;
    metricsBtn.innerHTML = "Show debug metrics";

    originalImg.hidden = true;
    responseImg.hidden = true;
    streamDiv.hidden = true;

    firstMessage = true;

}



/* The following code is referenced from the below link:
 * https://stackoverflow.com/questions/3916191/download-data-url-file
 * credit to owencm
 */ 
function downloadURI(uri, name) {
    var link = document.createElement("a");
    link.download = name;
    link.href = uri;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    delete link;
}
// End of reference

