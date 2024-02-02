from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)

    from .sentiment import sentiment
    app.register_blueprint(sentiment, url_prefix='/api/sentiment')

    return app
