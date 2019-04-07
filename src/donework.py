from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import requests

from src.gpt_2.src.interactive_conditional_samples import generate_sample
from src.gpt_2.src.check_if_correct import getNounImage
from src.scripts.generate import generate_paragraphs


GOOGLE_API_KEY = "AIzaSyBsgu9EkHIcsCQJJyiia1qH1WCtmWrLFvA"
GOOGLE_API_CX = "011903039758982039198:szvtofg-7gg"
GOOGLE_API_URL = "https://www.googleapis.com/customsearch/v1"


flask_app = Flask(__name__, template_folder='templates/')
CORS(flask_app)


@flask_app.route('/')
def index():
    return render_template('index.html')


@flask_app.route('/image', methods=['GET', 'POST'])
def image():
    body_request = request.json
    input_text = body_request['text']
    image_name = getNounImage(input_text)
    # defining a params dict for the parameters to be sent to the API
    params = {
        'key': GOOGLE_API_KEY,
        'cx': GOOGLE_API_CX,
        'q': image_name,
        'searchType': "image"
    } 
    # sending get request and saving the response as response object 
    r = requests.get(url=GOOGLE_API_URL, params=params)
    # extracting data in json format 
    data = r.json() 
    return jsonify({'url': data['items'][0]['link'], 'name': image_name})


@flask_app.route('/generate', methods=['GET', 'POST'])
def generate():
    body_request = request.json
    input_text = body_request['text']
    paragraphs = generate_paragraphs(input_text)
    for idx, p in enumerate(paragraphs):
        generated_text = generate_sample(p[2])
        paragraphs[idx].append(generated_text)

    result = ''
    for p in paragraphs:
        result += '\n\n'.join(p)

    return jsonify({'text': result})


