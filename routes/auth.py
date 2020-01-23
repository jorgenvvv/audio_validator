import json

import requests
from flask import Blueprint
from flask import current_app as app
from flask import jsonify, request
from flask_jwt_extended import (create_access_token, get_jwt_identity,
                                jwt_required)

from .. import jwt

auth = Blueprint('auth', __name__)

@jwt.user_claims_loader
def add_claims_to_access_token(identity):
    claims = {
        'userinfo': identity
    }

    if 'email' in identity:
        claims['user'] = identity['email']
        return claims
    elif 'name' in identity:
        claims['user'] = identity['name']
        return claims
    else:
        claims['user'] = 'UNKNOWN'

    return claims

@auth.route('/auth/<provider>', methods=['POST'])
def authenticate(provider):
    req = request.get_json()

    if provider == 'google':
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        auth_request = requests.post('https://accounts.google.com/o/oauth2/token', data={
            'code': req['code'],
            'client_id': app.config['GOOGLE_AUTH_CLIENT_ID'],
            'client_secret': app.config['GOOGLE_AUTH_CLIENT_SECRET'],
            'redirect_uri': req['redirectUri'],
            'grant_type': 'authorization_code'
        }, headers=headers)

        headers = {
            "Authorization": f'Bearer {auth_request.json()["access_token"]}'}
        user_info_request = requests.get(
            "https://openidconnect.googleapis.com/v1/userinfo", headers=headers)

        access_token = create_access_token(
            identity=user_info_request.json())

        return jsonify(access_token=access_token), 200

    else:
        raise NotImplementedError
