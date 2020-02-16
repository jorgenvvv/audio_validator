import hashlib

from flask import Blueprint
from flask import jsonify
from flask_jwt_extended import get_jwt_claims, jwt_required
from sqlalchemy import and_, func, desc, inspect

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
                ValidatedAudio.validator_skill_level.isnot(None)
            )
        ).first()
    )

    if validator_skill_level is not None:
        validator_skill_level = validator_skill_level[0]

    skill_level = {
        'skillLevel': validator_skill_level
    }

    return jsonify(skill_level)


@user.route('/user/validated/<lang>')
@jwt_required
def get_user_validated_audio_count(lang):
    claims = get_jwt_claims()

    lang_validated_count = (
        db.session.query(
            ValidatedAudio.file_name
        )
        .filter_by(expected_language_code=lang, created_by=claims['user'])
        .distinct()
        .count()
    )

    total_validated_count = (
        db.session.query(
            ValidatedAudio.file_name
        )
        .filter_by(created_by=claims['user'])
        .count()
    )

    user_rank = (
        db.session.query(
            func.count(ValidatedAudio.file_name).label("cnt")
        )
        .group_by(ValidatedAudio.created_by)
        .order_by(desc("cnt"))
    ).first()

    subquery = (
        db.session.query(
            ValidatedAudio.created_by,
            func.count(ValidatedAudio.file_name).label('cnt')
        )
        .group_by(ValidatedAudio.created_by)
    ).subquery()

    user_ranks = (
        db.session.query(
            subquery,
            func.rank().over(order_by=desc('cnt')).label('user_rank')
        )
    ).subquery()
    
    user_rank = db.session.query(user_ranks).filter_by(created_by=claims['user']).first()

    users_count = db.session.query(ValidatedAudio.created_by).distinct().count()

    return jsonify(
        {
            'languageValidatedCount': lang_validated_count, 
            'totalValidatedCount': total_validated_count,
            'rank': user_rank._asdict()['user_rank'] if user_rank else 0,
            'usersCount': users_count
        }
    )


@user.route('/user/leaderboard')
@jwt_required
def get_leaderboard():
    claims = get_jwt_claims()

    subquery = (
        db.session.query(
            ValidatedAudio.created_by,
            func.count(ValidatedAudio.file_name).label('cnt')
        )
        .group_by(ValidatedAudio.created_by)
    ).subquery()

    user_ranks = (
        db.session.query(
            subquery,
            func.rank().over(order_by=desc('cnt')).label('user_rank')
        )
    ).all()

    user_ranks = [r._asdict() for r in user_ranks]

    for r in user_ranks:
        if r['created_by'] != claims['user']:
            r['created_by'] = abs(hash(r['created_by'])) % (10 ** 8)

    return jsonify(user_ranks)
