import os

from flask import Flask, render_template
from flask import jsonify
from flask import send_file, send_from_directory

from flask_cors import CORS

from config import Config

def create_app():
    app = Flask(
        __name__, 
        instance_relative_config=True,
        static_folder = "./dist/static",
        template_folder = "./dist"
    )

    CORS(app)

    app.config.from_object(config.Config)
    
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/')
    def index():
        return render_template("index.html")

    @app.route('/audio/all')
    def available_audio():
        audio_files = os.listdir(app.config['AUDIO_PATH'])

        return jsonify(audio_files)

    @app.route('/audio/<name>')
    def audio(name):
        return send_from_directory(app.config['AUDIO_PATH'], name, conditional=True)


    return app