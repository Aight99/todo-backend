from flask import Blueprint, jsonify, request
from todo.Models.event import Event, Group, Desk, Tag
from app import db

main = Blueprint('main', __name__)


@main.route('/', methods=['GET'])
def test():
    from sqlalchemy import create_engine, MetaData
    engine = create_engine('sqlite:///todos.db')
    meta = MetaData()
    meta.reflect(bind=engine)
    tables = meta.tables.keys()
    print(tables)
    return jsonify("Bruh"), 200


@main.route('/hello', methods=['POST'])
def hello():
    data = request.get_json()
    name = data['first']
    password = data['second']

    return jsonify({'message': [name, password, 'help']}), 200


@main.route('/todos', methods=['POST'], strict_slashes=False)
def add_todo():
    request_data = request.get_json()

    print(request_data)

    header = request_data.get('header')
    tag_id = request_data.get('tag_id')
    group_id = request_data.get('group_id')
    place = request_data.get('place')
    date_begin_timestamp = request_data.get('date_begin_timestamp')
    date_end_timestamp = request_data.get('date_end_timestamp')
    description = request_data.get('description')
    is_done = request_data.get('is_done')

    if not tag_id:
        tag_id = 0
    if not group_id:
        group_id = 0

    new_event = Event(
        header=header,
        place=place,
        tag_id=tag_id,
        group_id=group_id,
        date_begin_timestamp=date_begin_timestamp,
        date_end_timestamp=date_end_timestamp,
        description=description,
        is_done=is_done
    )

    db.session.add(new_event)
    db.session.commit()

    return jsonify("Makarena"), 200


@main.route('/todos', methods=['GET'], strict_slashes=False)
def get_todos():
    todos = [todo.serialize() for todo in Event.query.all()]
    return jsonify(todos), 200


@main.route('/columns', methods=['GET'], strict_slashes=False)
def get_columns():
    columns = [column.serialize() for column in Group.query.all()]
    return jsonify(columns), 200


@main.route('/todos/<int:column_id>', methods=['GET'], strict_slashes=False)
def get_todos_from_one_column(column_id):
    todos = Event.query.filter_by(group_id=column_id, is_done=False).all()
    todos = [todo.serialize() for todo in todos]
    return jsonify(todos), 200


@main.route('/delete_todo', methods=['DELETE'], strict_slashes=False)
def delete_todo():
    request_data = request.get_json()
    todo_id = request_data.get('id')
    todo_to_delete = Event.query.filter_by(id=todo_id).first()
    if todo_to_delete:
        db.session.delete(todo_to_delete)
        db.session.commit()
    return "Totototototo", 200


@main.route('/edit_todo', methods=['PUT'], strict_slashes=False)
def edit_todo():
    request_data = request.get_json()

    todo_id = request_data.get('id')

    todo_to_edit = Event.query.filter_by(id=todo_id).first()
    if not todo_to_edit:
        return "Ne exist", 200

    edit_dict = dict()
    edit_dict['header'] = request_data.get('header')
    edit_dict['tag_id'] = request_data.get('tag_id')
    edit_dict['group_id'] = request_data.get('group_id')
    edit_dict['place'] = request_data.get('place')
    edit_dict['date_begin_timestamp'] = request_data.get('date_begin_timestamp')
    edit_dict['date_end_timestamp'] = request_data.get('date_end_timestamp')
    edit_dict['description'] = request_data.get('description')
    edit_dict['is_done'] = request_data.get('is_done')

    for key, value in edit_dict.items():
        if value:
            setattr(todo_to_edit, key, value)
    db.session.commit()

    return "I am just a fish", 200


@main.route('/add_column', methods=['POST'], strict_slashes=False)
def add_column():
    request_data = request.get_json()

    name = request_data.get('name')
    desk_id = request_data.get('desk_id')

    new_column = Group(
        name=name,
        desk_id=desk_id
    )

    db.session.add(new_column)
    db.session.commit()

    return "Column-group", 200


@main.route('/tags',  methods=['GET'], strict_slashes=False)
def get_tags():
    tags = [tag.serialize() for tag in Tag.query.all()]
    return jsonify(tags), 200


@main.route('/delete_tag', methods=['DELETE'], strict_slashes=False)
def delete_tag():
    request_data = request.get_json()
    tag_id = request_data.get('id')

    if tag_id == '0':
        return "Zero", 200

    tag_to_delete = Tag.query.filter_by(id=tag_id).first()

    if not tag_to_delete:
        return "Unexpected @all", 200

    events = Event.query.filter_by(tag_id=tag_id).all()
    for event in events:
        event.tag_id = 0
    db.session.delete(tag_to_delete)
    db.session.commit()
    return "Al al al", 200


@main.route('/add_tag', methods=['POST'], strict_slashes=False)
def add_tag():
    request_data = request.get_json()
    print(request_data)

    name = request_data.get('name')
    # Current user
    user_id = 0

    new_tag = Tag(
        name=name,
        user_id=user_id
    )

    db.session.add(new_tag)
    db.session.commit()
    return "@all", 200
