//import cv from "opencv.js";
// import * as cvstfjs from '@microsoft/customvision-tfjs';

let video = document.getElementById("videoInput"); // video is the id of video tag
let mobile = Boolean;
mobile = false;

if( /Android|android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) ) {
    console.log("Mobile")
    video.width = 480;
    video.height = 640;
} else {
    console.log("Desktop")
    video.width = 640;
    video.height = 480;
}

// video.width = 640;
// video.height = 480;

function showProgress(percentage){
    var pct = Math.floor(percentage*100);
    document.getElementById("modelPercentage").innerText = "Percentage loaded: " + pct + "%";
    console.log("Percentage loaded: " + percentage);
}

async function runWebcamCapture() {

    // Not sure if this is actually needed.
    video.setAttribute('autoplay', '');
    video.setAttribute('muted', '');
    video.setAttribute('playsinline', '');


    let model = new cvstfjs.ObjectDetectionModel();
    await model.loadModelAsync('js/model/model.json', {onProgress: showProgress});

    navigator.mediaDevices.getUserMedia({ video: {facingMode: 'environment',}, audio: false })
        .then(function(stream) {

            video.srcObject = stream;
            video.onloadedmetadata = () => {
                video.play();
            };

            async function process(){

                requestAnimationFrame(() => {
                    draw();
                    process();
                });

                async function draw(){

                    const canvas = document.getElementById("canvasOutput");

                    const ctx = canvas.getContext("2d");

                    canvas.width = video.width
                    canvas.height = video.height

                    ctx.clearRect(0,0, ctx.canvas.width, ctx.canvas.height);
                    ctx.drawImage(video,0, 0,video.width,video.height);

                    const result = await model.executeAsync(video);
                    console.log(result);

                    console.log(result[0]);

                    result[0].forEach(element => {
                        ctx.strokeStyle = "#00FFFF";
                        ctx.lineWidth = 2;
                        // ctx.strokeRect(element[0], element[1], element[2], element[3]);
                        ctx.strokeRect(50, 50, 50, 50);
                    });
                }
                

            }

            setTimeout(process, 0);


                // drawBoxes = predictions => {

                //     const canvas = document.getElementById("canvasOutput");

                //     const ctx = canvas.getContext("2d");

                //     canvas.width = video.width
                //     canvas.height = video.height

                //     ctx.clearRect(0,0, ctx.canvas.width, ctx.canvas.height);

                //     const font = "16px sans-serif";
                //     ctx.font = font;
                //     ctx.textBaseline = "top";
                //     ctx.drawImage(video,0, 0,video.width,video.height);


                //     predictions.forEach(prediction => {

                //         let i = 1;

                //         if (mobile){ i = 1; }

                //         const x = i * prediction.bbox[0];
                //         const y = i * prediction.bbox[1];
                //         const width = i * prediction.bbox[2];
                //         const height = i * prediction.bbox[3];

                //         ctx.strokeStyle = "#00FFFF";
                //         ctx.lineWidth = 2;
                //         ctx.strokeRect(x, y, width, height);

                //         let confidence = prediction.score.toPrecision(2);
                //         let label = prediction.class + " " + confidence;

                //         ctx.fillStyle = "#00FFFF";
                //         const textWidth = ctx.measureText(label).width;
                //         const textHeight = parseInt(font,10);
                //         ctx.fillRect(x,y,textWidth+4, textHeight+4);

                //         ctx.fillStyle = "#000000";
                //         ctx.fillText(label, x, y);

                //     })

            
        })
        .catch(function(err) {
            console.log("An error occurred! " + err);
        });
}

setTimeout(runWebcamCapture, 1000);