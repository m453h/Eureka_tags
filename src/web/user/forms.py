from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import Length, ValidationError


class PostForm(FlaskForm):
    title = StringField('Title', validators=[Length(min=10)])
    content = TextAreaField('content')
    submit = SubmitField('Save changes')

