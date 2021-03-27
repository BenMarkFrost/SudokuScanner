
let frame_id = 0;
let frameBuffer = {};
let latencyTracker = {};
let rollingAverageTracker = [];
let data = [];
let latencyParagraph = document.getElementById("latency");
let best = 1000000;
let worst = 0;
let tempFrame;
var urlCreator = window.URL || window.webkitURL;
let browwser_id = Math.floor(Math.random() * 10000);
let synced = true;

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

    tempFrameRate = 15

    if (latency < 200){
        tempFrameRate = 15
    } else {
        tempFrameRate = 5
    } 

    editableStream.getVideoTracks()[0].applyConstraints({frameRate: tempFrameRate});

    if (latency > worst){
        worst = latency;
    } else if (latency < best){
        best = latency;
    }

    // console.log(sum);

    // console.log(rollingAverageTracker)
    latencyParagraph.innerHTML = "Frame " + id + ": " + latency + "ms latency. Worst: " + worst + ", best: " + best;

}

function upload(frame){

    if (!synced){
        tempFrame = urlCreator.createObjectURL(frame);
        document.querySelector("#video").src = tempFrame;
    }

    frame_id = frame_id + 1;
    let formdata = new FormData();
    formdata.append("frame", frame);
    formdata.append("id", frame_id);
    formdata.append("browser_id", browwser_id);
    
    let xhr = new XMLHttpRequest();
    xhr.open('POST', window.location.origin + '/frame', true);

    xhr.responseType = "blob";
    xhr.onload = function () {
        if (this.status === 200) {
            // let response = JSON.parse(this.response);
            // console.log(response);

            solutionImg = urlCreator.createObjectURL(this.response);

            document.querySelector("#image").src = solutionImg;
            
            displayLatency(xhr.getResponseHeader("x-filename"))

            data.push(solutionImg)

        }
        else{
            console.error(xhr);
        }
    };
    
    if (Object.keys(latencyTracker).length < 20) {
        xhr.send(formdata);
        console.log("Sending " + frame_id);
        latencyTracker[frame_id] = Date.now();
        frameBuffer[frame_id] = frame;

    } else {
        console.error("Waiting on more than 200 frames...")
        frameBugger = []
        latencyTracker = []
    }
}

function toAPI(canvas){

    // TODO add toggle button for frame sync

    // console.log("Found me");

    data = []

    canvas.toBlob(upload, 'image/jpeg');

    // console.log(data);

}

function toggleFrameSync(sw){

    console.log("Frame sync: " + sw.checked);

    synced = sw.checked;


}