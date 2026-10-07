from flask import Flask
from .extensions import db, socketio

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    db.init_app(app)
    socketio.init_app(app)

    from .routes.main import bp as main_bp
    app.register_blueprint(main_bp)

    from . import events # registers socket handlers

    return app

