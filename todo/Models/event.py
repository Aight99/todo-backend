from app import db
from todo.Models.auth import User


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'user_id': self.user_id,
        }


class Desk(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'user_id': self.user_id,
        }


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    desk_id = db.Column(db.Integer, db.ForeignKey(Desk.id))

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'desk_id': self.desk_id,
        }


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    header = db.Column(db.String)
    place = db.Column(db.String, nullable=True)
    tag_id = db.Column(db.Integer, db.ForeignKey(Tag.id))
    group_id = db.Column(db.Integer, db.ForeignKey(Group.id))
    date_begin_timestamp = db.Column(db.Integer, nullable=True)
    date_end_timestamp = db.Column(db.Integer, nullable=True)
    description = db.Column(db.String, nullable=True)
    is_done = db.Column(db.Boolean)

    def serialize(self):
        return {
            'id': self.id,
            'header': self.header,
            'place': self.place,
            'tag_id': self.tag_id,
            'group_id': self.group_id,
            'date_begin_timestamp': self.date_begin_timestamp,
            'date_end_timestamp': self.date_end_timestamp,
            'description': self.description,
            'is_done': self.is_done,
            'tag_name': Tag.query.filter_by(id=self.tag_id).first().name
        }
