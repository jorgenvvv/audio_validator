import json
import os
import random
from datetime import datetime as dt
from json.decoder import JSONDecodeError

from flask import Blueprint, Flask
from flask import current_app as app
from flask import jsonify, request, send_file, send_from_directory
from flask_jwt_extended import get_jwt_claims, jwt_required
from sqlalchemy import and_, func

from ..model.validated_audio import ValidatedAudio, db

audio = Blueprint('audio', __name__)


@audio.route('/audio/<lang>/all')
@jwt_required
def get_audio(lang):
    claims = get_jwt_claims()

    audio_files = os.listdir(app.config['AUDIO_PATH'] + lang)

    random.shuffle(audio_files)

    selected_audio_files = []

    validated_limit = app.config['ITEMS_ON_PAGE'] // 2

    once_validated_files = (
        db.session.query(
            ValidatedAudio.file_name
        )
        .filter(ValidatedAudio.expected_language_code == lang)
        .group_by(ValidatedAudio.file_name)
        .having(
            and_(
                func.count(ValidatedAudio.file_name) == 1,
                ValidatedAudio.created_by != claims['user']
            )
        )
        .order_by(func.random())
        .limit(validated_limit)
    )


    for validated_file, in once_validated_files:
        metadata = get_audio_metadata(validated_file, lang)
        if metadata is not None:
            selected_audio_files.append(metadata)

    for audio_file in audio_files:
        if len(selected_audio_files) >= app.config['ITEMS_ON_PAGE']:
            break

        exists = db.session.query(ValidatedAudio.id).filter_by(
            file_name=audio_file).count() > 0

        if exists:
            continue

        metadata = get_audio_metadata(audio_file, lang)
        if metadata is not None:
            selected_audio_files.append(metadata)

    random.shuffle(selected_audio_files)

    return jsonify(selected_audio_files)


@audio.route('/audio/validated', methods=['POST'])
@jwt_required
def save_validated_audio():
    req = request.get_json()

    claims = get_jwt_claims()

    for audio in req['data']:
        validated_audio = ValidatedAudio(
            file_name=audio['file_name'],
            created_at=dt.now(),
            created_by=claims['user'],
            validator_skill_level=audio['validator_skill_level'],
            expected_language_code=audio['expected_language_code'],
            validation_value=audio['language'],
            video_id=audio['video_id'],
            video_title=audio['video_title']
        )

        db.session.add(validated_audio)

    db.session.commit()

    return '', 200


@audio.route('/audio/<lang>/<name>')
def get_audio_with_name(lang, name):
    return send_from_directory(app.config['AUDIO_PATH'] + lang, name, conditional=True)


def get_audio_metadata(audio_file, lang):
    metadata_file_name = audio_file.split('__')[0] + '.info.json'

    try:
        with open(os.path.join(app.config['AUDIO_METADATA_PATH'] + lang, metadata_file_name)) as json_file:
            json_metadata = json.load(json_file)
    except OSError:
        return None

    metadata_required = ['id', 'description', 'title']
    filtered_metadata = {
        r: json_metadata[r] for r in metadata_required
    }

    return {'file_name': audio_file, 'metadata': filtered_metadata}
