from .audio import audio
from .languages import languages

def init_app(app):
    app.register_blueprint(audio)
    app.register_blueprint(languages)