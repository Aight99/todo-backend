from flask import Blueprint, jsonify, request, session
from db import mongo
import json
from bson.objectid import ObjectId

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

    todo = db.event.insert_one({
        'date_begin': date_begin,
        'date_end': date_end,
        'group_id': int(request_data['group_id']),
        'header': request_data['header'],
        'place': place,
        'tag_id': tag_id,
        'text': request_data['text'],
        'is_done': False
    })

    return json.dumps(todo.inserted_id , default=str)


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
    todos = db.event.find({'group_id': column_id, 'is_done': False})
    a = [todo for todo in todos]

    return json.dumps(a, default=str)


@main.route('/delete_todo', methods=['POST'], strict_slashes=False)
def delete_todo():
    request_data = request.get_json()
    todo_id = request_data['_id']
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


@main.route('/add_column', methods=['POST'], strict_slashes=False)
def add_column():
    request_data = request.get_json()
    group_name = request_data['group_name']
    desk_id = request_data['desk_id']

    columns = db.group.find()
    a = [column for column in columns]
    group_id = a[-1]['group_id'] + 1

    column = db.group.insert_one({
        'group_id': group_id,
        'group_name': group_name,
        'desk_id': desk_id
    })

    return json.dumps([column.inserted_id, group_id], default=str)


@main.route('/edit_column', methods=['POST'], strict_slashes=False)
def edit_column_name():
    request_data = request.get_json()
    group_name = request_data['group_name']
    group__id = request_data['_id']
    group_id = request_data['group_id']
    desk_id = request_data['desk_id']

    column = db.group.update_one({'_id': ObjectId(group__id)}, {'$set': {
        'group_name': group_name,
        'group_id': group_id,
        'desk_id': desk_id
    }})

    return column.raw_result


@main.route('/delete_column', methods=['POST'], strict_slashes=False)
def delete_column():
    request_data = request.get_json()
    column_id = request_data['_id']
    column = db.group.delete_one({'_id': ObjectId(column_id)})
    db.event.delete_many({'group_id': request_data['group_id']})
    return column.raw_result


@main.route('/done_todo', methods=['POST'], strict_slashes=False)
def done_todo():
    request_data = request.get_json()
    todo_id = request_data['_id']
    todo = db.event.update_one({'_id': ObjectId(todo_id)}, {'$set': {
        'is_done': True
    }})

    return todo.raw_result