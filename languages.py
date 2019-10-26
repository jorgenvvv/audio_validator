import json
import os
from json.decoder import JSONDecodeError

from flask import Blueprint, Flask
from flask import current_app as app
from flask import jsonify, send_file, send_from_directory
from flask_cors import CORS

languages = Blueprint('languages', __name__)

@languages.route('/languages/all')
def get_all_languages():
    available_languages = app.config['AVAILABLE_LANGUAGES']

    for language in available_languages:
        all_files = os.listdir(app.config['AUDIO_PATH'] + language['code'])
        total_files_count = len(
            list(filter(lambda f: not f.endswith('info.json'), all_files)))

        json_file_name = app.config['DATA_PATH'] + language['code'] + '.json'

        if os.path.isfile(json_file_name):
            with open(json_file_name) as json_file:
                try:
                    json_data = json.load(json_file)
                except JSONDecodeError:
                    json_data = {}
                    json_data['validatedAudio'] = []
        else:
            json_data = {}
            json_data['validatedAudio'] = []

        validated_file_names = json_data['validatedAudio']

        validated_files_count = len(validated_file_names)

        language['total'] = total_files_count
        language['validated'] = validated_files_count

    return jsonify(available_languages)
