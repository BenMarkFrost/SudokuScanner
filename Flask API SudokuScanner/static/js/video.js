//import cv from "opencv.js";

let video = document.getElementById("videoInput");
let mobile = Boolean;
mobile = false;
let period = 5;
let count = 0;

if( /Android|android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) ) {
    console.log("Mobile")
    video.width = 480;
    video.height = 640;
} else {
    console.log("Desktop")
    video.width = 1000;
    video.height = 750;
}

async function runWebcamCapture() {


    // TODO Specifying framerate doesn't work here
    navigator.mediaDevices.getUserMedia({video: {facingMode: 'environment',}, audio: false })
        .then(function(stream) {

            video.srcObject = stream;
            video.onloadedmetadata = () => {
                video.play();
            };

            const canvas = document.getElementById("canvasInput");
            const ctx = canvas.getContext("2d");
            canvas.width = video.width
            canvas.height = video.height

            function processFrame(){

                count ++;

                if (count % period == 0){

                    // Drawing Original Video
                    ctx.clearRect(0,0, ctx.canvas.width, ctx.canvas.height);
                    ctx.drawImage(video,0, 0,video.width,video.height);
                    
                    let sImg = toAPI(canvas);
                    

                    if (sImg){

                        console.log(sImg)

                        // console.log("Border: " + border);

                        // ctx.drawImage(solutionImg, 0, 0, video.width, video.height);
                        
                        try{
                            let src = new cv.Mat(sImg.height, sImg.width, cv.CV_8UC4);

                            cv.imshow("canvasOutput", src);
                        } catch (error){
                            console.error("Error: " + error);
                        }
                    }

                    // if (border){
                    //     console.log(border[0][0][0] + " " + border[0][0][1]);
                    //     console.log(border[1][0][0] + " " + border[1][0][1]);

                    //     ctx.beginPath();
                    //     ctx.moveTo(border[0][0][0], border[0][0][1]);
                    //     ctx.lineTo(border[1][0][0], border[1][0][1]);
                    //     ctx.lineTo(border[2][0][0], border[2][0][1]);
                    //     ctx.lineTo(border[3][0][0], border[3][0][1]);
                    //     ctx.lineTo(border[0][0][0], border[0][0][1]);

                    //     ctx.lineWidth = 10;
                    //     ctx.strokeStyle = '#ff0000';
                    //     ctx.stroke();
                    // }
                }

                requestAnimationFrame(() => {
                    processFrame();
                })

            }
            
            processFrame();

        })
        .catch(function(err) {
            console.log("An error occurred! " + err);
        });
}

setTimeout(runWebcamCapture, 1000);