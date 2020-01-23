from flask import Blueprint
from flask import jsonify
from flask_jwt_extended import get_jwt_claims, jwt_required

user = Blueprint('user', __name__)


@user.route('/user')
@jwt_required
def get_user():
    claims = get_jwt_claims()

    return jsonify(claims['userinfo'])
 
