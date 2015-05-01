from app import db
from flask import url_for, current_app, request
import hashlib
from markdown import markdown
import bleach
from werkzeug.security import generate_password_hash, check_password_hash
from bs4 import BeautifulSoup

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

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))

    def __repr__(self):
        return '<Tag %r>' % (self.name)

posttags = db.Table('post_tag',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'))
)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(128), index = True)
    title = db.Column(db.String(128))
    content = db.Column(db.Text)
    content_html = db.Column(db.Text)
    timestamp = db.Column(db.DateTime)
    deleted = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    tags = db.relationship('Tag',
                           secondary = posttags,
                           backref=db.backref('posts', lazy='dynamic'),
                           lazy='dynamic')

    @staticmethod
    def on_changed_content(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                        'em', 'i', 'img', 'li', 'ol', 'pre', 'strong', 'ul',
                        'h1', 'h2', 'h3', 'p']
        allowed_attributes = {
                'img': ['src', 'alt', 'width', 'height', 'class'],
                'a': ['href']
        }

        soup = BeautifulSoup(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True, attributes=allowed_attributes))

        target.content_html = str(soup)

    def __repr__(self):
        return '<Post %r>' % (self.title)

db.event.listen(Post.content, 'set', Post.on_changed_content)
