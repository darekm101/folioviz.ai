// index.html script
var player = videojs('my-video');

// if (player) {
//   player.on('ended', function() {
//     // Click the "Keep it" button
//     document.getElementById("keep-it-button").click();
//   });
// }

player.on('ended', function() {
  // Submit the "Keep it" form
  document.getElementById("keep-it-form").submit();
});

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
