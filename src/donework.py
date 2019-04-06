from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import requests
from  src.gpt_2.src.interactive_conditional_samples import generateSample

GOOGLE_API_KEY = "AIzaSyBsgu9EkHIcsCQJJyiia1qH1WCtmWrLFvA"
GOOGLE_API_CX = "011903039758982039198:szvtofg-7gg"
GOOGLE_API_URL = "https://www.googleapis.com/customsearch/v1"

flask_app = Flask(__name__, template_folder='templates/')
CORS(flask_app)


@flask_app.route('/')
def index():
    return render_template('index.html')


@flask_app.route('/image')
def image():      
    imageName = request.args.get('imageName')
    # defining a params dict for the parameters to be sent to the API 
    PARAMS = {
        'key': GOOGLE_API_KEY,
        'cx': GOOGLE_API_CX,
        'q': imageName,
        'searchType': "image"
    } 
    # sending get request and saving the response as response object 
    r = requests.get(url = GOOGLE_API_URL, params = PARAMS) 
    # extracting data in json format 
    data = r.json() 
    return jsonify(data['items'][0]['link'])


@flask_app.route('/generate')
def generate():
    inputText = request.args.get('inputText')
    generatedText = generateSample(inputText)
    return jsonify(generatedText)


