from flask import Flask, render_template
from flask_cors import CORS


flask_app = Flask(__name__, template_folder='templates/')
CORS(flask_app)


@flask_app.route('/')
def index():
    return render_template('index.html')
