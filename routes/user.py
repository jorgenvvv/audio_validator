from flask import Blueprint
from flask import jsonify
from flask_jwt_extended import get_jwt_claims, jwt_required
from sqlalchemy import and_

from ..model.validated_audio import ValidatedAudio, db

user = Blueprint('user', __name__)


@user.route('/user')
@jwt_required
def get_user():
    claims = get_jwt_claims()

    return jsonify(claims['userinfo'])
 

@user.route('/user/skill/<lang>')
@jwt_required
def get_user_language_skill(lang):
    claims = get_jwt_claims()

    validator_skill_level = (
        db.session.query(
            ValidatedAudio.validator_skill_level
        )
        .filter(
            and_(
                ValidatedAudio.expected_language_code == lang,
                ValidatedAudio.created_by == claims['user'],
                ValidatedAudio.validator_skill_level is not None
            )
        ).first()
    )

    return jsonify(validator_skill_level)
