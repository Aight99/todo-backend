from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from todo.Models.event import Event, Group, Desk, Tag
from todo.Models.auth import User
from app import db, jwt

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


@main.route('/hello', methods=['POST', 'GET'])
@jwt_required()
def hello():
    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()
    return f"Hello, {user.name}!", 200


@main.route('/todos', methods=['POST'], strict_slashes=False)
@jwt_required()
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

    return new_event.serialize(), 200


@main.route('/todos', methods=['GET'], strict_slashes=False)
@jwt_required()
def get_todos():
    user_id = get_jwt_identity()
    desk_id = Desk.query.filter_by(user_id=user_id).first()
    group_id = Group.query.filter_by(desk_id=desk_id).first()
    todos = [todo.serialize() for todo in Event.query.filter_by(group_id=group_id).all()]
    return jsonify(todos), 200


@main.route('/todos/<int:column_id>', methods=['GET'], strict_slashes=False)
@jwt_required()
def get_todos_from_one_column(column_id):
    todos = Event.query.filter_by(group_id=column_id, is_done=False).all()
    todos = [todo.serialize() for todo in todos]
    return jsonify(todos), 200


@main.route('/todos', methods=['DELETE'], strict_slashes=False)
@jwt_required()
def delete_todo():
    request_data = request.get_json()
    todo_id = request_data.get('id')
    todo_to_delete = Event.query.filter_by(id=todo_id).first()
    if not todo_to_delete:
        return "Ne exist", 404
    db.session.delete(todo_to_delete)
    db.session.commit()
    return "Deleted", 200


@main.route('/todos', methods=['PUT'], strict_slashes=False)
@jwt_required()
def edit_todo():
    request_data = request.get_json()
    todo_id = request_data.get('id')

    todo_to_edit = Event.query.filter_by(id=todo_id).first()
    if not todo_to_edit:
        return "Ne exist", 404

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

    return todo_to_edit.serialize(), 200


@main.route('/done_todo', methods=['POST'], strict_slashes=False)
@jwt_required()
def done_todo():
    request_data = request.get_json()
    todo_id = request_data.get('id')

    todo_to_edit = Event.query.filter_by(id=todo_id).first()
    if not todo_to_edit:
        return "Ne exist", 404

    todo_to_edit.is_done = True
    db.session.commit()

    return todo_to_edit.serialize(), 200


@main.route('/done_todo', methods=['GET'], strict_slashes=False)
@jwt_required()
def get_done_todo():
    user_id = get_jwt_identity()
    desk_id = Desk.query.filter_by(user_id=user_id).first()
    group_id = Group.query.filter_by(desk_id=desk_id).first()
    todos = [todo.serialize() for todo in Event.query.filter_by(group_id=group_id, is_done=True).all()]
    return jsonify(todos), 200


@main.route('/columns', methods=['GET'], strict_slashes=False)
@jwt_required()
def get_columns():
    user_id = get_jwt_identity()
    desk_id = Desk.query.filter_by(user_id=user_id).first()
    columns = [column.serialize() for column in Group.query.filter_by(desk_id=desk_id).all()]
    return jsonify(columns), 200


@main.route('/columns', methods=['POST'], strict_slashes=False)
@jwt_required()
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

    return new_column.serialize(), 200


@main.route('/columns', methods=['DELETE'], strict_slashes=False)
@jwt_required()
def delete_column():
    request_data = request.get_json()
    column_id = request_data.get('id')
    column_to_delete = Group.query.filter_by(id=column_id).first()
    if not column_to_delete:
        return "Ne exist", 404
    db.session.delete(column_to_delete)
    db.session.commit()
    return "Deleted", 200


@main.route('/columns', methods=['PUT'], strict_slashes=False)
@jwt_required()
def edit_column():
    request_data = request.get_json()
    column_id = request_data.get('id')

    column_to_edit = Event.query.filter_by(id=column_id).first()
    if not column_to_edit:
        return "Ne exist", 404

    edit_dict = dict()
    edit_dict['name'] = request_data.get('name')
    edit_dict['desk_id'] = request_data.get('desk_id')

    for key, value in edit_dict.items():
        if value:
            setattr(column_to_edit, key, value)
    db.session.commit()

    return column_to_edit.serialize(), 200


@main.route('/tags',  methods=['GET'], strict_slashes=False)
@jwt_required()
def get_tags():
    user_id = get_jwt_identity()
    tags = [tag.serialize() for tag in Tag.query.filter_by(user_id=user_id).all()]
    return jsonify(tags), 200


@main.route('/tags', methods=['DELETE'], strict_slashes=False)
@jwt_required()
def delete_tag():
    request_data = request.get_json()
    tag_id = request_data.get('id')

    if tag_id == '0':
        return "Zero", 400

    tag_to_delete = Tag.query.filter_by(id=tag_id).first()

    if not tag_to_delete:
        return "Unexpected @all", 404

    events = Event.query.filter_by(tag_id=tag_id).all()
    for event in events:
        event.tag_id = 0
    db.session.delete(tag_to_delete)
    db.session.commit()
    return "Deleted", 200


@main.route('/tags', methods=['POST'], strict_slashes=False)
@jwt_required()
def add_tag():
    request_data = request.get_json()
    print(request_data)

    name = request_data.get('name')
    user_id = get_jwt_identity()

    new_tag = Tag(
        name=name,
        user_id=user_id
    )

    db.session.add(new_tag)
    db.session.commit()
    return new_tag.serialize(), 200


@main.route('/tags', methods=['PUT'], strict_slashes=False)
@jwt_required()
def edit_tag():
    request_data = request.get_json()
    tag_id = request_data.get('id')

    tag_to_edit = Tag.query.filter_by(id=tag_id).first()
    if not tag_to_edit:
        return "Ne exist", 404

    new_name = request_data.get('name')
    if new_name:
        tag_to_edit.name = new_name

    db.session.commit()

    return tag_to_edit.serialize(), 200


@main.route('/desks',  methods=['GET'], strict_slashes=False)
@jwt_required()
def get_desks():
    user_id = get_jwt_identity()
    desks = [desk.serialize() for desk in Desk.query.filter_by(user_id=user_id).all()]
    return jsonify(desks), 200


@main.route('/desks', methods=['DELETE'], strict_slashes=False)
@jwt_required()
def delete_desk():
    request_data = request.get_json()
    desk_id = request_data.get('id')

    desk_to_delete = Desk.query.filter_by(id=desk_id).first()
    if not desk_to_delete:
        return "Unexpected @all", 404

    db.session.delete(desk_to_delete)
    db.session.commit()
    return "Deleted", 200


@main.route('/desks', methods=['POST'], strict_slashes=False)
@jwt_required()
def add_desk():
    request_data = request.get_json()
    print(request_data)

    name = request_data.get('name')
    user_id = get_jwt_identity()

    new_desk = Desk(
        name=name,
        user_id=user_id
    )

    db.session.add(new_desk)
    db.session.commit()
    return new_desk.serialize(), 200


@main.route('/desks', methods=['PUT'], strict_slashes=False)
@jwt_required()
def edit_desk():
    request_data = request.get_json()
    desk_id = request_data.get('id')

    desk_to_edit = Desk.query.filter_by(id=desk_id).first()
    if not desk_to_edit:
        return "Ne exist", 404

    new_name = request_data.get('name')
    if new_name:
        desk_to_edit.name = new_name

    db.session.commit()

    return desk_to_edit.serialize(), 200

