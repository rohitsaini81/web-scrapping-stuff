/* listed all apps of uptodown
 step 1 select any random app
https://tiktok-lite.en.uptodown.com/android

step 2 get that download page url form ancor tag inside get latest version download button
https://tiktok.en.uptodown.com/android/download

step 3 extract download token and fetch download link using this function :*/
(function() {
  const token = document.querySelector('#detail-download-button').dataset.url;
  const url = "https://dw.uptodown.net/dwn/" + token;

  const iframe = document.createElement("iframe");
  iframe.style.display = "none";

  iframe.onload = function () {
    console.log("Final URL:", iframe.src);
    document.body.removeChild(iframe);
  };

  iframe.src = url;
  document.body.appendChild(iframe);
})();

