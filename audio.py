import json
import os
import random
from json.decoder import JSONDecodeError

from flask import Blueprint, Flask
from flask import current_app as app
from flask import jsonify, send_file, send_from_directory, request
from flask_cors import CORS

audio = Blueprint('audio', __name__)

@audio.route('/audio/<lang>/all')
def get_audio(lang):
    all_audio_files = os.listdir(app.config['AUDIO_PATH'] + lang)
    audio_files = list(filter(lambda f: not f.endswith('info.json'), all_audio_files))

    json_file_name = app.config['DATA_PATH'] + lang + '.json'

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

    not_validated_audio_files = []

    random.shuffle(audio_files)

    for audio_file in audio_files:
        if len(not_validated_audio_files) >= app.config['ITEMS_ON_PAGE']:
            break

        if not any(v['file_name'] == audio_file for v in validated_file_names):
            not_validated_audio_files.append({'file_name': audio_file})

    return jsonify(not_validated_audio_files)

@audio.route('/audio/validated', methods=['GET', 'POST'])
def save_validated_audio():
    data = request.get_json()

    json_file_name = app.config['DATA_PATH'] + data['lang'] + '.json'

    if not os.path.isfile(json_file_name):
        json_data = {}
        json_data['validatedAudio'] = []
    else:
        with open(json_file_name) as json_file:
            try:
                json_data = json.load(json_file)
            except JSONDecodeError:
                json_data = {}
                json_data['validatedAudio'] = []

    json_data['validatedAudio'] = json_data['validatedAudio'] +  data['data']

    with open(json_file_name, "w") as json_file:
        json.dump(json_data, json_file)

    return jsonify(data)

@audio.route('/audio/<lang>/<name>')
def get_audio_with_name(lang, name):
    return send_from_directory(app.config['AUDIO_PATH'] + lang, name, conditional=True)
