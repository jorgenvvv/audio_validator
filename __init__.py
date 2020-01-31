import json
import os
import random
from json.decoder import JSONDecodeError

from flask import (Flask, jsonify, render_template, request, send_file,
                   send_from_directory)
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    from . import routes
    from .config import Config

    app = Flask(
        __name__,
        instance_relative_config=True,
        static_folder='./dist/static',
        template_folder='./dist'
    )

    app.config.from_object(Config)
    app.config.from_json(app.config['LANGUAGES_FILE_PATH'])

    db.init_app(app)
    jwt.init_app(app)
    routes.init_app(app)

    CORS(app)

    with app.app_context():
        # Models have to be imported to create tables
        from . import model

        db.create_all()

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.before_first_request
    def calculcate_audio_data_stats():
        languages_in_folder = os.listdir(app.config['AUDIO_PATH'])

        language_stats = {}

        for language in languages_in_folder:
            language_audio_count = len(os.listdir(
                os.path.join(app.config['AUDIO_PATH'], language)))
            language_count = {'count': language_audio_count}
            language_stats[language] = language_count

        with open(app.config['AUDIO_STATS_FILE_PATH'], 'w') as fout:
            json.dump(language_stats, fout)

    @app.route('/', defaults={'path': '/'})
    @app.route('/<path:path>')
    def index(path):
        return render_template('index.html')

    @app.route('/assets/<path:path>')
    def get_assets(path):
        return send_from_directory('./dist/assets', path)

    return app
