// index.html script
console.log("main.js loaded");


var player = videojs('my-video');

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
  }
}

// Function to handle Speed Up button click

function handleSpeedUp() {
  player.playbackRate(player.playbackRate() + 1);
  console.log("Playback rate: " + player.playbackRate());
}

document.addEventListener('DOMContentLoaded', function () {
  // Add keydown event listener
  window.addEventListener('keydown', handleKeyDown);

  // Add click event listener for Speed Up button
  if (document.getElementById('btn-speed-up')) {
    document.getElementById('btn-speed-up').addEventListener('click', handleSpeedUp);
  }
});

document.addEventListener('DOMContentLoaded', function () {
  // Add keydown event listener
  window.addEventListener('keydown', handleKeyDown);

});
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
