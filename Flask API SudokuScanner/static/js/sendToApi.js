
let client_id = 0;
let latencyTracker = {};
let rollingAverageTracker = [];
let solutionImg;
let latencyParagraph = document.getElementById("latency")
let best;
let worst;

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
    xhr.responseType = "blob";
    xhr.onload = function () {
        if (this.status === 200) {
            // let response = JSON.parse(this.response);
            // console.log(response);

            var urlCreator = window.URL || window.webkitURL;
            solutionImg = urlCreator.createObjectURL(this.response);

            console.log(this.response)
            
            console.log(xhr.getResponseHeader("x-filename"))

            displayLatency(xhr.getResponseHeader("x-filename"))

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

    return solutionImg;

}