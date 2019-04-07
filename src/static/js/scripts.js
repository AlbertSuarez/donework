

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
      textInput.value = text + generatedText;
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
  xhr.open('GET', 'http://0.0.0.0:6969/generate?inputText=' + text);
  xhr.send();
}

function openlink(link){
  window.open(link);
}

function download(){
  var textInput = document.getElementById('textInput');
  var text = textInput.value;
  var xhr = new XMLHttpRequest();
  xhr.onload = function(){
    if (xhr.status >= 200 && xhr.status < 300){
      var link = xhr.responseText;
      console.log(link)
      openlink(link);
    };
    xhr.open('GET', 'http://0.0.0.0:6969/download?inputText='+text)
    xhr.send();
  }
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
  xhr.open('GET', 'http://0.0.0.0:6969/image?text=' + text);
  xhr.send();
}


function make_preview(el) {

  // Esconder texto

  //Poner slider


  run();
  autoScrollTo(el);
}

function autoScrollTo(el) {
  var top = $("#" + el).offset().top;
  $("html, body").animate({ scrollTop: top }, 1000);
}