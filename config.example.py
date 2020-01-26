
"""
===============================================
APP CONFIGURATION

To use this file as configuration rename it to:

    config.py

===============================================
"""

import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    # Debug mode
    DEBUG = False
     
    # Specify a secret key for JWT authentication
    JWT_SECRET_KEY = ''

    # JWT access token expire time (if not set default is 15 minutes)
    JWT_ACCESS_TOKEN_EXPIRES = 7200  # 2 hours

    # To use google authentication CLIENT_ID and CLIENT_SECRET are needed
    # They can be obtained from https://console.developers.google.com/
    GOOGLE_AUTH_CLIENT_ID = ''
    GOOGLE_AUTH_CLIENT_SECRET = ''

    # Sqlite database location
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Path where audio files are stored
    AUDIO_PATH = ''

    # Path to a json file where language codes and names are stored
    # This file will be imported into app config separately
    LANGUAGES_FILE_PATH = os.path.join(basedir, 'languages.json')

    # How many audio files to display on page
    ITEMS_ON_PAGE = 10
