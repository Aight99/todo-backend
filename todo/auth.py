
from db import mongo
from flask import (
    Blueprint,
    jsonify,
    request,
    session)
from werkzeug.security import generate_password_hash, check_password_hash

db = mongo.db

auth = Blueprint('auth', __name__)


# @auth.route('/login')
# def login():
#     return render_template('login.html')
#
#
# @auth.route('/signup')
# def signup():
#     return render_template('signup.html')
#

# @auth.route('/hello', methods=['POST'])
# def hello():
#     return jsonify({'message': 'hello'})


@auth.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    name = data['login']
    password = data['password']

    user = db.users.find_one({"login": name})

    if user:
        return jsonify({'message': 'sign up failed'})

    db.users.insert_one({
        'login': name,
        'password': generate_password_hash(password, method='sha256')
    })

    return jsonify({'message': [name, password]})


@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    name = data['login']
    password = data['password']

    user = db.users.find_one({"login": name})

    if not user or not check_password_hash(user['password'], password):
        return jsonify({'message': 'sign in failed'})

    login_val = user['login']
    session['login'] = login_val

    return jsonify({'message': 'sign in success'})


@auth.route('/logout')
def logout():
    if "login" in session:
        session.pop('email', None)

    return jsonify({'message': 'log out'})
