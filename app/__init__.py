from quart import Quart

def create_app():
    app = Quart(__name__)

    app.config["RESPONSE_TIMEOUT"] = None

    from .routes.chat import bp as chat_bp
    app.register_blueprint(chat_bp)

    return app
