from flask import Blueprint, jsonify, request, session
from db import mongo
import json
from bson.objectid import ObjectId
import datetime
import re

main = Blueprint('main', __name__)
db = mongo.db


@main.route('/hello', methods=['POST'])
def hello():
    data = request.get_json()
    name = data['first']
    password = data['second']

    return jsonify({'message': [name, password, 'help']})


@main.route('/todos', methods=['POST'])
def add_todo():
    request_data = request.get_json()
    # if "login" not in session:
    #     return jsonify({'message': 'user not authorization'})
    # email = session["login"]
    print(request_data)
    tag_id = request_data['tag_id']
    place = request_data['place']
    date_begin = request_data['date_begin']
    date_end = request_data['date_end']
    if tag_id == '':
        tag_id = 0
    if place == '':
        place = None

    db.event.insert_one({
        'date_begin': date_begin,
        'date_end': date_end,
        'group_id': int(request_data['group_id']),
        'header': request_data['header'],
        'place': place,
        'tag_id': tag_id,
        'text': request_data['text']
    })

    return jsonify({'message': 'da'})


@main.route('/todos', methods=['GET'], strict_slashes=False)
def get_todos():
    todos = db.event.find()
    a = [todo for todo in todos]

    return json.dumps(a, default=str)


@main.route('/columns', methods=['GET'], strict_slashes=False)
def get_columns():
    columns = db.group.find()
    a = [todo for todo in columns]

    return json.dumps(a, default=str)


@main.route('/todos/<int:column_id>', methods=['GET'], strict_slashes=False)
def get_todos_from_one_column(column_id):
    todos = db.event.find({'group_id': column_id})
    a = [todo for todo in todos]

    return json.dumps(a, default=str)


@main.route('/delete_todo', methods=['POST'], strict_slashes=False)
def delete_todo():
    request_data = request.get_json()
    todo_id = request_data['_id']
    print(todo_id)
    todo = db.event.delete_one({'_id': ObjectId(todo_id)})
    return todo.raw_result


@main.route('/edit_todo', methods=['POST'], strict_slashes=False)
def edit_post():
    request_data = request.get_json()
    todo_id = request_data['_id']
    tag_id = request_data['tag_id']
    place = request_data['place']
    date_begin = request_data['date_begin']
    date_end = request_data['date_end']

    if tag_id == '':
        tag_id = 0
    if place == '':
        place = None

    todo = db.event.update_one({'_id': ObjectId(todo_id)}, {'$set': {
        'date_begin': date_begin,
        'date_end': date_end,
        'group_id': int(request_data['group_id']),
        'header': request_data['header'],
        'place': place,
        'tag_id': tag_id,
        'text': request_data['text']
    }})

    return todo.raw_result
