//import cv from "opencv.js";

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

            const canvas = document.getElementById("canvasInput");
            const ctx = canvas.getContext("2d");
            canvas.width = video.width
            canvas.height = video.height

            // const canvasOut = document.getElementById("canvasOutput");
            // const ctxOut = canvasOut.getContext("2d");
            // canvasOut.width = video.width;
            // canvasOut.height = video.height;

            const indexOfMaxValue = (a, t = i => i) =>
            a.reduce((iMax, x, i, arr) => (t(x) > t(arr[iMax]) ? i : iMax), 0);

            const arrayRotate = (arr, count) => {
                count -= arr.length * Math.floor(count / arr.length);
                arr.push.apply(arr, arr.splice(0, count));
                return arr;
              };
              
              // takes an array of coordinates and rotate them to that the
              // top-right corner comes first
            const rotateTopRightFirst = coords => {
                // find the top left coord index.
                const pairs = [];
                for (let i = 0; i < 4; i++) {
                  pairs[i] = [coords[i * 2], coords[i * 2 + 1]];
                }
                const bottomRight = indexOfMaxValue(pairs, p =>
                  Math.sqrt(p[0] * p[0] + p[1] * p[1])
                );
                if (bottomRight !== 1) {
                  const shift = -(1 - bottomRight);
                  const newCoords = arrayRotate(coords, shift * 2);
                  return newCoords;
                } else {
                  return coords;
                }
            };


            function findSquare(src){

                const countourImageBuffer = cv.Mat.zeros(src.rows, src.cols, cv.CV_8UC3);
                const contours = new cv.MatVector();
                const hierarchy = new cv.Mat();

                cv.findContours(src, contours, hierarchy,cv.RETR_CCOMP,cv.CHAIN_APPROX_SIMPLE);

                const color = index =>
                    new cv.Scalar(
                    (Math.sin(index) + 1.5) * 100,
                    (Math.cos(index) + 1.5) * 100,
                    0
                    );

                const rectangles = [];
                for (let i = 0; i < contours.size(); ++i) {
                    const contour = contours.get(i);
                    const approximatedContour = new cv.Mat();
                    cv.approxPolyDP(contour, approximatedContour, 10, true);
                
                    // is it a rectangle contour?
                    if (approximatedContour.size().height === 4) {
                        rectangles.push({
                            coord: Array.from(approximatedContour.data32S),
                            area: cv.contourArea(approximatedContour)
                        });
                    }

                    cv.drawContours(
                        countourImageBuffer,
                        contours,
                        i,
                        color(approximatedContour.size().height),
                        1,
                        cv.LINE_8,
                        hierarchy,
                        0
                    );

                    approximatedContour.delete();
                }
          
                contours.delete();
                hierarchy.delete();

                if (rectangles.length === 0) {
                    return { countourImage: countourImageBuffer };
                }

                const idx = indexOfMaxValue(rectangles, r => r.area);
                return {
                    coords: rotateTopRightFirst(rectangles[idx].coord),
                    countourBuffer: countourImageBuffer
                };

            }

            function processFrame(){

                // Drawing Original Video
                ctx.clearRect(0,0, ctx.canvas.width, ctx.canvas.height);
                ctx.drawImage(video,0, 0,video.width,video.height);
                
                let src = cv.imread('canvasInput')

                try {
                    cv.cvtColor(src, src, cv.COLOR_RGBA2GRAY, 0);
                } catch (error) {
                    processFrame()
                    return;
                }

                cv.adaptiveThreshold(src, src, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 2, 5);

                let contours = findSquare(src);
                
                let ctMat;

                try {

                    if (contours.length > 1) {
                        ctMat = contours.countourBuffer;
                    } else {
                        ctMat = contours.countourImage;
                    }

                    console.log(ctMat);

                    cv.imshow('canvasOutput', src);

                    ///

                    // const tmp = new cv.Mat(ctMat);

                    cv.cvtColor(ctMat, ctMat, cv.COLOR_RGB2RGBA);

                    const imgData = new ImageData(
                        new Uint8ClampedArray(ctMat.data),
                        ctMat.cols,
                        ctMat.rows
                    );

                    ctx.putImageData(imgData, 0, 0);
                    ctMat.delete();

                } catch (error) {
                        
                }
                ///

                src.delete();
                
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