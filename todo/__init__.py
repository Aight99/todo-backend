from flask import Flask
from db import mongo
from flask_cors import CORS

def create_app():
    app = Flask(__name__, static_url_path='')
    app.config.from_pyfile("config.py")
    mongo.init_app(app)
    CORS(app)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
