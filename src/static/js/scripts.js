

function run() {
  document.getElementById("targetDiv").style.visibility = "visible"; 
  var text = document.getElementById('textInput').value,
      target = document.getElementById('targetDiv'),
      converter = new showdown.Converter(),
      html = converter.makeHtml(text);
    target.innerHTML = html;
}

function generateText() {
  textInput = document.getElementById('textInput');
  text = textInput.value;
  // Set up our HTTP request
  var xhr = new XMLHttpRequest();

  // Setup our listener to process completed requests
  xhr.onload = function () {
    // Process our return data
    if (xhr.status >= 200 && xhr.status < 300) {
      // What do when the request is successful
      console.log('Text generated!');
      textInput.value = text + xhr.responseText;
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


function generateImage() {
  console.log("hola");
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
      textInput.value = text + '\n\n' + xhr.responseText;
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

