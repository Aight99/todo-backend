from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String)
    name = db.Column(db.String)
    password = db.Column(db.String)

    def serialize(self):
        return {
            'id': self.id,
            'login': self.login,
            'name': self.name,
        }

    def __str__(self):
        return f'{self.id}:{self.login}'
