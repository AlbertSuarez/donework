function run() {
  var text = document.getElementById('textInput').value;
  var target = document.getElementById('targetDiv');

  converter = new showdown.Converter(),
  html = converter.makeHtml(text);
  target.innerHTML = html;
}

function generateText() {
  var textInput = document.getElementById('textInput');
  var text = textInput.value;
  var temperature_div = document.getElementById('range_temperature');
  var rand = temperature_div.value;

    // Put slider
    document.getElementById("waiting-div").style.display = "inline-block";
    document.getElementById("textInput").style.display  = "none";


  // Set up our HTTP request
  var xhr = new XMLHttpRequest();

  // Setup our listener to process completed requests
  xhr.onload = function () {
    // Process our return data
    if (xhr.status >= 200 && xhr.status < 300) {
      // What do when the request is successful
      console.log('Text generated!');

      var json = JSON.parse(xhr.responseText)
      var generatedText = json.text;
      textInput.value = generatedText;
      document.getElementById("textInput").style.display  = "inline-block";
      document.getElementById("waiting-div").style.display = "none";
      run();
    } else {
      // What do when the request fails
      console.log('The request failed!');
    }
    // Code that should run regardless of the request status
  };
  // Create and send a GET request
  // The first argument is the post type (GET, POST, PUT, DELETE, etc.)
  // The second argument is the endpoint URL
  xhr.open('POST', 'http://35.187.2.140:8080/generate');
  xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
  xhr.send(JSON.stringify({ "text": text , "rand": rand}));
  xhr.send();
}

function openlink(link){
  window.open(link);
}

function download(){
  var textInput = document.getElementById('textInput');
  var text = textInput.value;
  console.log("Text-1: ", text);
  var xhr = new XMLHttpRequest();
  xhr.onload = function(){
    if (xhr.status >= 200 && xhr.status < 300){
      var json = JSON.parse(xhr.responseText);
      var fileLink = json.path;
      openlink(fileLink);
    } else {
      console.log('failed')
    };
  }
  var url = 'http://35.187.2.140:8080/downloadLink';
  xhr.open('POST', url);
  xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
  console.log("text: ", text);
  xhr.send(JSON.stringify({ "text": text }));
}

function generateImage() {
  textInput = document.getElementById('textInput');
  text = textInput.value;
  // Set up our HTTP request
  var xhr = new XMLHttpRequest();

  // Setup our listener to process completed requests
  xhr.onload = function () {
    // Process our return data
    if (xhr.status >= 200 && xhr.status < 300) {
      // What do when the request is successful

      console.log('Image generated!', xhr.responseText);
      var json = JSON.parse(xhr.responseText)
      var imageUrl = json.url;
      // imageUrl = imageUrl.substring(1,imageUrl.length-2)
      textInput.value = text + '\n\n' + '<img src="' + imageUrl + '" style="display:block;margin-left:auto;margin-right:auto;border-radius:10px;" width=300px title="' + json.name +'">';
      run();
    } else {
      // What do when the request fails
      console.log('The request failed!');
    }
    // Code that should run regardless of the request status
  };
  // Create and send a GET request
  // The first argument is the post type (GET, POST, PUT, DELETE, etc.)
  // The second argument is the endpoint URL
  xhr.open('POST', 'http://35.187.2.140:8080/image');
  xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
  xhr.send(JSON.stringify({ "text": text }));
  xhr.send();
}


function make_preview(el) {
  run();
  autoScrollTo(el);
}

function autoScrollTo(el) {
  var top = $("#" + el).offset().top;
  $("html, body").animate({ scrollTop: top }, 1000);
}