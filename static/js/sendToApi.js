
let client_id = 0;
let frameBuffer = {};
let latencyTracker = {};
let rollingAverageTracker = [];
let data = [];
let latencyParagraph = document.getElementById("latency")
let best = 1000000;
let worst = 0;
let tempFrame;
var urlCreator = window.URL || window.webkitURL;

//TODO only play frames once API response received

function displayLatency(id){

    // TODO Display best and worst and average latencies here?

    let timeOfAPICall;

    try{
        timeOfAPICall = latencyTracker[id];
        delete latencyTracker[id];
        // console.log(timeOfAPICall);
        // let d = new Date();
        latency = Date.now() - timeOfAPICall;
        console.log("Received " + id)

        frame = frameBuffer[id];
        delete frameBuffer[id];

        tempFrame = urlCreator.revokeObjectURL(tempFrame)

        tempFrame = urlCreator.createObjectURL(frame);

        document.querySelector("#video").src = tempFrame;

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

    client_id = client_id + 1;
    let formdata = new FormData();
    formdata.append("frame", frame);
    formdata.append("id", client_id)
    
    let xhr = new XMLHttpRequest();
    xhr.open('POST', window.location.origin + '/frame', true);
    xhr.responseType = "blob";
    xhr.onload = function () {
        if (this.status === 200) {
            // let response = JSON.parse(this.response);
            // console.log(response);

            solutionImg = urlCreator.createObjectURL(this.response);

            
            document.querySelector("#image").src = solutionImg;

            // data.push(solutionImg);

            // console.log(this.response)
            
            displayLatency(xhr.getResponseHeader("x-filename"))

            // console.log(xhr.getResponseHeader("x-filename"))

            // returnedImg = this.response;

            // var file = new File([returnedImg], "response.jpg", { type: "image/jpeg", });
            
            // console.log(file);

            // solutionImg = file;

            // console.log("Received " + response["id"]);
            // displayLatency(response["id"]);

            // Make this work for more than one puzzle
            // solutionImg = response["img"]

            // img = this.response
            // console.log(type(img)

            // print(solutionImg)

            // var resp = this.response;
            // var byteArray = new Uint8Array(resp);
            // var str = String.fromCharCode.apply(null, byteArray);
            // var src = "data:image/jpeg;base64," + btoa(str);
            // // console.log(btoa(str));
            // var img = document.createElement("img");
            // img.src = src;


            // let vidOut = document.getElementById("canvasOutput");
            // vidOut.

            // solutionImg = src

            // var img = document.createElement("img");
            // img.src = src;

        }
        else{
            console.error(xhr);
        }
    };
    if (!(Object.keys(latencyTracker).length > 200)) {
        xhr.send(formdata);
        console.log("Sending " + client_id);
        latencyTracker[client_id] = Date.now();
        frameBuffer[client_id] = frame;

    } else {
        console.error("Waiting on more than 200 frames...")
        frameBugger = []
        latencyTracker = []
    }
}

function toAPI(canvas){

    // TODO add toggle button for frame sync

    data = [];

    canvas.toBlob(upload, 'image/jpeg');

    return data;

}