import json
import os
import random
from json.decoder import JSONDecodeError

from flask import (Flask, jsonify, render_template, request, send_file,
                   send_from_directory)
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from audio_validator.config import Config


def create_app():
    from . import routes

    app = Flask(
        __name__,
        instance_relative_config=True,
        static_folder='./dist/static',
        template_folder='./dist'
    )

    routes.init_app(app)

    CORS(app)

    app.config.from_object(config.Config)

    jwt = JWTManager(app)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/')
    def index():
        return render_template('index.html')

    return app
