import os

from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import requests

from src import *
from src.gpt_2.src.interactive_conditional_samples import generate_sample
from src.gpt_2.src.check_if_correct import getNounImage
from src.scripts.generate import generate_paragraphs
from src.similarity.util import helper
from src.similarity.util.nmslib import Nmslib


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
    text = request.args.get('text')
    print(text)
    imageName = getNounImage(text)
    print(imageName)
    # defining a params dict for the parameters to be sent to the API 
    PARAMS = {
        'key': GOOGLE_API_KEY,
        'cx': GOOGLE_API_CX,
        'q': imageName,
        'searchType': "image"
    } 
    # sending get request and saving the response as response object 
    r = requests.get(url=GOOGLE_API_URL, params=PARAMS)
    # extracting data in json format 
    data = r.json() 
    return jsonify({'url': data['items'][0]['link'], 'name': imageName})


@flask_app.route('/generate')
def generate():
    input_text = request.args.get('inputText')
    paragraphs = generate_paragraphs(input_text)
    for idx, p in enumerate(paragraphs):
        generated_text = generate_sample(input_text)
        paragraphs[idx].append(generated_text)

    result = ''
    for p in paragraphs:
        result += '\n\n'.join(p)

    return jsonify(result)


