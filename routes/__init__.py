from .audio import audio
from .languages import languages
from .auth import auth

def init_app(app):
    app.register_blueprint(audio)
    app.register_blueprint(languages)
    app.register_blueprint(auth)
