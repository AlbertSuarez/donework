function run() {
  document.getElementById("targetDiv").style.visibility = "visible"; 
  var text = document.getElementById('textInput').value,
      target = document.getElementById('targetDiv'),
      converter = new showdown.Converter(),
      html = converter.makeHtml(text);
    target.innerHTML = html;
}