from app import db
from flask import url_for, current_app, request
import hashlib
from werkzeug.security import generate_password_hash, check_password_hash



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    email = db.Column(db.String(64), index = True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post',backref='user', lazy='dynamic')

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return True

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User %r %r>' % (self.first_name, self.last_name)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(64))
    title = db.Column(db.String(64))
    content = db.Column(db.Text)
    timestamp = db.Column(db.DateTime)
    deleted = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Entry %r>' % (self.name)
