import os
from flask import Flask
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'super_secret_default_key')

@app.route('/')
def index():
    return "Page Analyzer is running!"