from .audio import audio
from .languages import languages
from .auth import auth
from .user import user
from .results import results

def init_app(app):
    app.register_blueprint(audio)
    app.register_blueprint(languages)
    app.register_blueprint(auth)
    app.register_blueprint(user)
    app.register_blueprint(results)
