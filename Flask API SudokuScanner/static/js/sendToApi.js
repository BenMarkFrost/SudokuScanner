
let client_id = 0;
let latencyTracker = {};
let rollingAverageTracker = [];
let border;
let latencyParagraph = document.getElementById("latency")

function displayLatency(id){

    // TODO Display best and worst and average latencies here?

    let timeOfAPICall;

    try{
        timeOfAPICall = latencyTracker[id];
        delete latencyTracker[id];
        // console.log(timeOfAPICall);
        // let d = new Date();
        latency = Date.now() - timeOfAPICall;

        
    } catch (error) {
        console.error("Response without API call");
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

    latency = sum / rollingAverageTracker.length

    // console.log(sum);

    // console.log(rollingAverageTracker)
    latencyParagraph.innerHTML = "Frame " + id + ": " + Math.ceil(latency) + "ms latency";

}

function upload(frame){

    client_id = client_id + 1;
    let formdata = new FormData();
    formdata.append("frame", frame);
    formdata.append("id", client_id)
    // formdata.append("threshold", scoreThreshold);
 
    let xhr = new XMLHttpRequest();
    xhr.open('POST', window.location.origin + '/frame', true);
    xhr.onload = function () {
        if (this.status === 200) {
            let response = JSON.parse(this.response);
            // console.log(response);

            console.log("Received " + response["id"]);
            displayLatency(response["id"]);

            // Make this work for more than one puzzle
            border = response["border"]

            // console.log(border);

            // displayBorder(border);


            // console.log(response["id"])
 
            // console.log("Almost parsing");

        }
        else{
            console.error(xhr);
        }
    };
    if (!(Object.keys(latencyTracker).length > 20)) {
        xhr.send(formdata);
        console.log("Sending " + client_id);
        // let d = new Date();
        latencyTracker[client_id] = Date.now();
        // console.log(latencyTracker);
    } else {
        console.error("Waiting on more than 20 frames...")
    }
}

function toAPI(canvas){

    canvas.toBlob(upload, 'image/jpeg');

    return border;

}