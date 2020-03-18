from flask import Blueprint
from flask import jsonify
from flask import current_app as app
from flask_jwt_extended import get_jwt_claims, jwt_required
from sqlalchemy import func

from ..model.validated_audio import ValidatedAudio, db

results = Blueprint('results', __name__)


@results.route('/results')
@jwt_required
def get_results():
    results = (
        db.session.query(
            ValidatedAudio.expected_language_code,
            ValidatedAudio.validation_value,
            func.count(ValidatedAudio.validation_value),
        )
        .group_by(
            ValidatedAudio.expected_language_code,
            ValidatedAudio.validation_value,
        )
    ).all()

    subquery = (
        db.session.query(
            ValidatedAudio.file_name,
        )
        .group_by(ValidatedAudio.file_name)
        .having(func.count(ValidatedAudio.file_name) > 1)
    ).subquery()

    results2 = (
        db.session.query(
            ValidatedAudio.file_name,
            ValidatedAudio.validation_value,
            ValidatedAudio.expected_language_code
        )
        .filter(ValidatedAudio.file_name.in_(subquery))
        .order_by(ValidatedAudio.file_name)
    ).all()

    results3 = (
        db.session.query(
            ValidatedAudio.expected_language_code,
            func.count(ValidatedAudio.expected_language_code)
        )
        .filter(ValidatedAudio.file_name.in_(subquery))
        .group_by(ValidatedAudio.expected_language_code)
    ).all()


    tmp = {}
    for r in results:
        if r[0] in tmp:
            tmp[r[0]][r[1]] = r[2]
        else:
            tmp[r[0]] = {}
            tmp[r[0]][r[1]] = r[2]

    result = []
    for key in tmp:
        value = tmp[key]
        value['language'] = app.config['ALL_LANGUAGES'][key]
        value['language']['code'] = key
        result.append(value)

    language_overlaps = {}
    for r2 in results2:
        if not r2[0] in language_overlaps:
            language_overlaps[r2[0]] = {}
            language_overlaps[r2[0]]['lang'] = r2[2]
            language_overlaps[r2[0]]['values'] = []
            language_overlaps[r2[0]]['values'].append(r2[1])
        else:
            language_overlaps[r2[0]]['values'].append(r2[1])
    
    for lo in language_overlaps.keys():
        if len(set(language_overlaps[lo]['values'])) == 1:
            for r in result:
                if r['language']['code'] == language_overlaps[lo]['lang']:
                    if 'answer_overlap' not in r:
                        r['answer_overlap'] = 1
                    else:
                        r['answer_overlap'] = r['answer_overlap'] + 1

    for r3 in results3:
        for r in result:
            if r['language']['code'] == r3[0]:
                r['total_validated_twice'] = r3[1] / 2

    return jsonify(result)
