from datetime import timedelta
from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token
from todo.Models.auth import User
from app import db
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)


@auth.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('login')
    name = data.get('name')
    password = data.get('password')
    password_rep = data.get('password_rep')

    if password_rep != password:
        return "password does not match password repeat", 200

    user = User.query.filter_by(login=username).first()

    if user:
        return "user already exist", 200

    new_user = User(
        login=username,
        name=name,
        password=generate_password_hash(password)
    )
    db.session.add(new_user)
    db.session.commit()

    access_token = create_access_token(identity=new_user.id, expires_delta=timedelta(days=7))
    return jsonify({"access_token": access_token}), 200


@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('login')
    password = data.get('password')

    user = User.query.filter_by(login=username).first()

    if not user or not check_password_hash(user.password, password):
        return "sign in failed", 200

    access_token = create_access_token(identity=user.id, expires_delta=timedelta(days=7))
    return jsonify({"access_token": access_token}), 200
