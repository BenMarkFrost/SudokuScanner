
let frame_id = 0;
let frameBuffer = {};
let latencyTracker = {};
let rollingAverageTracker = [];
let latencyParagraph = document.getElementById("latency");
let timeTakenParagraph = document.getElementById("timeTaken");
let progressParagraph = document.getElementById("progress");
let saveBtn = document.getElementById("saveBtn");
let metricsDiv = document.getElementById("metricsDiv");
let metricsBtn = document.getElementById("metricsDropDownBtn");
let streamDiv = document.getElementById("streamDiv");
let startBtn = document.getElementById("startBtn");
let infoDiv = document.getElementById("infoDiv");
let best = 1000000;
let worst = 0;
let tempFrame;
var urlCreator = window.URL || window.webkitURL;
let browser_id = Math.floor(Math.random() * 10000);
let synced = true;
let solvedImage = false;
let solutionImage = {img: null, timeReceived: 0};
let stalled = false;
let stalledNum = 0;

let cloudRunDomain = 'https://sudokuapp-jy7atdmmqq-ew.a.run.app';

//TODO only play frames once API response received

function displayLatency(id){

    // TODO Display best and worst and average latencies here?

    let timeOfAPICall;

    try{
        timeOfAPICall = latencyTracker[id];
        delete latencyTracker[id];
        latency = Date.now() - timeOfAPICall;
        console.log("Received " + id)

        frame = frameBuffer[id];
        delete frameBuffer[id];

        tempFrame = urlCreator.revokeObjectURL(tempFrame)

        tempFrame = urlCreator.createObjectURL(frame);

        if (synced){
            document.querySelector("#video").src = tempFrame;
        }

        // data.push(tempFrame);

    } catch (error) {
        console.error(error);
    }

    rollingAverageTracker.push(latency)

    // Can this be optimised with splicing?
    if (rollingAverageTracker.length > 10){
        rollingAverageTracker.shift()
    }

    let sum = 0;
    // Make this a lambda expression?
    for (i = 0; i < rollingAverageTracker.length; i++){
        sum += rollingAverageTracker[i];
    }

    latency = Math.ceil(sum / rollingAverageTracker.length)

    // tempFrameRate = 15

    // if (latency < 200){
    //     tempFrameRate = 15
    // } else {
    //     tempFrameRate = 5
    // } 

    // editableStream.getVideoTracks()[0].applyConstraints({frameRate: tempFrameRate});

    if (latency > worst){
        worst = latency;
    } else if (latency < best){
        best = latency;
    }

    // console.log(sum);

    // console.log(rollingAverageTracker)
    latencyParagraph.innerHTML = "Frame " + id + "<br>" + latency + "ms round trip latency. Worst: " + worst + ", best: " + best;

}

function displayTimeTaken(timeTaken){

    outputText =  "Server processing time: " + timeTaken + "ms";

    timeTakenParagraph.innerHTML = outputText

}

function displaySolutionProgress(calculated){

    // console.log("iscalculated: " + calculated);

    if (solvedImage == false){

        // console.log(calculated)
        if (calculated == "True"){

            console.log("Solution found");

            solvedImage = true;

            progressParagraph.innerHTML = outputText = "<b>Sudoku solution has been found, click here to download: <b>"
            saveBtn.hidden = false
        }
    }
}

function upload(frame){

    if (!synced){
        tempFrame = urlCreator.createObjectURL(frame);
        document.querySelector("#video").src = tempFrame;
    }

    if (stalled == true){
        // console.log("stalled");
        if (stalledNum < 100){
            stalledNum = stalledNum + 1;
            return
        } else {
            stalledNum = 0
        }
    }

    frame_id = frame_id + 1;
    let formdata = new FormData();
    formdata.append("frame", frame);
    formdata.append("id", frame_id);
    formdata.append("browser_id", browser_id);
    
    let xhr = new XMLHttpRequest();
    // xhr.open('POST', window.location.origin + '/frame', true);
    xhr.open('POST', cloudRunDomain + '/frame', true);

    xhr.responseType = "blob";
    xhr.onload = function () {
        if (this.status === 200) {
            // let response = JSON.parse(this.response);
            // console.log(response);

            solutionImg = urlCreator.createObjectURL(this.response);

            document.querySelector("#image").src = solutionImg;
            
            // Do I need 'x-'?
            displayLatency(xhr.getResponseHeader("x-filename"), xhr.getResponseHeader("x-timeTaken"))

            displayTimeTaken(xhr.getResponseHeader("x-timeTaken"));

            displaySolutionProgress(xhr.getResponseHeader("x-solution"));

            stalled = false

        }
        else{
            console.error(xhr);
        }
    };
    
    if (Object.keys(frameBuffer).length < 20 || stalled) {
        xhr.send(formdata);
        console.log("Sending " + frame_id);
        latencyTracker[frame_id] = Date.now();
        frameBuffer[frame_id] = frame;
    } else {
        console.error("Waiting on more than 20 frames...")
        stalled = true;
        hideDownloadButton();
        frameBuffer = {};
        latencyTracker = {};
    }
}

function hideDownloadButton(){

    if (solutionImage.img == null){
        progressParagraph.innerHTML = outputText = ""
        saveBtn.hidden = true
        solvedImage = false;
    }

}

function toAPI(canvas){

    // TODO add toggle button for frame sync

    // console.log("Found me");

    canvas.toBlob(upload, 'image/jpeg', 0.5);

    // console.log(data);

}

function toggleFrameSync(sw){

    console.log("Frame sync: " + sw.checked);

    synced = sw.checked;

}

// @ owencm https://stackoverflow.com/questions/3916191/download-data-url-file
function downloadURI(uri, name) {
    var link = document.createElement("a");
    link.download = name;
    link.href = uri;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    delete link;
}

function requestSolutionImage(){

    let formdata = new FormData();
    formdata.append("solutionRequest", browser_id);
    
    let xhr = new XMLHttpRequest();
    xhr.open('POST', cloudRunDomain + '/frame', true);

    xhr.responseType = "blob";
    xhr.onload = function () {
        if (this.status === 200) {

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

function startStreaming(){

    infoDiv.hidden = true;
    startBtn.hidden = true
    streamDiv.hidden = false;
    metricsBtn.hidden = false;

    runWebcamCapture();

}