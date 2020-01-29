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
    languages_in_folder = os.listdir(app.config['AUDIO_PATH'])
    all_languages = app.config['ALL_LANGUAGES']

    available_languages = {
        lang: all_languages[lang] for lang in languages_in_folder}

    for language in available_languages:
        all_files = os.listdir(app.config['AUDIO_PATH'] + language)

        all_audio_files_count = len(
            [f for f in all_files if not f.endswith('info.json')])

        validated_files_count = (
            db.session.query(
                ValidatedAudio.file_name
            )
            .filter_by(expected_language_code=language)
            .distinct()
            .count()
        )

        all_languages[language]['total'] = all_audio_files_count
        all_languages[language]['validated'] = validated_files_count

    return jsonify(available_languages)


@languages.route('/languages/<lang>/info')
@jwt_required
def get_language_info(lang):
    language_info = app.config['AVAILABLE_LANGUAGES'][lang]

    return jsonify(language_info)
