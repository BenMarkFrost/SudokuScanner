const video = document.getElementById("videoInput");

// Create a objectDetector object
const objectDetector = ml5.objectDetector('cocossd', modelLoaded);

// When the model is loaded
function modelLoaded() {
  console.log("Model Loaded!");
}

// Detect objects in the video element
objectDetector.detect(function(err, results) {
  console.log(results); // Will output bounding boxes of detected objects
});