import os

from flask import Flask, render_template


def create_app():
    app = Flask(
        __name__, 
        instance_relative_config=True,
        static_folder = "./dist/static",
        template_folder = "./dist"
    )
    
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/')
    def index():
        return render_template("index.html")

    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app