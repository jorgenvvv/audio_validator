import json
import os
import random
from json.decoder import JSONDecodeError

from audio_validator.audio import audio
from audio_validator.languages import languages
from audio_validator.config import Config
from flask import (Flask, jsonify, render_template, request, send_file,
                   send_from_directory)
from flask_cors import CORS


def create_app():
    app = Flask(
        __name__,
        instance_relative_config=True,
        static_folder='./dist/static',
        template_folder='./dist'
    )

    app.register_blueprint(audio)
    app.register_blueprint(languages)

    CORS(app)

    app.config.from_object(config.Config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/')
    def index():
        return render_template('index.html')


    return app
