from flask import g, current_app
from flask.ext.wtf import Form
from flask.ext.pagedown.fields import PageDownField
from wtforms import TextField, HiddenField, TextAreaField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Optional, Email
from ..models import User, Post

class LoginForm(Form):
    email = TextField('email', validators=[Required(), Email()])
    password = PasswordField('password', validators=[Required()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')

class PostForm(Form):
    id = HiddenField('post_id')
    title = TextField('title', validators=[Required()])
    content = PageDownField("Start writing!", validators=[Required()])
    submit = SubmitField('Submit')
