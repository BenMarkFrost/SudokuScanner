//import cv from "opencv.js";

let video = document.getElementById("videoInput"); // video is the id of video tag
let mobile = Boolean;
mobile = false;

if( /Android|android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) ) {
    console.log("Mobile")
//     // video.width = screen.availWidth;
//     // video.height = (video.width / 3) * 4;
//     mobile = true;
    video.width = 480;
    video.height = 640;
} else {
    console.log("Desktop")
//     // video.height = screen.availHeight;
//     // video.width = (video.height / 3) * 4;
    video.width = 640;
    video.height = 480;
}

async function runWebcamCapture() {

    // Not sure if this is actually needed.
    video.setAttribute('autoplay', '');
    video.setAttribute('muted', '');
    video.setAttribute('playsinline', '');


    navigator.mediaDevices.getUserMedia({ video: {facingMode: 'environment',}, audio: false })
        .then(function(stream) {

            video.srcObject = stream;
            video.onloadedmetadata = () => {
                video.play();
            };

            cocoSsd.load().then(model => {
                
                
                function process(){

                    model.detect(video).then(predictions => {
                        console.log('Predictions: ', predictions);
                        drawBoxes(predictions);
                        requestAnimationFrame(() => {
                            process();
                        })
                    })
    
                    drawBoxes = predictions => {

                        const canvas = document.getElementById("canvasOutput");

                        const ctx = canvas.getContext("2d");

                        canvas.width = video.width
                        canvas.height = video.height

                        ctx.clearRect(0,0, ctx.canvas.width, ctx.canvas.height);

                        const font = "16px sans-serif";
                        ctx.font = font;
                        ctx.textBaseline = "top";
                        ctx.drawImage(video,0, 0,video.width,video.height);


                        predictions.forEach(prediction => {

                            let i = 1;

                            if (mobile){ i = 1; }

                            const x = i * prediction.bbox[0];
                            const y = i * prediction.bbox[1];
                            const width = i * prediction.bbox[2];
                            const height = i * prediction.bbox[3];

                            ctx.strokeStyle = "#00FFFF";
                            ctx.lineWidth = 2;
                            ctx.strokeRect(x, y, width, height);

                            let confidence = prediction.score.toPrecision(2);
                            let label = prediction.class + " " + confidence;

                            ctx.fillStyle = "#00FFFF";
                            const textWidth = ctx.measureText(label).width;
                            const textHeight = parseInt(font,10);
                            ctx.fillRect(x,y,textWidth+4, textHeight+4);

                            ctx.fillStyle = "#000000";
                            ctx.fillText(label, x, y);

                        })



                    }

                    // setTimeout(process, 1000/FPS);
                }
    
                setTimeout(process, 0);

            })
            
        })
        .catch(function(err) {
            console.log("An error occurred! " + err);
        });
}

setTimeout(runWebcamCapture, 1000);