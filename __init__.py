import os
import json
from json.decoder import JSONDecodeError

from flask import Flask, render_template
from flask import jsonify
from flask import send_file, send_from_directory
from flask import request

from flask_cors import CORS

from audio_validator.config import Config

def create_app():
    app = Flask(
        __name__, 
        instance_relative_config=True,
        static_folder = "./dist/static",
        template_folder = "./dist"
    )

    CORS(app)

    app.config.from_object(config.Config)
    
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/')
    def index():
        return render_template("index.html")

    @app.route('/languages/all')
    def get_all_languages():
        languages = app.config['AVAILABLE_LANGUAGES']

        return jsonify(languages)

    @app.route('/audio/<lang>/all')
    def get_audio(lang):
        audio_files = os.listdir(app.config['AUDIO_PATH'] + lang)

        data = [{'file_name': a} for a in audio_files]

        return jsonify(data)

    @app.route('/audio/validated', methods=['GET', 'POST'])
    def save_validated_audio():
        data = request.get_json()

        json_file_name = app.config['DATA_PATH'] + data['lang'] + '.json'

        if os.path.isfile(json_file_name):
            with open(json_file_name) as json_file:
                try:
                    json_data = json.load(json_file)
                except JSONDecodeError:
                    print('invalid file')

                    json_data = {}
                    json_data['validatedAudio'] = []
        else:
            json_data = {}
            json_data['validatedAudio'] = []

        json_data['validatedAudio'] = json_data['validatedAudio'] +  data['data']

        with open(json_file_name, "w") as json_file:
            json.dump(json_data, json_file)

        return jsonify(data)
    
    @app.route('/audio/<lang>/<name>')
    def get_audio_with_name(lang, name):
        return send_from_directory(app.config['AUDIO_PATH'] + lang, name, conditional=True)


    return app