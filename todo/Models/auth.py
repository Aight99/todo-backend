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

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return self.is_active

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def __str__(self):
        return f'{self.id}:{self.login}'
