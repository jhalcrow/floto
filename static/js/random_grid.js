var block_size = 240;
var base = 'http://www.ournewballandchain.com';

function addImage(src) {
  var c=document.getElementById("floto_display");
  var ctx=c.getContext("2d");
  var width = c.clientWidth;
  var height = c.clientHeight;

  var blocks_height = Math.floor(height / block_size);
  var blocks_width = Math.floor(width / block_size);

  var block_i = Math.floor(Math.random() * blocks_height);
  var block_j = Math.floor(Math.random() * blocks_width);


  var img = new Image();
  img.src = src;

  ctx.drawImage(img, block_j * block_size, block_i * block_size, block_size, block_size);
}

function initImages() {
  var xhr = new XMLHttpRequest();
  var url = base + '/floto/api/events/test/tip?n=15'
  xhr.onload = function() {
    imgArr = JSON.parse(this.responseText);
    for(var imgIdx in imgArr.photos) {
      addImage(imgArr.photos[imgIdx].url);
    }
  };
  xhr.open('GET', url, true);
  xhr.send();
}

function updateImage() {
  var xhr = new XMLHttpRequest();
  var url = base + '/floto/api/events/test/new?n=3'
  xhr.onload = function() {
    imgArr = JSON.parse(this.responseText);
    console.log("Got " + imgArr.photos.length + " images.");
    for(var imgIdx in imgArr.photos) {
      var imgUrl = imgArr.photos[imgIdx].url;
      addImage(imgUrl);
      console.log("Adding " + imgUrl);
    }
  };
  xhr.open('GET', url, true);
  xhr.send();
}