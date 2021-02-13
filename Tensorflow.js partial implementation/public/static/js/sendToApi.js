
let client_id = 0;
let latencyTracker = {};
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
        latencyParagraph.innerHTML = "Frame " + id + " : " + latency;
    } catch (error) {
        console.error("Response without API call");
    }

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
        console.log(latencyTracker);
    } else {
        console.error("Waiting on more than 20 frames...")
    }

}

function toAPI(canvas){

    canvas.toBlob(upload, 'image/jpeg');

}