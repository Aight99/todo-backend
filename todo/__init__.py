from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
jwt = None


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("config.py")
    db.init_app(app)
    CORS(app, resources={r"/": {"origins": "http://localhost:3000"}})

    from todo.Models.event import Event, Tag, Desk, Group
    from todo.Models.auth import User

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    global jwt
    jwt = JWTManager(app)

    return app
