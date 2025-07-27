from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)

    from .chat.chat import bp as chat_bp
    app.register_blueprint(chat_bp, url_prefix='/chat')

    @app.route("/")
    def home():
        return "<h1>gwdai home</h1>"


    return app