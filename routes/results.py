from flask import Blueprint
from flask import jsonify
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
            func.count(ValidatedAudio.validation_value)
        )
        .group_by(
            ValidatedAudio.expected_language_code,
            ValidatedAudio.validation_value
        )
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
        value['language'] = key
        result.append(value)

    return jsonify(result)
