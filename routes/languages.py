import json
import os
from json.decoder import JSONDecodeError

from flask import Blueprint, Flask
from flask import current_app as app
from flask import jsonify, send_file, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import jwt_required

from ..model.validated_audio import ValidatedAudio, db

languages = Blueprint('languages', __name__)

@languages.route('/languages/all')
@jwt_required
def get_all_languages():
    available_languages = app.config['AVAILABLE_LANGUAGES']

    for language in available_languages:
        all_files = os.listdir(app.config['AUDIO_PATH'] + language['code'])

        all_audio_files_count = len([f for f in all_files if not f.endswith('info.json')])

        validated_files_count = (
            db.session.query(
                ValidatedAudio.file_name
            )
            .filter_by(expected_language_code=language['code'])
            .distinct()
            .count()
        )

        language['total'] = all_audio_files_count
        language['validated'] = validated_files_count

    return jsonify(available_languages)


@languages.route('/languages/<lang>/info')
@jwt_required
def get_language_info(lang):
    correct_lang_config = next(
        (l for l in app.config['AVAILABLE_LANGUAGES'] if l['code'] == lang), None)

    return jsonify(correct_lang_config)