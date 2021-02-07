//import cv from "opencv.js";

let video = document.getElementById("videoInput"); // video is the id of video tag

if( /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) ) {
    console.log("Mobile")
    video.width = 480;
    video.height = 640;
} else {
    console.log("Desktop")
    console.log(screen.availHeight)
    console.log(screen.height)
    console.log(screen.height * 0.96)
    video.height = screen.availHeight;
    video.width = (video.height / 3) * 4;
}

// video.width = 640;
// video.height = 480;

function runWebcamCapture() {

    let src = new cv.Mat(video.height, video.width, cv.CV_8UC4);
    let dst = new cv.Mat(video.height, video.width, cv.CV_8UC1);
    let cap = new cv.VideoCapture(video)

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

            const FPS = 30

            cocoSsd.load().then(model => {
                
                
                function process(){
                    // cap.read(src)
                    // cv.cvtColor(src, dst, cv.COLOR_RGBA2GRAY);
                    // cv.imshow("canvasOutput", dst)

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

                            const x = prediction.bbox[0];
                            const y = prediction.bbox[1];
                            const width = prediction.bbox[2];
                            const height = prediction.bbox[3];

                            ctx.strokeStyle = "#00FFFF";
                            ctx.lineWidth = 2;
                            ctx.strokeRect(x, y, width, height);

                            ctx.fillStyle = "#00FFFF";
                            const textWidth = ctx.measureText(prediction.class).width;
                            const textHeight = parseInt(font,10);
                            ctx.fillRect(x,y,textWidth+4, textHeight+4);

                            ctx.fillStyle = "#000000";
                            ctx.fillText(prediction.class, x, y);

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