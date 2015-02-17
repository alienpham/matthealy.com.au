from flask import g, current_app
from flask.ext.wtf import Form
from wtforms import TextField, TextAreaField
from wtforms.validators import Required, Email

class ContactForm(Form):

    name = TextField('name', validators = [Required()])
    email = TextField('email', validators=[Required(), Email()])
    subject = TextField('subject', validators = [Required()])
    message = TextAreaField('message', validators = [Required()])
