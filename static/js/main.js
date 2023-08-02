// index.html script
console.log("main.js loaded");

var player = videojs('my-video');

// Global variables to store IN and OUT points
var inPoint = null;
var outPoint = null;

function handleKeyDown(event) {
  // Check which key was pressed
  console.log("Key Pressed:");
  console.log(event.key);
  switch (event.key.toLowerCase()) {
    case 'l': // Keep it
      document.getElementById("btn-keep-it").submit();
      break;
    case 'j': // Back
      document.querySelector('form[action="/previous"]').submit();
      break;
    case 'd': // Delete it
      document.querySelector('form[action="/remove"]').submit();
      break;
  //   case 'i': // IN point
  //     inPoint = player.currentTime();
  //     document.getElementById("in-point").innerText = "IN: " + formatTime(inPoint);
  //     break;
  //   case 'o': // OUT point
  //     outPoint = player.currentTime();
  //     document.getElementById("out-point").innerText = "OUT: " + formatTime(outPoint);
  //     break;
  // }

  case 'i':
    inPoint = player.currentTime();
    // Check if IN point is after OUT point
    if (outPoint !== null || inPoint > outPoint) {
      outPoint = player.duration(); // Set OUT point to the end of the video
      console.log("OUT point is set to the end of the video");
      document.getElementById("out-point").innerText = "OUT: " + formatTime(outPoint); 
    }
    document.getElementById("in-point").innerText = "IN: " + formatTime(inPoint);
    
    break;
  case 'o':
    outPoint = player.currentTime();
    // Check if OUT point is before IN point
    if (inPoint !== null && outPoint < inPoint) {
      outPoint = player.duration(); // Set OUT point to the end of the video
      console.log("OUT point is set to the end of the video");
    }
    document.getElementById("out-point").innerText = "OUT: " + formatTime(outPoint);
    
    break;
  }

  // Enable Trim button if both IN and OUT points are set
  if (inPoint !== null && outPoint !== null) {
    document.getElementById("btn-trim").disabled = false;
  }
}

// Function to format time in MM:SS format
// function formatTime(seconds) {
//   const minutes = Math.floor(seconds / 60);
//   const secs = Math.floor(seconds % 60);
//   return minutes.toString().padStart(2, '0') + ":" + secs.toString().padStart(2, '0');
// }


function formatTime(seconds) {
  const minutes = Math.floor(seconds / 60);
  const secs = Math.floor(seconds % 60);
  const millis = Math.floor((seconds % 1) * 1000); // Getting the milliseconds part
  return minutes.toString().padStart(2, '0') + ":" +
         secs.toString().padStart(2, '0') + "." +
         millis.toString().padStart(3, '0'); // Formatting with 3 digits for milliseconds
}


// Function to handle Speed Up button click
function handleSpeedUp() {
  player.playbackRate(player.playbackRate() * 2);
  console.log("Playback rate: " + player.playbackRate());
}

// Function to handle Trim button click
function handleTrim() {
  if (inPoint !== null && outPoint !== null) {
    // Code to handle trimming between inPoint and outPoint
    // You can add the logic to trim the video here
  }
}

document.addEventListener('DOMContentLoaded', function () {
  // Add keydown event listener
  window.addEventListener('keydown', handleKeyDown);

  // Add click event listener for Speed Up button
  if (document.getElementById('btn-speed-up')) {
    document.getElementById('btn-speed-up').addEventListener('click', handleSpeedUp);
  }

  // Add click event listener for Trim button
  if (document.getElementById('btn-trim')) {
    document.getElementById('btn-trim').addEventListener('click', handleTrim);
  }
});

// Rest of the code...


// player.on('ended', function() {
//   // Submit the "Keep it" form
//   document.getElementById("keep-it-form").submit();
// });

// For index.html
if (document.getElementById("my-video")) {
  const indexPlayer = videojs("my-video");

  indexPlayer.on("ended", function () {
    // Reload the page to autoplay the next video
    location.reload();
  });
}
// play_all.html script
if (typeof video_files !== "undefined") {
  const videos = video_files;
  let videoIndex = 0;

  function playNextVideo() {
    if (videoIndex < videos.length) {
      const currentVideo = videojs.getPlayers()["video" + (videoIndex % 2)];
      const nextVideo = videojs.getPlayers()["video" + ((videoIndex + 1) % 2)];

      currentVideo.el().style.zIndex = 1;
      nextVideo.el().style.zIndex = 0;

      currentVideo.src(videos[videoIndex]);
      currentVideo.currentTime(0);
      currentVideo.load();
      currentVideo.play();

      videoIndex++;
    } else {
      videoIndex = 0;
      playNextVideo();
    }
  }

  document.addEventListener("DOMContentLoaded", function () {
    const video1 = videojs('video0');
    const video2 = videojs('video1');

    video1.on('ended', playNextVideo);
    video2.on('ended', playNextVideo);

    playNextVideo();
  });
}
